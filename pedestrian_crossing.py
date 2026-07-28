"""
pedestrian_crossing.py

This models the pedestrian "Walk" / "Don't Walk" signal, and includes a
button that pedestrians can press to REQUEST a walk signal - this is the
"sensor-triggered" complexity we talked about adding in Week 2.

Design idea: the pedestrian signal doesn't decide things on its own -
it reacts to the traffic light's state. Pedestrians can only walk when
the traffic light is RED (cars stopped), so this class will need to look
at the TrafficController's state to decide what to show.
"""

from enum import Enum
from traffic_controller import LightState


class PedestrianState(Enum):
    WALK = "WALK"
    DONT_WALK = "DONT_WALK"


class PedestrianCrossing:
    def __init__(self):
        self.state = PedestrianState.DONT_WALK
        self.request_pending = False  # has someone pressed the button?

    def press_button(self):
        """
        Called when a pedestrian presses the crossing button.
        We just record that a request came in - we don't act on it
        immediately, because we have to wait for the traffic light
        to actually be RED before it's safe to walk.
        """
        self.request_pending = True

    def update(self, traffic_state):
        """
        This is called every tick (same as TrafficController.tick()),
        and decides what the pedestrian signal should show based on:
          1. Whether a walk request is pending
          2. What the traffic light is currently doing

        Parameters:
            traffic_state: the current LightState of the traffic light
                           (passed in from main.py, since this class doesn't
                           control the traffic light itself)
        """
        if traffic_state == LightState.RED and self.request_pending:
            self.state = PedestrianState.WALK
            self.request_pending = False  # request has been fulfilled
        elif traffic_state != LightState.RED:
            # As soon as the light isn't red anymore, force Don't Walk -
            # safety first, cars are moving again
            self.state = PedestrianState.DONT_WALK

    def get_state(self):
        return self.state
