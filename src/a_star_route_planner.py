import math

import matplotlib.pyplot as plt
from car_park import CarPark # Importing the CarPark class from another file


class Node:
    def __init__(self, x, y, cost, parent_node_index):
        self.x = x  # x-coordinate of the node
        self.y = y  # y-coordinate of the node
        self.cost = cost # Cost associated with reaching this node
        self.parent_node_index = parent_node_index # Index of the parent node in the closed set


class AStarRoutePlanner:
    def __init__(self, car_park): 
        self.car_park: CarPark = car_park # Reference to the car park object


        # Motion Model: dx, dy, cost for different movements
        self.motions = [
            [1, 0, 1],
            [0, 1, 1],
            [-1, 0, 1],
            [0, -1, 1],
            [-1, -1, math.sqrt(2)],
            [-1, 1, math.sqrt(2)],
            [1, -1, math.sqrt(2)],
            [1, 1, math.sqrt(2)],
        ]

        self.goal_node: Node = Node(0, 0, 0.0, -1) # Initialize the goal node

    # Function to search for a route using A* algorithm
    def search_route(self, start_point, goal_point, show_process=True):
        start_node = Node(start_point[0], start_point[1], 0.0, -1) # Create a start node
        self.goal_node = Node(goal_point[0], goal_point[1], 0.0, -1) # Create a goal node

        open_set = {self.car_park.get_grid_index(start_node.x, start_node.y): start_node}  # Nodes to be evaluated
        closed_set = {} # Evaluated nodes

        while open_set:
            # Choose the node with the lowest cost 
            current_node_index = min(
                open_set,
                key=lambda o: open_set[o].cost + self.calculate_heuristic_cost(open_set[o]),
            )
            current_node = open_set[current_node_index] 

            if show_process:
                self.plot_process(current_node, closed_set) # Plot current process


            if current_node.x == self.goal_node.x and current_node.y == self.goal_node.y:
                print("Find goal")
                self.goal_node = current_node
                return self.process_route(closed_set) # Reconstruct the path

            # Move current node from open set to closed set
            del open_set[current_node_index]

            # Explore neighbor nodes
            closed_set[current_node_index] = current_node

            # expand_grid search grid based on motion model
            for motion in self.motions:
                next_node = Node(
                    current_node.x + motion[0],
                    current_node.y + motion[1],
                    current_node.cost + motion[2],
                    current_node_index,
                )
                next_node_index = self.car_park.get_grid_index(
                    next_node.x, next_node.y
                )

                if self.car_park.is_not_crossed_obstacle(
                        (current_node.x, current_node.y),
                        (next_node.x, next_node.y),
                ):
                    if next_node_index in closed_set:
                        continue

                    if next_node_index not in open_set:
                        open_set[next_node_index] = next_node  # Add newly discovered node
                    else:
                        if open_set[next_node_index].cost > next_node.cost:
                            # Update the cost of existing node if a better path is found
                            open_set[next_node_index] = next_node

        print("Cannot find Route")
        return [], []

    # Reconstruct the path from the goal node to the start node
    def process_route(self, closed_set):
        rx = [round(self.goal_node.x)]
        ry = [round(self.goal_node.y)]
        parent_node = self.goal_node.parent_node_index
        while parent_node != -1:
            n = closed_set[parent_node]
            rx.append(n.x)
            ry.append(n.y)
            parent_node = n.parent_node_index
        return rx, ry

    # Calculate heuristic cost (Euclidean distance) from current node to goal node
    def calculate_heuristic_cost(self, node):
        distance = math.sqrt(
            (node.x - self.goal_node.x) ** 2
            + (node.y - self.goal_node.y) ** 2
        )

        cost = distance
        return cost

    # Plot the current process
    @staticmethod
    def plot_process(current_node, closed_set):
        # show graph
        plt.plot(current_node.x, current_node.y, "xc") # Plot current node
        
        # For stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect(
            "key_release_event",
            lambda event: [exit(0) if event.key == "escape" else None],
        )
        if len(closed_set.keys()) % 10 == 0:
            plt.pause(0.001)


def main():
    car_park = CarPark() # Create a car park object
    obstacle_x = [obstacle[0] for obstacle in car_park.obstacles]
    obstacle_y = [obstacle[1] for obstacle in car_park.obstacles]
    plt.plot(obstacle_x, obstacle_y, ".k") # Plot obstacles

    # Define start and goal points
    start_point = [14, 4]
    goal_point = [69, 59]
    print(f"Start A Star Route Planner (start {start_point}, end {goal_point})")

    # Plot start and goal points
    plt.plot(start_point[0], start_point[1], "og")
    plt.plot(goal_point[0], goal_point[1], "xb")
    plt.text(start_point[0], start_point[1], 'Start', color='green', fontsize=10, ha='right')
    plt.text(goal_point[0], goal_point[1], 'Goal', color='blue', fontsize=10, ha='right')
    plt.title("A Star Route Planner")
    plt.grid(True)
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.axis("equal")

    # Create AStarRoutePlanner object and search for a route
    a_star = AStarRoutePlanner(car_park)
    rx, ry = a_star.search_route(start_point, goal_point, False)

    # Plot the found route
    plt.plot(rx, ry, "-r")
    plt.pause(0.001)
    plt.show()

if __name__ == "__main__":
    main()
