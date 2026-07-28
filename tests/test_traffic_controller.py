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
        controller = TrafficController(red_duration=3)
        for _ in range(3):
            controller.tick()
        self.assertEqual(controller.get_state(), LightState.GREEN)

    def test_transitions_green_to_yellow(self):
        controller = TrafficController(green_duration=2)
        # First, force it out of RED so we're testing GREEN specifically
        controller.state = LightState.GREEN
        controller.timer = 0
        for _ in range(2):
            controller.tick()
        self.assertEqual(controller.get_state(), LightState.YELLOW)

    def test_full_cycle_returns_to_red(self):
        """Confirms the full cycle RED -> GREEN -> YELLOW -> RED works
        correctly over a complete loop."""
        controller = TrafficController(red_duration=2, green_duration=2, yellow_duration=2)
        for _ in range(6):  # 2+2+2 ticks = one full cycle
            controller.tick()
        self.assertEqual(controller.get_state(), LightState.RED)


if __name__ == "__main__":
    unittest.main()
