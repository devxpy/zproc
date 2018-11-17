import random
import time

import zproc

TIMEOUT = 0.5
SLOW = False

ctx = zproc.Context()
ctx.state["foobar"] = 0


def wait_and_stop():
    try:
        test_process.wait(TIMEOUT)
    except TimeoutError:
        test_process.stop()
    print("\n" * 5, "-" * 10, "\n" * 5)
    time.sleep(1)


@zproc.atomic
def inc(snap):
    snap["foobar"] += 1


@ctx._process
def generator(state):
    while True:
        inc(state)
        if SLOW:
            time.sleep(random.random())


print("LIVE:")


@ctx._process
def test_process(state):
    while True:
        print(state.get_when_change("foobar", live=True), end=",", flush=True)
        if SLOW:
            time.sleep(random.random())


wait_and_stop()
print("BUFFERED:")


@ctx._process
def test_process(state):
    while True:
        print(state.get_when_change("foobar", live=False), end=",", flush=True)
        if SLOW:
            time.sleep(random.random())


wait_and_stop()
print("LIVE:")


@ctx.call_when_change("foobar", pass_state=False, live=True)
def test_process(foobar):
    print(foobar, end=",", flush=True)
    if SLOW:
        time.sleep(random.random())


wait_and_stop()
print("BUFFERED:")


@ctx.call_when_change("foobar", live=False, pass_state=False)
def test_process(foobar):
    print(foobar, end=",", flush=True)
    if SLOW:
        time.sleep(random.random())


wait_and_stop()
