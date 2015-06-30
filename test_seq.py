from seq import *
from mock_executor import *
from top import *


class SeqWithTwoSteps():
    def __init__(self):
        self.first_step = MockExecutor('foo')
        self.second_step = MockExecutor('bar')
        self.to_test = Seq([self.first_step, self.second_step])
        self.top = Top()


def handles_start_by_delegating_to_its_first_step():
    s = SeqWithTwoSteps()
    s.to_test.start(s.top)
    assert len(s.first_step.seen) == 1
    assert s.first_step.seen[0][0] == 'start'
    assert len(s.second_step.seen) == 0
    assert s.top.seen == 0

def handles_done_by_starting_its_next_step():
    s = SeqWithTwoSteps()
    s.to_test.start(s.top)
    s.to_test.done()
    assert len(s.second_step.seen) == 1
    assert s.second_step.seen[0][0] == 'start'
    assert s.top.seen == 0

def calls_its_done_callback_if_there_is_no_next_step():
    s = SeqWithTwoSteps()
    s.to_test.start(s.top)
    s.to_test.done()
    s.to_test.done()
    assert s.top.seen == 1

def handles_event_by_delegating_to_its_current_step():
    s = SeqWithTwoSteps()
    s.to_test.start(s.top)
    s.to_test.event('hello')
    assert len(s.first_step.seen) == 2
    assert s.first_step.seen[1] == ('event', 'hello')
    s.to_test.done()
    s.to_test.event('world')
    assert len(s.second_step.seen) == 2
    assert s.second_step.seen[1] == ('event', 'world')

def handles_resources_by_computing_union_of_its_steps_resources():
    s = SeqWithTwoSteps()
    assert s.to_test.resources() == {'foo': True, 'bar': True}

if __name__ == '__main__':
    handles_start_by_delegating_to_its_first_step()
    handles_done_by_starting_its_next_step()
    calls_its_done_callback_if_there_is_no_next_step()
    handles_event_by_delegating_to_its_current_step()
    handles_resources_by_computing_union_of_its_steps_resources()






    

