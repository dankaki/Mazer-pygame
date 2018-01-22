import pygame
import math
screen = pygame.display.set_mode((400, 300))

# Constant values that are used to convert degrees into radians and vice-versa
deg2rad = math.pi / 180
rad2deg = 1.0 / deg2rad

deltaTime = 0
# Vector class holds two variables - x and y, and is used to represent 2D vectors
class Vector:
    def __init__(self, x, y):
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

    def multiply(self, vec):
        # Multiply this vector with another vector
        self.x *= vec.x
        self.y *= vec.y

    def divide(self, vec):
        # Divide this vector with another vector
        self.x /= vec.x
        self.y /= vec.y

    def flip(self):
        # Flip this vector (multiply coordinates by -1)
        self.x *= -1
        self.y *= -1

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_normalized(self):
        magnitude = self.get_magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)


# Tank class is used to simplify some things
class Tank:

    # color - What color should the tank be
    # key_tuple - Keys used to move the tank
    #   [forward, backward, left, right, shoot]
    # width, height - Dimensions of tank
    # def_rotation, def_position - Default position and default rotation of tank
    # acceleration - Value of acceleration that is used to move (forward or backward)
    # turn_acceleration - Acceleration that is used to turn (left or right)
    # max_speed - Maximum magnitude (length) of velocity vector
    # drag - Value that is used to slow down linear movement
    # angular_drag - Value that is used to slow down rotational movement
    # cannon_length - Length of cannon

    def __init__(self, color, key_tuple, width, height, def_rotation, def_position,
                 acceleration, turn_acceleration, max_speed, drag, angular_drag, cannon_length):
        self.color = color
        self.key_tuple = key_tuple
        self.width = width
        self.height = height
        self.cannon_length = cannon_length
        self.rotation = def_rotation
        self.position = def_position
        self.velocity = Vector(0, 0)

    def update(self):
        keyPressed = pygame.key.get_pressed()
        




    def add_position(self, vec):
        self.position += vec

    def add_rotation(self, val):
        # Add value to current rotation and normalize the angle
        self.rotation += val
        self.rotation %= 360

        if self.rotation < 0:
            self.rotation += 360

    def get_vertices(self):
        # Calculate half of width and half of height used to simplify further processes
        half_width = self.width / 2
        half_height = self.height / 2

        # Some math used to rotate square around its center
        point1 = Vector(-half_width, half_height).rotate(self.rotation * deg2rad)
        point2 = Vector(half_width, half_height).rotate(self.rotation * deg2rad)
        point3 = Vector(half_width, -half_height).rotate(self.rotation * deg2rad)
        point4 = Vector(-half_width, -half_height).rotate(self.rotation * deg2rad)

        # Add back our position
        point1.add(self.position)
        point2.add(self.position)
        point3.add(self.position)
        point4.add(self.position)

        # Convert vectors into array of tuples (positions)
        return [point1.to_tuple(), point2.to_tuple(), point3.to_tuple(), point4.to_tuple()]

    def draw(self):
        # Draw polygon
        pygame.draw.polygon(screen, self.color, self.get_vertices(), 0)


# Initialize PyGame
pygame.init()
DONE = False

# Configure tanks
tank1 = Tank((255, 255, 255), (), 100, 100, 0, Vector(200, 200), 50)

# Previous frame tick - variable that is used to calculate deltaTime :
#   DeltaTime is amount of milliseconds between rendering current frame and previous frame
#   It can be used to simulate physics easily
previousFrameTick = pygame.time.get_ticks()

# Loop while user did not exit the program
while not DONE:
    # Loop through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # If user closed the game - quit
            DONE = True

    # Calculate deltaTime
    deltaTime = (pygame.time.get_ticks() - previousFrameTick) / 1000.0
    previousFrameTick = pygame.time.get_ticks()

    # Clear the screen
    screen.fill((0, 0, 0))

    # User-defined code
    tank1.add_rotation(-360 * deltaTime)
    tank1.draw()

    # Update screen
    pygame.display.update()
