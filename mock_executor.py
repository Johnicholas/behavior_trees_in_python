class MockExecutor:
    def __init__(self, resource):
        self.seen = []
        self.resource = resource

    def start(self, done_callback):
        self.seen.append(('start', done_callback))

    def event(self, to_handle):
        self.seen.append(('event', to_handle))

    def resources(self):
        return {self.resource: True}

