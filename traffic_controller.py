"""
traffic_controller.py

This file defines the TrafficController class, which models a traffic light
as a "state machine" - meaning the light is always in exactly one state
(RED, YELLOW, or GREEN), and moves between states based on rules we define.

Why use a class here? Because a traffic light has:
  - its own internal data (current state, how long it's been in that state)
  - its own behavior (how it decides to switch states)
A class lets us bundle that data and behavior together cleanly.
"""

from enum import Enum


class LightState(Enum):
    """
    An Enum (short for 'enumeration') is a way to define a fixed set of
    named values. Instead of using plain strings like "red" or "green"
    (which are easy to misspell), we define exact, safe options here.
    """
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"


class TrafficController:
    """
    Represents a single traffic light and manages its state transitions.

    This version supports two timing "profiles": NORMAL and RUSH_HOUR.
    During rush hour, green lights stay on longer (to let more cars through
    a busy intersection), which is a realistic behavior real traffic systems
    actually use.
    """

    def __init__(self, normal_durations=None, rush_hour_durations=None):
        """
        Instead of passing in three separate numbers like before, we now pass
        in two DICTIONARIES - one for normal timing, one for rush hour timing.
        This is a common pattern: when you have multiple related settings that
        travel together (a "profile" or "configuration"), it's cleaner to
        group them into one object (here, a dict) rather than pass a growing
        list of separate arguments.

        If nothing is provided, we fall back to sensible defaults using
        Python's "or" trick: `normal_durations or {...}` means "use
        normal_durations if it was given, otherwise use this default dict."
        """
        self.normal_durations = normal_durations or {
            LightState.GREEN: 10,
            LightState.YELLOW: 3,
            LightState.RED: 10,
        }
        self.rush_hour_durations = rush_hour_durations or {
            LightState.GREEN: 18,   # longer green - more cars need to pass
            LightState.YELLOW: 3,   # yellow safety timing doesn't change
            LightState.RED: 8,      # shorter red - keep traffic moving
        }

        self.rush_hour = False  # starts in normal mode by default
        self.state = LightState.RED  # every traffic light starts at RED
        self.timer = 0  # tracks how long we've been in the current state

    @property
    def durations(self):
        """
        A @property lets us define a method that behaves like a regular
        attribute (you access it as `self.durations`, not `self.durations()`).
        Here, it picks WHICH duration set to use based on whether rush hour
        mode is currently on - this way the rest of the code doesn't need to
        know or care which mode we're in, it just asks for "the durations."
        """
        return self.rush_hour_durations if self.rush_hour else self.normal_durations

    def set_rush_hour(self, is_rush_hour):
        """
        Turns rush hour mode on or off. In a real system, this might be
        triggered by a clock (e.g., 7-9am and 4-6pm) - for our simulation,
        we'll trigger it manually from main.py to keep things simple.
        """
        self.rush_hour = is_rush_hour

    def tick(self):
        """
        This method represents one "step" of time passing (e.g., one second).
        Call this repeatedly in a loop to simulate the light running over time.

        This is the core logic of the whole simulation: check if we've been
        in the current state long enough, and if so, move to the next one.
        """
        self.timer += 1

        # Check if it's time to transition to the next state
        if self.timer >= self.durations[self.state]:
            self._transition()
            self.timer = 0  # reset the timer for the new state

    def _transition(self):
        """
        Defines the ORDER of states: RED -> GREEN -> YELLOW -> RED -> ...
        The underscore prefix (_transition) is a Python convention meaning
        "this method is meant for internal use only, not called from outside
        the class."
        """
        if self.state == LightState.RED:
            self.state = LightState.GREEN
        elif self.state == LightState.GREEN:
            self.state = LightState.YELLOW
        elif self.state == LightState.YELLOW:
            self.state = LightState.RED

    def get_state(self):
        """A simple 'getter' method so other code can check the current state
        without directly touching the internal self.state variable. This is
        good practice - it keeps the internal details of the class protected."""
        return self.state
