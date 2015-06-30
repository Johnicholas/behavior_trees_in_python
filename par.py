class Par:
    def __init__(self, lanes):
        self.lanes = lanes
        self.lanes_outstanding = None
        self.event_to_lane = {}
        for l in lanes:
            for r in lanes[l].resources():
                assert r not in self.event_to_lane
                self.event_to_lane[r] = l

    def start(self, done_callback):
        assert self.lanes_outstanding == None
        self.done_callback = done_callback
        self.lanes_outstanding = 0
        for l in self.lanes:
            self.lanes_outstanding += 1 
            self.lanes[l].start(self.done)

    def done(self):
        if self.lanes_outstanding > 1:
            self.lanes_outstanding -= 1
        else:
            self.done_callback()

    def event(self, to_handle):
        l = self.event_to_lane[to_handle]
        self.lanes[l].event(to_handle)

    def resources(self):
        a = {}
        for l in self.lanes:
            for r in self.lanes[l].resources():
                a[r] = True
        return a




