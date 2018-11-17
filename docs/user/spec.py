import zproc

ctx = zproc.Context()

ctx.start()


def my_proc(ctx):
    state = ctx.create_state()

    for snap in state.get_when_available():
        pass


ctx.spawn(my_proc)


swarm = ctx.create_swarm()


state = ctx.create_state()


state["test"] = 5
