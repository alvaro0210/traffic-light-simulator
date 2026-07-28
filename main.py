"""
main.py

This is the entry point of the program - the file you actually run.
It creates our two objects (TrafficController and PedestrianCrossing),
then runs a loop that simulates time passing, printing what's happening
at each step so we can see the system working.
"""

from traffic_controller import TrafficController
from pedestrian_crossing import PedestrianCrossing

# How many ticks (simulated seconds) to run the simulation for
SIMULATION_LENGTH = 40

# When should a pedestrian "press the button"? (just for demo purposes,
# we'll simulate someone pressing it at tick 5)
PEDESTRIAN_PRESS_TICK = 5


def run_simulation():
    # Create our two components
    traffic = TrafficController(green_duration=10, yellow_duration=3, red_duration=10)
    crossing = PedestrianCrossing()

    print(f"{'Tick':<6}{'Traffic Light':<15}{'Pedestrian':<12}")
    print("-" * 33)

    for tick in range(SIMULATION_LENGTH):
        # Simulate a pedestrian pressing the button at a specific moment
        if tick == PEDESTRIAN_PRESS_TICK:
            crossing.press_button()
            print(f"  >>> Pedestrian pressed the button at tick {tick}")

        # Update the pedestrian crossing BEFORE advancing the traffic light,
        # so it reacts to the traffic light's state at the START of this tick
        crossing.update(traffic.get_state())

        # Print the current state of both systems this tick
        print(f"{tick:<6}{traffic.get_state().value:<15}{crossing.get_state().value:<12}")

        # Advance the traffic light by one tick
        traffic.tick()


if __name__ == "__main__":
    # This line means: "only run the simulation if this file is executed
    # directly (not if it's imported into another file)." It's standard
    # Python practice.
    run_simulation()
