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
    """

    def __init__(self, green_duration=10, yellow_duration=3, red_duration=10):
        """
        The __init__ method runs automatically when you create a new
        TrafficController object. It sets up the starting values.

        Parameters (the numbers below are in "ticks" - think of a tick as
        one second, or one simulation step - we'll define this more in main.py):
            green_duration: how long the light stays green
            yellow_duration: how long the light stays yellow
            red_duration: how long the light stays red
        """
        self.state = LightState.RED  # every traffic light starts at RED
        self.timer = 0  # tracks how long we've been in the current state

        # Store the durations so we can reference them when deciding
        # whether it's time to switch states
        self.durations = {
            LightState.GREEN: green_duration,
            LightState.YELLOW: yellow_duration,
            LightState.RED: red_duration,
        }

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
