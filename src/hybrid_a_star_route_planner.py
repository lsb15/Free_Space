import math
import matplotlib.pyplot as plt

from car_park import CarPark


class Pose:
    def __init__(self, x, y, theta):
        self.x = x # x-coordinate of the pose
        self.y = y # y-coordinate of the pose
        self.theta = theta # orientation angle of the pose


class Node:
    def __init__(
            self,
            pose,
            cost,
            steering,
            parent_node_index,
    ):
        self.pose = pose # pose of the node
        self.discrete_x = round(pose.x) # rounded x-coordinate of the node
        self.discrete_y = round(pose.y) # rounded y-coordinate of the node
        self.cost = cost # cost associated with reaching this node
        self.steering = steering # steering angle associated with this node
        self.parent_node_index = parent_node_index # index of the parent node in the closed set


class HybridAStarRoutePlanner:
    def __init__(self, car_park):
        self.car_park: CarPark = car_park # reference to the car park object

        # Motion Model
        self.wheelbase = 2.7  # wheelbase of the vehicle
        steering_degree_inputs = [-40, -20, -10, 0, 10, 20, 40] # possible steering degree inputs
        self.steering_inputs = [math.radians(x) for x in steering_degree_inputs] # convert steering degrees to radians
        self.chord_lengths = [2, 1] # possible chord lengths for motion

        self.goal_node = None  # initialize the goal node as None

    # Function to search for a route using Hybrid A* algorithm
    def search_route(self, start_pose, goal_pose, show_process=True):
        start_node = Node(start_pose, 0, 0, -1) # create a start node
        self.goal_node = Node(goal_pose, 0, 0, -1) # create a goal node

        open_set = {self.car_park.get_grid_index(start_node.discrete_x, start_node.discrete_y): start_node} # nodes to be evaluated
        closed_set = {} # evaluated nodes

        while open_set:
            current_node_index = min(
                open_set,
                key=lambda o: open_set[o].cost + self.calculate_heuristic_cost(open_set[o]),
            )
            current_node = open_set[current_node_index]

            if show_process:
                self.plot_process(current_node, closed_set)

            if self.calculate_distance_to_end(current_node.pose) <= 1:
                print("Find Goal")
                self.goal_node = current_node
                return self.process_route(closed_set)

            # Remove the item from the open set
            del open_set[current_node_index]

            # Add it to the closed set
            closed_set[current_node_index] = current_node

            # Calculate next possible nodes based on motion model
            next_nodes = [
                self.calculate_next_node(
                    current_node, current_node_index, velocity, steering
                )
                for steering in self.steering_inputs
                for velocity in self.chord_lengths
            ]
            for next_node in next_nodes:
                if self.car_park.is_not_crossed_obstacle(
                        (current_node.discrete_x, current_node.discrete_y),
                        (next_node.discrete_x, next_node.discrete_y),
                ):
                    next_node_index = self.car_park.get_grid_index(next_node.discrete_x, next_node.discrete_y)
                    if next_node_index in closed_set:
                        continue

                    if next_node_index not in open_set:
                        open_set[next_node_index] = next_node  # discovered a new node
                    else:
                        if open_set[next_node_index].cost > next_node.cost:
                            # This path is the best until now. record it
                            open_set[next_node_index] = next_node

        print("Cannot find Route")
        return [], []

    
    def process_route(self, closed_set):
        # Initialize lists for x and y coordinates of the path
        rx = [self.goal_node.pose.x] # x-coordinate of the goal node
        ry = [self.goal_node.pose.y] # y-coordinate of the goal node
    
        parent_node = self.goal_node.parent_node_index
        # Iterate until reaching the start node (parent_node_index == -1)
        while parent_node != -1:
            n = closed_set[parent_node] # Get the node from the closed set
            rx.append(n.pose.x) # Append x-coordinate of the node to the path
            ry.append(n.pose.y) # Append y-coordinate of the node to the path
            parent_node = n.parent_node_index
        return rx, ry

    # Function to calculate the next node based on current node, velocity, and steering angle
    def calculate_next_node(self, current, current_node_index, chord_length, steering):
        theta = self.change_radians_range(
            current.pose.theta + chord_length * math.tan(steering) / float(self.wheelbase)
        )
        x = current.pose.x + chord_length * math.cos(theta)
        y = current.pose.y + chord_length * math.sin(theta)

        return Node(
            Pose(x, y, theta),
            current.cost + chord_length,
            steering,
            current_node_index,
        )

    # Function to calculate heuristic cost from current node to goal node
    def calculate_heuristic_cost(self, node):
        distance_cost = self.calculate_distance_to_end(node.pose)
        angle_cost = abs(self.change_radians_range(node.pose.theta - self.goal_node.pose.theta)) * 0.1
        steering_cost = abs(node.steering) * 10

        cost = distance_cost + angle_cost + steering_cost
        return float(cost)

    # Function to calculate Euclidean distance from current pose to goal pose
    def calculate_distance_to_end(self, pose):
        distance = math.sqrt(
            (pose.x - self.goal_node.pose.x) ** 2 + (pose.y - self.goal_node.pose.y) ** 2
        )
        return distance

    # Function to convert radians range from -pi to pi
    @staticmethod
    def change_radians_range(angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    # Function to plot the current process
    @staticmethod
    def plot_process(current_node, closed_set):
        # show graph
        plt.plot(current_node.discrete_x, current_node.discrete_y, "xc") # plot current node
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
    plt.plot(obstacle_x, obstacle_y, ".k") # plot obstacles

    # Define start and goal poses
    start_pose = Pose(14.0, 4.0, math.radians(0))
    goal_pose = Pose(69.0, 59.0, math.radians(90))
    print(f"Start Hybrid A Star Route Planner (start {start_pose.x, start_pose.y}, end {goal_pose.x, goal_pose.y})")

    plt.plot(start_pose.x, start_pose.y, "og")
    plt.plot(goal_pose.x, goal_pose.y, "xb")
    plt.text(start_pose.x, start_pose.y, 'Start', color='green', fontsize=10, ha='right')
    plt.text(goal_pose.x, goal_pose.y, 'Goal', color='blue', fontsize=10, ha='right')
    plt.xlim(-1, car_park.cp_width + 1)
    plt.ylim(-1, car_park.cp_height + 1)
    plt.title("Hybrid A Star Route Planner")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.grid(True)
    plt.axis("equal")

    hybrid_a_star_route_planner = HybridAStarRoutePlanner(car_park)
    rx, ry = hybrid_a_star_route_planner.search_route(start_pose, goal_pose, False)
    plt.plot(rx, ry, "-r")
    plt.pause(0.001)
    plt.show()


if __name__ == "__main__":
    main()
