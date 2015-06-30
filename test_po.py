from po import *
from mock_executor import *
from top import *

class LikeSeqWithTwoSteps():
    def __init__(self):
        self.first_step = MockExecutor('foo')
        self.second_step = MockExecutor('bar')
        self.to_test = Po()
        first_step_key = self.to_test.add(self.first_step)
        second_step_key = self.to_test.add(self.second_step)
        self.to_test.before(first_step_key, second_step_key)
        self.top = Top()

def can_act_like_a_seq():
    s = LikeSeqWithTwoSteps()
    s.to_test.start(s.top)
    assert len(s.first_step.seen) == 1
    assert s.first_step.seen[0][0] == 'start'
    assert len(s.second_step.seen) == 0
    assert s.top.seen == 0
    s.to_test.event('foo')
    assert len(s.first_step.seen) == 2
    assert s.first_step.seen[1] == ('event', 'foo')
    s.to_test.done(0)
    assert len(s.second_step.seen) == 1
    assert s.second_step.seen[0][0] == 'start'
    assert s.top.seen == 0
    s.to_test.event('bar')
    assert len(s.second_step.seen) == 2
    assert s.second_step.seen[1] == ('event', 'bar')
    s.to_test.done(1)
    assert s.top.seen == 1

class LikeParWithTwoLanes():
    def __init__(self):
        self.left_lane = MockExecutor('foo')
        self.right_lane = MockExecutor('bar')
        self.to_test = Po()
        self.to_test.add(self.left_lane)
        self.to_test.add(self.right_lane)
        self.top = Top()

def can_act_like_a_par():
    s = LikeParWithTwoLanes()
    s.to_test.start(s.top)
    assert len(s.left_lane.seen) == 1
    assert s.left_lane.seen[0][0] == 'start'
    assert len(s.right_lane.seen) == 1
    assert s.right_lane.seen[0][0] == 'start'
    assert s.to_test.ops_outstanding == 2
    assert s.top.seen == 0
    s.to_test.event('foo')
    assert len(s.left_lane.seen) == 2
    assert s.left_lane.seen[1] == ('event', 'foo')
    assert len(s.right_lane.seen) == 1
    s.to_test.event('bar')
    assert len(s.right_lane.seen) == 2
    assert s.right_lane.seen[1] == ('event', 'bar')
    s.to_test.done(0)
    assert s.to_test.ops_outstanding == 1
    s.to_test.done(1)
    assert s.top.seen == 1

def handles_resources_by_computing_the_union_of_its_lanes_resources():
    s1 = LikeParWithTwoLanes()
    assert s1.to_test.resources() == {'foo': True, 'bar': True}
    s2 = LikeSeqWithTwoSteps()
    assert s2.to_test.resources() == {'foo': True, 'bar': True}

class TheNGraph():
    def __init__(self):
        self.a = MockExecutor('a')
        self.b = MockExecutor('b')
        self.c = MockExecutor('c')
        self.d = MockExecutor('d')
        self.to_test = Po()
        self.a_key = self.to_test.add(self.a)
        self.b_key = self.to_test.add(self.b)
        self.c_key = self.to_test.add(self.c)
        self.d_key = self.to_test.add(self.d)
        self.to_test.before(self.a_key, self.b_key)
        self.to_test.before(self.c_key, self.d_key)
        self.to_test.before(self.a_key, self.d_key)
        self.top = Top()

def ngraph_abcd():
    n = TheNGraph()
    n.to_test.start(n.top)
    assert n.to_test.ops_outstanding == 2
    assert len(n.a.seen) == 1
    assert n.a.seen[0][0] == 'start'
    assert len(n.c.seen) == 1
    assert n.c.seen[0][0] == 'start'
    assert len(n.b.seen) == 0
    assert len(n.d.seen) == 0
    n.to_test.event('a')
    assert len(n.a.seen) == 2
    assert n.a.seen[1] == ('event', 'a')
    n.to_test.event('c')
    assert len(n.c.seen) == 2
    assert n.c.seen[1] == ('event', 'c')
    n.to_test.done(n.a_key)
    assert len(n.b.seen) == 1
    assert n.b.seen[0][0] == 'start'
    n.to_test.event('c')
    assert len(n.c.seen) == 3
    assert n.c.seen[2] == ('event', 'c')
    n.to_test.event('b')
    assert len(n.b.seen) == 2
    assert n.b.seen[1] == ('event', 'b')
    assert n.to_test.ops_outstanding == 2
    n.to_test.done(n.b_key)
    assert len(n.c.seen) == 3
    assert len(n.d.seen) == 0
    assert n.to_test.ops_outstanding == 1
    n.to_test.done(n.c_key)
    assert len(n.d.seen) == 1
    assert n.d.seen[0][0] == 'start'
    assert n.to_test.ops_outstanding == 1
    n.to_test.event('d')
    assert len(n.d.seen) == 2
    assert n.d.seen[1] == ('event', 'd')
    assert n.top.seen == 0
    n.to_test.done(n.d_key)
    assert n.top.seen == 1

if __name__ == '__main__':
    can_act_like_a_seq()
    can_act_like_a_par()
    handles_resources_by_computing_the_union_of_its_lanes_resources()
    ngraph_abcd()
    
    




