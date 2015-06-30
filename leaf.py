class Leaf:
    def __init__(self, message, resource):
        self.message = message
        self.resource = resource

    def start(self, done_callback):
        self.done_callback = done_callback
        print self.message

    def event(self, to_handle):
        assert self.done_callback
        assert to_handle == self.resource
        self.done_callback(self)

    def resources(self):
        return {self.resource: True}


