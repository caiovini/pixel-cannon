import pygame as pg

from os.path import join

_back_ground_path = join("assets", "cannon-ball", "PNG", "background.png")
_ground_path = join("assets", "cannon-ball", "PNG", "ground.png")
_cannon_base_path = join("assets", "cannon-ball", "PNG", "cannon2.png")
_cannon_path = join("assets", "cannon-ball", "PNG", "cannon.png")
_ball_path = join("assets", "cannon-ball", "PNG", "ball.png")


class Base(pg.sprite.Sprite):

    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

    def set_position(self, x, y) -> None:

        # Change my rectangle

        self.rect.x = x
        self.rect.y = y


class Background(Base):

    def __init__(self):
        image = pg.image.load(_back_ground_path).convert_alpha()
        Base.__init__(self, image)


class Ground(Base):

    def __init__(self):
        image = pg.image.load(_ground_path).convert_alpha()
        Base.__init__(self, image)


class CannonBase(Base):

    def __init__(self):
        image = pg.image.load(_cannon_base_path).convert_alpha()
        Base.__init__(self, image)


class Cannon(Base):

    def __init__(self):
        image = pg.image.load(_cannon_path).convert_alpha()
        self.rotate_image = image
        self.angle = 0
        Base.__init__(self, image)

    def rotate(self, angle):

        self.angle += angle
        orig_rect = self.image.get_rect()
        rot_image = pg.transform.rotate(self.image, self.angle)
        self.rotate_image = rot_image

    def check_collision(self, object_):
        return self.rect.colliderect(object_.rect)


class Ball(Base):

    def __init__(self):
        image = pg.image.load(_ball_path).convert_alpha()
        self.angle = 0
        Base.__init__(self, image)

        self.set_initial_position()

    def set_initial_position(self):
        self.set_position(-self.image.get_rect().size[0] * 10,
                          -self.image.get_rect().size[1] * 10)
