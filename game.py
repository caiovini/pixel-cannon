import pygame as pg
import sys
import math
import random

from assets import (Background,
                    Ground,
                    CannonBase,
                    Cannon,
                    Ball)

from plane import Plane
from os.path import join

sprite_width, sprite_height = 0, 1
clock = pg.time.Clock()
plane_sign = u'\u2708'  # Unicode for plane

SCREEN_WIDTH, SCREEN_HEIGHT = 854, 480
BROWN = pg.Color(40, 26, 14)
YELLOW = pg.Color(255, 255, 0)
BLACK = pg.Color(0, 0, 0)


def main():
    pg.init()  # Init pygame
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Pixel cannon")
    font_msg = pg.font.SysFont("Comic Sans MS", 20)
    font_plane = pg.font.Font(join("fonts", "segoe-ui-symbol.ttf"), 20)

    alpha_bg = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    alpha_bg.set_alpha(128)
    alpha_bg.fill((BLACK))

    background = Background()
    ground = Ground()
    cannon_base = CannonBase()
    cannon = Cannon()
    ball = Ball()
    plane = Plane()

    cannon_base.set_position(100, SCREEN_HEIGHT - (ground.image.get_rect()
                                                   .size[sprite_height] + cannon_base.image.get_rect().size[sprite_height]))

    cannon.set_position(115, cannon_base.rect.y -
                        cannon_base.image.get_rect().size[sprite_height] / 1.8)

    def build_ground():
        # Build ground according to the size of screen width
        for i in range(math.ceil(SCREEN_WIDTH / ground.image.get_rect().size[sprite_width])):
            ground.set_position(
                i * ground.image.get_rect().size[sprite_width], SCREEN_HEIGHT - ground.image.get_rect().size[sprite_height])
            screen.blit(ground.image, ground.rect)

    planes_missed = plane_speed = 8
    game_over = fly_airplane = is_shooting = done = False
    score = plane_altitude = x_ball = y_ball = speed_ball = 0
    plane_position_x = SCREEN_WIDTH + \
        plane.flying_image.get_rect(
        ).size[sprite_width]  # Initial position for the plane
    while not done:

        if not fly_airplane:
            plane_altitude = random.randrange(0, 5000)
            if 0 < plane_altitude < 100:  # Randomically generates planes
                fly_airplane = True

        screen.blit(background.image, background.rect)
        screen.blit(cannon_base.image, cannon_base.rect)

        # Shooting validation
        if not cannon.check_collision(ball) and not game_over:
            keys = pg.key.get_pressed()

            if keys[pg.K_LEFT]:
                if cannon.angle < 90:
                    cannon.rotate(1)

            if keys[pg.K_RIGHT]:
                if cannon.angle > 0:
                    cannon.rotate(-1)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                done = True

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    done = True

                if event.key == pg.K_SPACE and not is_shooting and not game_over:

                    ball.angle = cannon.angle
                    is_shooting = True

        if is_shooting:

            # Only allow shooting when ball is out of screen boundaries
            if x_ball > SCREEN_WIDTH or y_ball < -ball.image.get_rect().size[sprite_height]:
                is_shooting = False
                x_ball = y_ball = speed_ball = 0
                ball.set_initial_position()

            else:
                speed_ball += 10
                x_ball: float = cannon.rect.x + cannon_base.image.get_rect().size[sprite_height] / 4 + \
                    math.cos(math.radians(360 - ball.angle)) * speed_ball

                y_ball: float = cannon.rect.y + cannon_base.image.get_rect().size[sprite_height] / 4 + \
                    math.sin(math.radians(360 - ball.angle)) * speed_ball

                ball.set_position(x_ball, y_ball)
                screen.blit(ball.image, ball.rect)

        screen.blit(cannon.rotate_image, cannon.rotate_image.get_rect(center=cannon.image.get_rect
                                                                      (topleft=(cannon.rect.x - cannon.angle/2, cannon.rect.y - cannon.angle/2)).center).topleft)

        if fly_airplane:
            plane.set_position(plane_position_x, plane_altitude)
            plane.animate()
            screen.blit(plane.flying_image, plane.rect)
            plane_position_x -= plane_speed

            if not plane.is_alive:  # If hit, lose altitude
                plane_altitude += 2

            if plane.check_collision(ball):
                ball.set_initial_position()
                is_shooting = False
                x_ball = y_ball = speed_ball = 0
                plane.is_alive = False
                score += plane_position_x / 100

            if plane_position_x < -plane.flying_image.get_rect().size[sprite_width]:
                if not plane.is_alive:
                    plane_speed += .1
                else:
                    if planes_missed > 0:
                        planes_missed -= 1
                        if planes_missed == 0:
                            game_over = True

                fly_airplane = False
                plane.is_alive = True

                plane_position_x = SCREEN_WIDTH + \
                    plane.flying_image.get_rect().size[sprite_width]

        label = font_msg.render(f"SCORE: {score:.2f}", 1, BROWN)
        screen.blit(label, (10, 0))

        label = font_plane.render(
            plane_sign * planes_missed, 1, BROWN)
        screen.blit(label, (SCREEN_WIDTH / 2.5, 0))

        build_ground()
        if game_over:
            screen.blit(alpha_bg, (0, 0))
            label = font_msg.render(
                "GAME OVER", 1, YELLOW)
            screen.blit(label, (SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5))

        pg.display.flip()
        clock.tick(60)  # FPS


if __name__ == '__main__':
    sys.exit(main())
