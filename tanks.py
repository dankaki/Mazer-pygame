import pygame
import math
import os
import vector as vmath

screen = pygame.display.set_mode((400, 300))

# Constant values that are used to convert degrees into radians and vice-versa
deg2rad = math.pi / 180
rad2deg = 1.0 / deg2rad

delta_time = 0

friction_coefficient = 2.0
gravity_coefficient = -9.81


def get_sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    return 0


def clamp_zero(num):
    if num > 0:
        return num
    return 0.0


def lerp(start, end, factor):
    return (1 - factor) * start + factor * end;


# Tank class is used to simplify some things
class Tank:

    # mass - Mass of tank
    # color - What color should the tank be
    # key_tuple - Keys used to move the tank
    #   [forward, backward, left, right, shoot]
    # width, height - Dimensions of tank
    # def_rotation, def_position - Default position and default rotation of tank
    # force - Value of force that is used to move (forward or backward)
    # turn_torque - Torque that is used to turn (left or right)
    # max_velocity - Maximum magnitude (length) of velocity vector
    # drag - Value that is used to slow down linear movement
    # angular_drag - Value that is used to slow down rotational movement
    # cannon_length - Length of cannon

    def __init__(self, mass, color, key_tuple, width, height, def_rotation, def_position, cannon_width, cannon_length,
                 movement_force, turn_torque, max_velocity):
        self.mass = mass
        self.color = color
        self.key_tuple = key_tuple
        self.width = width
        self.height = height
        self.cannon_length = cannon_length
        self.cannon_width = cannon_width
        self.rotation = def_rotation
        self.position = def_position
        self.movement_force = movement_force
        self.turn_torque = turn_torque
        self.max_velocity = max_velocity

        self.force = vmath.Vector(0)
        self.acceleration = vmath.Vector(0)
        self.velocity = vmath.Vector(0)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[self.key_tuple[1]]:
            self.force.y = self.movement_force
        elif key_pressed[self.key_tuple[0]]:
            self.force.y = -self.movement_force
        else:
            self.force.y = 0

        if key_pressed[self.key_tuple[3]]:
            self.add_rotation(-self.turn_torque * delta_time)
        elif key_pressed[self.key_tuple[2]]:
            self.add_rotation(self.turn_torque * delta_time)

        self.force.add(self.velocity.get_normalized()
                       .multiply(vmath.Vector(self.mass * gravity_coefficient * friction_coefficient)))

        self.acceleration = self.force.divide_new(vmath.Vector(self.mass))

        self.velocity.add(self.acceleration.multiply(vmath.Vector(delta_time)))

        if self.velocity.get_magnitude() > self.max_velocity:
            self.velocity = self.velocity.get_normalized().multiply(vmath.Vector(self.max_velocity))

        self.position.add(self.velocity.multiply_new(vmath.Vector(delta_time)).rotate(self.rotation * deg2rad))

        self.draw()

    def add_position(self, vec):
        self.position.add(vec)

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
        point1 = vmath.Vector(-half_width, half_height).rotate(self.rotation * deg2rad)
        point2 = vmath.Vector(half_width, half_height).rotate(self.rotation * deg2rad)
        point3 = vmath.Vector(half_width, -half_height).rotate(self.rotation * deg2rad)
        point4 = vmath.Vector(-half_width, -half_height).rotate(self.rotation * deg2rad)

        # Add back our position
        point1.add(self.position)
        point2.add(self.position)
        point3.add(self.position)
        point4.add(self.position)

        # Convert vectors into array of tuples (positions)
        return [point1.to_tuple(), point2.to_tuple(), point3.to_tuple(), point4.to_tuple()]

    def get_vertices_cannon(self):
        # Calculate half of width and half of height used to simplify further processes
        half_width = self.cannon_width / 2
        half_height = self.cannon_length / 2

        # Some math used to rotate square around its center
        point1 = vmath.Vector(-half_width, 0).rotate(self.rotation * deg2rad)
        point2 = vmath.Vector(half_width, 0).rotate(self.rotation * deg2rad)
        point3 = vmath.Vector(half_width, -self.cannon_length).rotate(self.rotation * deg2rad)
        point4 = vmath.Vector(-half_width, -self.cannon_length).rotate(self.rotation * deg2rad)

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
        pygame.draw.polygon(screen, (255, 255, 255), self.get_vertices_cannon(), 0)


# Initialize PyGame
pygame.init()
DONE = False

mass = 10
color = (255, 0, 0)
width = 50
height = 80
wasd_key_tuple = (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_f)
acceleration = 10
turn_acceleration = 10.0
drag = 10.0
angular_drag = 10.0

max_speed = 1000
cannon_width = 15
cannon_length = 75

# Configure tanks
tank1 = Tank(mass, color, wasd_key_tuple, width, height, 0, vmath.Vector(100),
             cannon_width, cannon_length, 1000, 100, 100)

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
    delta_time = (pygame.time.get_ticks() - previousFrameTick) / 1000.0
    previousFrameTick = pygame.time.get_ticks()

    # Clear the screen
    screen.fill((0, 0, 0))

    # User-defined code
    tank1.update()

    # Update screen
    pygame.display.update()
