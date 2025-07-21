from collections import defaultdict

class ControllerRegistry:
    def __init__(self, controllers):
        self.by_state = defaultdict(list)
        for ctrl in controllers:
            for state in getattr(ctrl.__class__, "states", ()):
                self.by_state[state].append(ctrl)

    def get_for(self, state):
        return self.by_state[state]
