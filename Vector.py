import math


class Vec:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def of(tuplee):
        return Vec(tuplee[0], tuplee[1])

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x + other.x, self.y + other.y)
        else:
            raise ValueError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x - other.x, self.y - other.y)
        else:
            raise ValueError("Unsupported operand type for -")

    def __mul__(self, scalar):
        return Vec(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vec(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vec(0, 0)
        else:
            return self / mag

    def distance(self, other):
        """Calculate the Euclidean distance between two points."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)


    def rotate(self, angle_degrees):
        # Convert angle from degrees to radians
        angle_radians = math.radians(angle_degrees)

        # Extract coordinates
        x, y = self.x, self.y

        # Apply rotation matrix
        x_prime = x * math.cos(angle_radians) - y * math.sin(angle_radians)
        y_prime = x * math.sin(angle_radians) + y * math.cos(angle_radians)

        # Return the rotated vector
        return Vec(x_prime, y_prime)

    def tuple(self):
        return (self.x, self.y)

UP = Vec(0, 1)
ZERO = Vec(0, 0)


