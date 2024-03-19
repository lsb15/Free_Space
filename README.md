# Free_Space

# The Car Park Route Planning System

## Overview

The Car Park Route Planning System is a collection of Python modules designed to facilitate route planning within a cark park environment. It includes implementations of the A* algorithm and the Hybrid A* algorithm for finding optimal paths between two points while considering obstacles and vehicle dynamics.

The system consists of the following modules:

1. **`car_park.py`**: Defines the `CarPark` class, representing the layout of the car park environment, including obstacles and boundary constraints.

2. **`a_star_route_planner.py`**: Implements the A* Route Planner using the A* algorithm to find the shortest path between two points within the car park.

3. **`hybrid_a_star_route_planner.py`**: Implements the Hybrid A* Route Planner, an extension of the A* algorithm, which incorporates vehicle dynamics and continuous motion planning to find optimal paths considering vehicle kinematics.

## Modules

### `car_park.py`

The `car_park.py` module provides functionalities to define and visualize the layout of the car park environment. Key features include:

- Representation of obstacles and boundary constraints within the car park.
- Methods for checking obstacle collision and generating grid indices.
- Visualization of the car park layout using Matplotlib.

### `a_star_route_planner.py`

The `a_star_route_planner.py` module implements the A* Route Planner using the A* algorithm. Key features include:

- Definition of the `AStarRoutePlanner` class, which performs route planning using the A* algorithm.
- Utilization of a grid-based search to find the shortest path while avoiding obstacles.
- Visualization of the search process and calculated path within the car park environment.

### `hybrid_a_star_route_planner.py`

The `hybrid_a_star_route_planner.py` module implements the Hybrid A* Route Planner, an extension of the A* algorithm, considering vehicle dynamics and continuous motion planning. Key features include:

- Definition of the `HybridAStarRoutePlanner` class, which performs route planning using the Hybrid A* algorithm.
- Incorporation of vehicle kinematics, including wheelbase and steering inputs, to generate feasible trajectories.
- Visualization of the search process, starting pose, goal pose, and calculated path within the car park environment.

## Usage

To utilize the Car Park Route Planning System, follow these steps:

1. Import the required modules into your Python script or interactive environment.

2. Define the layout of the car park environment using the `CarPark` class from `car_park.py`.

3. Choose the appropriate route planner (`AStarRoutePlanner` or `HybridAStarRoutePlanner`) based on your requirements.

4. Specify the starting and goal poses within the car park environment.

5. Use the route planner to find the optimal path between the specified poses.

6. Visualize the search process and calculated path within the car park environment using the provided visualization methods.



**Reference:
PythonRobotics A* grid planning 
(author: Atsushi Sakai(@Atsushi_twi) / Nikos Kanargias (nkana@tee.gr))
https://github.com/AtsushiSakai/PythonRobotics/blob/master/PathPlanning/AStar/a_star.py

