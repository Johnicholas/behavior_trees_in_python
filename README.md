# seq:

* handles start by delegating to its first step DONE
* handles done by starting its next step, DONE
* or calling its done callback if there is no next step DONE
* handles event by delegating to its current step DONE
* handles resources by computing the union of its steps resources DONE

# par:

* handles start by delegating to all of its lanes, DONE
* handles done by decrementing its count of lanes outstanding DONE
* or calling its done callback if there is no next step DONE
* handles event by looking the event up in its event to lane map, DONE
* (and delegating to the appropriate lane)
* handles resources by computing the union of its lanes resources, DONE
* (which are required to be disjoint)

# leaf:

* handles start by printing a message
* handles event by calling its done callback
* handles resources by returning a singleton set

# po:

* handles start by delegating to all its operations that have zero prereqs, DONE
* handles done by decrementing the prereqs of all the immediate successors, DONE
* and starting them if they have zero outstanding prereqs DONE
* handles event by looking the event up in the current resource-to-op map, DONE
* and delegating to that op. DONE
* handles resources by computing the union of its operations resources DONE





