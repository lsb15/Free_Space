import matplotlib.pyplot as plt

class CarPark:
    def __init__(self):
        self.cp_width: int = 82
        self.cp_height: int = 63

        self.obstacles = []
        self.obstacle_lines = []

        # Defining obstacles
        for x in range(self.cp_width + 1):
            self.obstacles.append((x, 0))
            self.obstacles.append((x, self.cp_height))
        for y in range(1, self.cp_height):
            self.obstacles.append((0, y))
            self.obstacles.append((self.cp_width, y))
        self.obstacle_lines = [
            [(0, 0), (0, self.cp_height)],
            [(0, 0), (self.cp_width, 0)],
            [(self.cp_width, 0), (self.cp_width, self.cp_height)],
            [(0, self.cp_height), (self.cp_width, self.cp_height)],
        ]

        # Defining horizontal lines
        for x in range(11, self.cp_width - 10):
            self.obstacles.append((x, 17))
            self.obstacles.append((x, 40))
        self.obstacle_lines.append([(11, 17), (self.cp_width - 10, 17)])
        self.obstacle_lines.append([(11, 40), (self.cp_width - 10, 40)])

        # Defining vertical lines
        for x in range(16):
            for y in range(6):
                self.obstacles.append((x * 4 + 11, y + 11))
                self.obstacles.append((x * 4 + 11, y + 18))
                self.obstacles.append((x * 4 + 11, y + 34))
                self.obstacles.append((x * 4 + 11, y + 41))
                self.obstacles.append((x * 4 + 11, y + 57))
            self.obstacle_lines.append([(x * 4 + 11, 11), (x * 4 + 11, 24)])
            self.obstacle_lines.append([(x * 4 + 11, 34), (x * 4 + 11, 47)])
            self.obstacle_lines.append([(x * 4 + 11, 57), (x * 4 + 11, 63)])

    def get_grid_index(self, x, y):
        return x + y * self.cp_width

    def is_not_crossed_obstacle(self, previous_node, current_node):
        is_cross_line = any(
            [
                self.intersect(obstacle_line, [previous_node, current_node])
                for obstacle_line in self.obstacle_lines
            ]
        )
        return (
                current_node not in set(self.obstacles)
                and 0 < current_node[0] < self.cp_width
                and 0 < current_node[1] < self.cp_height
                and not is_cross_line
        )

    def intersect(self, line1, line2):
        A = line1[0]
        B = line1[1]
        C = line2[0]
        D = line2[1]
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def ccw(self, A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    def plot_car_park(self):
        fig, ax = plt.subplots()

        # Plotting obstacles
        for line in self.obstacle_lines:
            ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 'k-')

        ax.set_xlim(-1, self.cp_width + 1)
        ax.set_ylim(-1, self.cp_height + 1)
        ax.set_title("Car Park")
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
        ax.grid(True)
        ax.axis("equal")
        plt.show()

if __name__ == "__main__":
    Car_Park = CarPark()
    Car_Park.plot_car_park()
