import signal
import struct
from typing import NamedTuple

TASK_NONCE_LENGTH = ZMQ_IDENTITY_LENGTH = 8

TASK_INFO_FMT = ">III"
TASK_ID_LENGTH = TASK_NONCE_LENGTH + struct.calcsize(TASK_INFO_FMT)

CHUNK_INFO_FMT = ">i"
CHUNK_ID_LENGTH = TASK_ID_LENGTH + struct.calcsize(CHUNK_INFO_FMT)

DEFAULT_ZMQ_RECVTIMEO = -1
DEFAULT_NAMESPACE = "default"

ALL_SIGNALS = set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP}

CLOSE_WORKER_MSG = [b""]


class Msgs:
    cmd = 0
    info = 1
    namespace = 2
    args = 3
    kwargs = 4


class Commands:
    ping = 0
    get_server_meta = 1

    get_state = 2
    set_state = 3

    run_fn_atomically = 4
    run_dict_method = 5

    watch = 6


class ServerMeta(NamedTuple):
    version: str

    server_address: str
    watcher_router: str

    task_router: str
    task_result_pull: str
    task_pub_ready: str

    task_proxy_in: str
    task_proxy_out: str


# ServerMeta = NamedTuple(
#     "ServerMeta",
#     [
#         ("version", str),
#         ("state_router", str),
#         ("state_pub", str),
#         ("task_router", str),
#         ("task_result_pull", str),
#         ("task_pub_ready", str),
#         ("task_proxy_in", str),
#         ("task_proxy_out", str),
#     ],
# )
