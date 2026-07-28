"""
visualize.py

This runs the same simulation as main.py, but instead of printing a text
table, it draws a timeline chart using matplotlib - a Python library for
creating graphs and plots.

The idea: represent each state (RED/GREEN/YELLOW for the light, WALK/
DONT_WALK for pedestrians) as a colored horizontal bar, so you can see the
whole simulation's behavior at a glance, the same way a real engineer
might visualize a timing diagram for a control system.
"""

import matplotlib.pyplot as plt
from traffic_controller import TrafficController, LightState
from pedestrian_crossing import PedestrianCrossing, PedestrianState

SIMULATION_LENGTH = 50
PEDESTRIAN_PRESS_TICK = 5
RUSH_HOUR_START_TICK = 25

# Colors for each state - chosen to intuitively match real traffic lights
LIGHT_COLORS = {
    LightState.RED: "#d62728",
    LightState.GREEN: "#2ca02c",
    LightState.YELLOW: "#ffbf00",
}
PEDESTRIAN_COLORS = {
    PedestrianState.WALK: "#1f77b4",
    PedestrianState.DONT_WALK: "#7f7f7f",
}


def run_and_record():
    """
    Runs the simulation (same logic as main.py) but instead of printing,
    it records every state into lists we can hand off to matplotlib.
    Separating "run the simulation" from "display the simulation" like
    this is good practice - it means we could add a totally different
    display (a website, a different chart type) without touching the
    simulation logic itself.
    """
    traffic = TrafficController()
    crossing = PedestrianCrossing(walk_duration=5)

    light_history = []
    pedestrian_history = []
    rush_hour_ticks = []

    for tick in range(SIMULATION_LENGTH):
        if tick == PEDESTRIAN_PRESS_TICK:
            crossing.press_button()
        if tick == RUSH_HOUR_START_TICK:
            traffic.set_rush_hour(True)

        crossing.update(traffic.get_state())

        light_history.append(traffic.get_state())
        pedestrian_history.append(crossing.get_state())
        if traffic.rush_hour:
            rush_hour_ticks.append(tick)

        traffic.tick()

    return light_history, pedestrian_history, rush_hour_ticks


def plot_timeline(light_history, pedestrian_history, rush_hour_ticks):
    """
    Draws two horizontal timeline rows (one for the traffic light, one for
    the pedestrian signal), where each tick is a colored segment.
    """
    fig, ax = plt.subplots(figsize=(14, 3))

    # Draw each tick as a 1-unit-wide colored rectangle using ax.barh
    # (a horizontal bar chart) - we draw one bar per tick, per row.
    for tick, state in enumerate(light_history):
        ax.barh(1, 1, left=tick, color=LIGHT_COLORS[state], edgecolor="white", linewidth=0.5)

    for tick, state in enumerate(pedestrian_history):
        ax.barh(0, 1, left=tick, color=PEDESTRIAN_COLORS[state], edgecolor="white", linewidth=0.5)

    # Mark where rush hour starts with a vertical dashed line
    if rush_hour_ticks:
        ax.axvline(x=rush_hour_ticks[0], color="black", linestyle="--", linewidth=1)
        ax.text(rush_hour_ticks[0] + 0.3, 1.6, "Rush hour starts", fontsize=9)

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Pedestrian", "Traffic Light"])
    ax.set_xlabel("Tick (simulated time)")
    ax.set_title("Traffic Light & Pedestrian Crossing Simulation Timeline")
    ax.set_xlim(0, len(light_history))

    # Build a simple legend explaining the colors, since color alone
    # isn't enough context for someone viewing the chart cold
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, color=LIGHT_COLORS[LightState.RED], label="Red"),
        plt.Rectangle((0, 0), 1, 1, color=LIGHT_COLORS[LightState.GREEN], label="Green"),
        plt.Rectangle((0, 0), 1, 1, color=LIGHT_COLORS[LightState.YELLOW], label="Yellow"),
        plt.Rectangle((0, 0), 1, 1, color=PEDESTRIAN_COLORS[PedestrianState.WALK], label="Walk"),
        plt.Rectangle((0, 0), 1, 1, color=PEDESTRIAN_COLORS[PedestrianState.DONT_WALK], label="Don't Walk"),
    ]
    ax.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=5)

    plt.tight_layout()
    plt.savefig("simulation_timeline.png", dpi=150, bbox_inches="tight")
    print("Saved chart to simulation_timeline.png")


if __name__ == "__main__":
    light_history, pedestrian_history, rush_hour_ticks = run_and_record()
    plot_timeline(light_history, pedestrian_history, rush_hour_ticks)
