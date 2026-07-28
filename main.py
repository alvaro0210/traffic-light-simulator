"""
main.py

This is the entry point of the program - the file you actually run.
It creates our two objects (TrafficController and PedestrianCrossing),
then runs a loop that simulates time passing, printing what's happening
at each step so we can see the system working.

This version demonstrates:
  - Switching into rush hour mode partway through the simulation
  - A pedestrian request that gets fulfilled with a fixed walk duration
    (rather than walking for the entire red light)
"""

from traffic_controller import TrafficController
from pedestrian_crossing import PedestrianCrossing

# How many ticks (simulated seconds) to run the simulation for
SIMULATION_LENGTH = 50

# When should a pedestrian "press the button"?
PEDESTRIAN_PRESS_TICK = 5

# When should rush hour mode kick in? (just for demo purposes)
RUSH_HOUR_START_TICK = 25


def run_simulation():
    # Create our two components
    traffic = TrafficController()
    crossing = PedestrianCrossing(walk_duration=5)

    print(f"{'Tick':<6}{'Traffic Light':<15}{'Pedestrian':<12}{'Rush Hour':<10}")
    print("-" * 43)

    for tick in range(SIMULATION_LENGTH):
        # Simulate a pedestrian pressing the button at a specific moment
        if tick == PEDESTRIAN_PRESS_TICK:
            crossing.press_button()
            print(f"  >>> Pedestrian pressed the button at tick {tick}")

        # Simulate rush hour starting partway through the simulation
        if tick == RUSH_HOUR_START_TICK:
            traffic.set_rush_hour(True)
            print(f"  >>> Rush hour mode activated at tick {tick}")

        # Update the pedestrian crossing BEFORE advancing the traffic light,
        # so it reacts to the traffic light's state at the START of this tick
        crossing.update(traffic.get_state())

        # Print the current state of everything this tick
        rush_hour_label = "YES" if traffic.rush_hour else "no"
        print(
            f"{tick:<6}{traffic.get_state().value:<15}"
            f"{crossing.get_state().value:<12}{rush_hour_label:<10}"
        )

        # Advance the traffic light by one tick
        traffic.tick()


if __name__ == "__main__":
    # This line means: "only run the simulation if this file is executed
    # directly (not if it's imported into another file)." It's standard
    # Python practice.
    run_simulation()
