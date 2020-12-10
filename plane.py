import pygame as pg

from os.path import join


_plane_path = join("assets", "free_plane_sprite", "png", "Plane")
_plane_scale = 125


class Plane(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.flying_images = [pg.transform.flip( # Load all images as list comprehensions
                              pg.transform.scale(pg.image.load(
                                  join(_plane_path, "Fly (" + str(i) + ").png")), (_plane_scale, _plane_scale)), True, False) for i in range(1, 3)]

        self.dead_image = pg.transform.flip(
            pg.transform.scale(pg.image.load(
                join(_plane_path, "Dead (1).png")), (_plane_scale, _plane_scale)), True, False)

        self.is_alive = True
        self.index = 0
        self.flying_image = self.flying_images[self.index]
        self.rect = self.flying_image.get_rect()

    def animate(self) -> None:

        if self.is_alive:

            if self.index == len(self.flying_images):
                self.index = 0

            self.flying_image = self.flying_images[self.index]
            self.index += 1
            return

        self.flying_image = self.dead_image # Overwrite with the dead image

    def set_position(self, x, y) -> None:

        # Change my rectangle

        self.rect.x = x
        self.rect.y = y

    def check_collision(self, object_) -> bool:
        return self.rect.colliderect(object_.rect)
