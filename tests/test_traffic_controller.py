"""
test_traffic_controller.py

Unit tests verify that individual pieces of your code behave correctly,
in isolation. This is standard practice in real engineering work - it's
one of the things that separates a "hobby script" from a properly
engineered piece of software, and it's worth highlighting on a resume.

We use Python's built-in 'unittest' module here since it requires no
extra installation.

To run these tests, navigate to the project's root folder and run:
    python -m unittest tests/test_traffic_controller.py
"""

import unittest
import sys
import os

# This adds the parent folder to Python's search path, so this test file
# (which lives inside tests/) can find traffic_controller.py (which lives
# one folder up, in the project root)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from traffic_controller import TrafficController, LightState


class TestTrafficController(unittest.TestCase):

    def test_starts_at_red(self):
        """A brand new traffic light should always start at RED - this is
        a real-world safety rule, so it's worth explicitly testing for it."""
        controller = TrafficController()
        self.assertEqual(controller.get_state(), LightState.RED)

    def test_transitions_red_to_green(self):
        """After enough ticks pass, RED should transition to GREEN."""
        controller = TrafficController(
            normal_durations={LightState.RED: 3, LightState.GREEN: 10, LightState.YELLOW: 3}
        )
        for _ in range(3):
            controller.tick()
        self.assertEqual(controller.get_state(), LightState.GREEN)

    def test_transitions_green_to_yellow(self):
        controller = TrafficController(
            normal_durations={LightState.RED: 10, LightState.GREEN: 2, LightState.YELLOW: 3}
        )
        # First, force it out of RED so we're testing GREEN specifically
        controller.state = LightState.GREEN
        controller.timer = 0
        for _ in range(2):
            controller.tick()
        self.assertEqual(controller.get_state(), LightState.YELLOW)

    def test_full_cycle_returns_to_red(self):
        """Confirms the full cycle RED -> GREEN -> YELLOW -> RED works
        correctly over a complete loop."""
        controller = TrafficController(
            normal_durations={LightState.RED: 2, LightState.GREEN: 2, LightState.YELLOW: 2}
        )
        for _ in range(6):  # 2+2+2 ticks = one full cycle
            controller.tick()
        self.assertEqual(controller.get_state(), LightState.RED)

    def test_rush_hour_uses_different_durations(self):
        """Confirms that switching to rush hour mode actually changes the
        timing the controller uses - this is the core of the new feature."""
        controller = TrafficController(
            normal_durations={LightState.RED: 10, LightState.GREEN: 10, LightState.YELLOW: 3},
            rush_hour_durations={LightState.RED: 5, LightState.GREEN: 20, LightState.YELLOW: 3},
        )
        controller.set_rush_hour(True)
        self.assertEqual(controller.durations[LightState.GREEN], 20)
        controller.set_rush_hour(False)
        self.assertEqual(controller.durations[LightState.GREEN], 10)


if __name__ == "__main__":
    unittest.main()
