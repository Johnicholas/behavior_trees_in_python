class Op:
    def __init__(self, executor):
        self.prereqs = 0
        self.executor = executor
        self.successors = []

class Po:
    def __init__(self):
        self.ops = []

    def add(self, to_add):
        answer = len(self.ops)
        self.ops.append(Op(to_add))
        return answer

    def before(self, op1, op2):
        assert op1 >= 0 and op1 < len(self.ops)
        assert op2 >= 0 and op2 < len(self.ops)
        self.ops[op2].prereqs += 1
        self.ops[op1].successors.append(op2)

    def start_op(self, oid, o):
        self.ops_outstanding += 1
        for r in o.executor.resources():
            assert r not in self.event_to_op
            self.event_to_op[r] = oid
        o.executor.start(lambda: self.done(oid))

    def start(self, done_callback):
        self.done_callback = done_callback
        self.event_to_op = {}
        self.ops_outstanding = 0
        for oid, o in enumerate(self.ops):
            if o.prereqs == 0:
                self.start_op(oid, o)

    def done(self, oid):
        o = self.ops[oid]
        for r in o.executor.resources():
            assert r in self.event_to_op
            del self.event_to_op[r]
        for s in o.successors:
            assert self.ops[s].prereqs >= 1
            self.ops[s].prereqs -= 1
            if self.ops[s].prereqs == 0:
                self.start_op(s, self.ops[s])
        assert self.ops_outstanding >= 1
        self.ops_outstanding -= 1
        if self.ops_outstanding == 0:
            self.done_callback()

    def event(self, to_handle):
        oid = self.event_to_op[to_handle]
        o = self.ops[oid]
        o.executor.event(to_handle)

    def resources(self):
        a = {}
        for o in self.ops:
            for r in o.executor.resources():
                a[r] = True
        return a





