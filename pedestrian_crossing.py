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
    def __init__(self, walk_duration=5):
        """
        Parameters:
            walk_duration: how many ticks the WALK signal stays on for,
                           regardless of how long the light stays red.
                           Real pedestrian signals work this way - you get
                           a fixed amount of time to cross, not "however
                           long the light happens to stay red."
        """
        self.state = PedestrianState.DONT_WALK
        self.request_pending = False  # has someone pressed the button?
        self.walk_duration = walk_duration
        self.walk_timer = 0  # tracks how long we've been in WALK state

    def press_button(self):
        """
        Called when a pedestrian presses the crossing button.
        We just record that a request came in - we don't act on it
        immediately, because we have to wait for the traffic light
        to actually be RED before it's safe to walk.

        EDGE CASE handled here: if the button is pressed multiple times
        (e.g., an impatient pedestrian mashing it, or multiple people
        pressing it), nothing breaks - request_pending is just set to
        True again, which has no extra effect. This is called being
        "idempotent" - calling it many times has the same result as
        calling it once.
        """
        self.request_pending = True

    def update(self, traffic_state):
        """
        This is called every tick (same as TrafficController.tick()),
        and decides what the pedestrian signal should show based on:
          1. Whether a walk request is pending
          2. What the traffic light is currently doing
          3. How long we've already been showing WALK

        Parameters:
            traffic_state: the current LightState of the traffic light
                           (passed in from main.py, since this class doesn't
                           control the traffic light itself)
        """
        if self.state == PedestrianState.WALK:
            # We're already walking - count up the timer and check if
            # the fixed walk duration has run out
            self.walk_timer += 1
            if self.walk_timer >= self.walk_duration or traffic_state != LightState.RED:
                # Either the walk time is up, OR the light changed early
                # (EDGE CASE: light changes before walk_duration finishes -
                # safety wins, so we cut the walk signal short)
                self.state = PedestrianState.DONT_WALK
                self.walk_timer = 0

        elif traffic_state == LightState.RED and self.request_pending:
            # Not currently walking, but a request is pending and it's
            # now safe (light is red) - start the walk signal
            self.state = PedestrianState.WALK
            self.walk_timer = 0
            self.request_pending = False  # request has been fulfilled

        elif traffic_state != LightState.RED:
            # No active walk signal, light isn't red - nothing to do,
            # stay in DONT_WALK. (EDGE CASE: a request could still be
            # "pending" here, waiting patiently for the next red light -
            # we deliberately do NOT clear request_pending in this branch,
            # so the pedestrian doesn't have to press the button again.)
            self.state = PedestrianState.DONT_WALK

    def get_state(self):
        return self.state
