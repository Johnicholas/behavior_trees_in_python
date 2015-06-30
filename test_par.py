from par import *
from mock_executor import *
from top import *

class ParWithTwoLanes:
    def __init__(self):
        self.left_lane = MockExecutor('foo')
        self.right_lane = MockExecutor('bar')
        self.to_test = Par({'left': self.left_lane, 'right': self.right_lane})
        self.top = Top()

def handles_start_by_delegating_to_all_of_its_lanes():
    s = ParWithTwoLanes()
    s.to_test.start(s.top)
    assert len(s.left_lane.seen) == 1
    assert s.left_lane.seen[0][0] == 'start'
    assert len(s.right_lane.seen) == 1
    assert s.right_lane.seen[0][0] == 'start'

def handles_done_by_decrementing_its_count_of_lanes_outstanding():
    s = ParWithTwoLanes()
    s.to_test.start(s.top)
    assert s.to_test.lanes_outstanding == 2
    s.to_test.done()
    assert s.to_test.lanes_outstanding == 1

def calls_its_done_callback_if_there_are_no_lanes_outstanding():
    s = ParWithTwoLanes()
    s.to_test.start(s.top)
    assert s.top.seen == 0
    s.to_test.done()
    assert s.top.seen == 0
    s.to_test.done()
    assert s.top.seen == 1

def handles_event_by_looking_the_event_up_in_its_event_to_lane_map():
    s1 = ParWithTwoLanes()
    s1.to_test.start(s1.top)
    s1.to_test.event('foo')
    assert len(s1.left_lane.seen) == 2
    assert s1.left_lane.seen[1] == ('event', 'foo')
    assert len(s1.right_lane.seen) == 1
    s2 = ParWithTwoLanes()
    s2.to_test.start(s2.top)
    s2.to_test.event('bar')
    assert len(s2.right_lane.seen) == 2
    assert s2.right_lane.seen[1] == ('event', 'bar')
    assert len(s2.left_lane.seen) == 1

def handles_resources_by_computing_the_union_of_its_lanes_resources():
    s = ParWithTwoLanes()
    assert s.to_test.resources() == {'foo': True, 'bar': True}

if __name__ == "__main__":
    handles_start_by_delegating_to_all_of_its_lanes()
    handles_done_by_decrementing_its_count_of_lanes_outstanding()
    calls_its_done_callback_if_there_are_no_lanes_outstanding()
    handles_event_by_looking_the_event_up_in_its_event_to_lane_map()
    handles_resources_by_computing_the_union_of_its_lanes_resources()





