from collections import Iterable
from multiprocessing.connection import Connection
from typing import Union, Callable

import zmq

from zproc import util
from zproc.consts import CLOSE_WORKER_MSG
from zproc.exceptions import RemoteException
from zproc.state.state import State
from .map_plus import map_plus


def run_task(
    target: Callable, task: Iterable, state: State
) -> Union[list, RemoteException]:
    params, pass_state, namespace = task
    if pass_state:
        state.namespace = namespace

        def target_with_state(*args, **kwargs):
            return target(state, *args, **kwargs)

        target = target_with_state

    return map_plus(target, *params)


# fmt: off
def worker_process(server_address: str, send_conn: Connection):
    try:
        with \
                util.create_zmq_ctx() as zmq_ctx, \
                zmq_ctx.socket(zmq.PULL) as proxy_out, \
                zmq_ctx.socket(zmq.PUSH) as result_pull:
            server_meta = util.get_server_meta(zmq_ctx, server_address)

            try:
                proxy_out.connect(server_meta.task_proxy_out)
                result_pull.connect(server_meta.task_result_pull)
                state = State(server_address)
            except Exception:
                send_conn.send_bytes(util.dumps(RemoteException()))
            else:
                send_conn.send_bytes(b"")
            finally:
                send_conn.close()

            while True:
                msg = proxy_out.recv_multipart()
                if msg == CLOSE_WORKER_MSG:
                    return
                chunk_id, target_bytes, task_bytes = msg

                try:
                    task = util.loads(task_bytes)
                    target = util.loads_fn(target_bytes)

                    result = run_task(target, task, state)
                except KeyboardInterrupt:
                    raise
                except Exception:
                    result = RemoteException()
                result_pull.send_multipart([chunk_id, util.dumps(result)])
    except Exception:
        util.log_internal_crash("Worker process")