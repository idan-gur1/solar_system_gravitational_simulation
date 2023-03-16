import math

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
VENUS_COLOR = (100, 70, 70)
BLUE = (100, 149, 237)
GRAY = (128, 128, 128)
RED = (255, 50, 50)

FONT = pygame.font.SysFont("comicsans", 20)


G = 6.67428e-11
SCALE = 200 / 150e9  # 200 pixels is 150e9 meters
TIME_STEP = 3600 * 24


class Planet:
    planets = []

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win, i):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{self.name} - " + "{:.2e}".format(self.distance_to_sun) + f" - {round(self.distance_to_sun, 1)}m", True, self.color)
            win.blit(distance_text, (5, i * distance_text.get_height() * 2))

    def calc_force(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.calc_force(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * TIME_STEP
        self.y_vel += total_fy / self.mass * TIME_STEP

        self.x += self.x_vel * TIME_STEP
        self.y += self.y_vel * TIME_STEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892e30, "sun")
    sun.sun = True

    mercury = Planet(-1 * 58e9, 0, 8, GRAY, 3.285e23, "mercury")
    mercury.y_vel = 47362.5

    venus = Planet(-1 * 100e9, 0, 14, VENUS_COLOR, 4.867e24, "venus")
    venus.y_vel = 35021.39

    earth = Planet(-1 * 149.6e9, 0, 16, BLUE, 5.974e24, "earth")
    earth.y_vel = 29806

    mars = Planet(-1 * 227.9e9, 0, 12, RED, 0.642e24, "mars")
    mars.y_vel = 24100

    planets = [sun, mercury, venus, earth, mars]

    t = 0

    while run:
        dt = clock.tick(60)
        t += dt
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for i, planet in enumerate(planets):
            planet.update_position(planets)
            planet.draw(WIN, i)

        if t > 6000:
            for p in planets:
                p.orbit.clear()
            t = 0

        pygame.display.update()

    pygame.quit()


main()
