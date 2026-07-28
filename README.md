# Traffic Light & Pedestrian Crossing Simulator

A Python simulation of a traffic light system with pedestrian crossing logic, modeled as a finite state machine.

## Why I Built This

As an incoming Computer Engineering student at the University of Manitoba, I wanted a project that would help me practice core embedded-systems concepts — finite state machines, timing logic, and event-driven behavior — before starting coursework in control systems (ECE 2220/2262). Traffic light systems are a classic real-world example of this kind of logic.

## What It Does

- Models a traffic light cycling through RED → GREEN → YELLOW states with configurable durations
- Models a pedestrian crossing signal (WALK / DON'T WALK) that responds to a pedestrian pressing a crossing button
- Ensures pedestrians can only be given a WALK signal when the traffic light is RED (a basic safety constraint)
- Runs a tick-based simulation (each "tick" represents one time step) and prints the state of both systems over time

## How to Run It

```bash
python3 main.py
```

To run the unit tests:

```bash
python -m unittest tests/test_traffic_controller.py -v
```

## Project Structure

```
traffic-light-simulator/
├── README.md
├── traffic_controller.py   # Core traffic light state machine
├── pedestrian_crossing.py  # Pedestrian signal logic
├── main.py                 # Runs the simulation
└── tests/
    └── test_traffic_controller.py
```

## What I'd Extend Next

- Multiple intersections coordinating with each other
- Variable timing based on time of day (e.g., rush hour vs. off-peak)
- A visual (graphical) representation instead of text output

## Author

Alvaro Oda — Computer Engineering student, University of Manitoba
