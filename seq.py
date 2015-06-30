class Seq:
    def __init__(self, steps):
        self.steps = steps
        self.current_step = None

    def start(self, done_callback):
        assert self.current_step == None
        self.done_callback = done_callback
        self.current_step = 0
        self.steps[self.current_step].start(self.done)

    def done(self):
        assert self.current_step != None
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            self.steps[self.current_step].start(self.done)
        else:
            self.done_callback()

    def event(self, to_handle):
        assert self.current_step != None
        self.steps[self.current_step].event(to_handle)

    def resources(self):
        a = {}
        for s in self.steps:
            for r in s.resources():
                a[r] = True
        return a




