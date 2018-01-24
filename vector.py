import math


# Vector class holds two variables - x and y, and is used to represent 2D vectors
class Vector:
    def __init__(self, x, y = None):
        if y is None:
            self.x = x
            self.y = x
        else:
            self.x = x
            self.y = y

    def rotate(self, deg):
        # Rotate vector around origin
        x1 = self.x * math.cos(deg) - self.y * math.sin(deg)
        y1 = self.x * math.sin(deg) + self.y * math.cos(deg)
        return Vector(x1, y1)

    def to_tuple(self):
        # Convert the vector into tuple
        return self.x, self.y

    def add(self, vec):
        # Add another vector to this vector
        self.x += vec.x
        self.y += vec.y

        return self

    def add_new(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def multiply(self, vec):
        # Multiply this vector with another vector
        self.x *= vec.x
        self.y *= vec.y

        return self

    def multiply_new(self, vec):
        return Vector(self.x * vec.x, self.y * vec.y)

    def divide(self, vec):
        # Divide this vector with another vector
        self.x /= vec.x
        self.y /= vec.y

        return self

    def divide_new(self, vec):
        return Vector(self.x / vec.x, self.y / vec.y)

    def flip(self):
        # Flip this vector (multiply coordinates by -1)
        self.x *= -1
        self.y *= -1

        return self

    def flip_new(self):
        return Vector(self.x * -1, self.y * -1)

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_normalized(self):
        magnitude = self.get_magnitude()

        if magnitude == 0:
            return Vector(0)
        return Vector(self.x / magnitude, self.y / magnitude)
