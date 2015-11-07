from __future__ import division

import pygame
from random import random
from math import pi

from arena import Arena, ARENA_MARKINGS_COLOR, ARENA_MARKINGS_WIDTH
from ..markers import Token, Faces
from ..game_object import GameObject

import pypybox2d

class CTFWall(GameObject):
    @property
    def location(self):
        return self._body.position

    @location.setter
    def location(self, new_pos):
        if self._body is None:
            return # Slight hack: deal with the initial setting from the constructor
        self._body.position = new_pos

    @property
    def heading(self):
        return self._body.angle

    @heading.setter
    def heading(self, _new_heading):
        if self._body is None:
            return # Slight hack: deal with the initial setting from the constructor
        self._body.angle = _new_heading

    def __init__(self, arena):
        self._body = arena._physics_world.create_body(position=(0, 0),
                                                      angle=0,
                                                      type=pypybox2d.body.Body.STATIC)
        self._body.create_polygon_fixture([(-0.75, -0.15),
                                           ( 0.75, -0.15),
                                           ( 0.75,  0.15),
                                           (-0.75,  0.15)],
                                          restitution=0.2,
                                          friction=0.3)
        super(CTFWall, self).__init__(arena)

    surface_name = 'sr/wall.png'

class LiamArena(Arena):
    team_colours = [[255,165,0],[255,242,0],[237,28,36],[63,72,204]]
    default_colour = [195,195,195]
    
    start_locations = [(-3.6, -3.6),
                       ( 3.6, -3.6),
                       ( 3.6,  3.6),
                       (-3.6,  3.6)]

    start_headings = [0.25*pi,
                      0.75*pi,
                      -0.75*pi,
                      -0.25*pi]

    def __init__(self, objects=None, wall_markers=True, zone_flags=True):
        super(LiamArena, self).__init__(objects, wall_markers)
        #self._init_walls()
        self._init_tokens(zone_flags)

        self.images = None


    def _init_tokens(self, zone_flags):
        if zone_flags:
            token_locations = []
            for x in [-1.5, 0, 1.5]:
                for y in [-1.5, 0, 1.5]:
                    token_locations.append((x, y))
        else:
            token_locations = [(0, 0)]

        for i, location in enumerate(token_locations):
            token = Token(self, i, damping=0.5)
            if  i == 0 :
                token.faces = Faces([2,1,5,3,0,4])
            elif i == 6 :
                token.faces = Faces([3,0,2,5,4,1])
            elif i == 8 :
                token.faces = Faces([4,1,0,3,5,2])
            elif i == 2 :
                token.faces = Faces([5,3,2,1,4,0])
            else:
                token.faces = Faces([0,1,2,3,4,4])
            token.face = token.faces[0]
            
            token.location = location
            token.heading = 0
            self.objects.append(token)

    def _init_walls(self):
        wall_settings = [(-2.25, 0, 0),
                         (2.25, 0, 0),
                         (0, 2.25, pi/2),
                         (0, -2.25, pi/2)]
        for x, y, rotation in wall_settings:
            wall = CTFWall(self)
            wall.location = (x, y)
            wall.heading = rotation
            self.objects.append(wall)

    def draw_background(self, surface, display):
        super(LiamArena, self).draw_background(surface, display)

        def line(start, end):
            pygame.draw.line(surface, ARENA_MARKINGS_COLOR,
                             display.to_pixel_coord(start), display.to_pixel_coord(end),
                             ARENA_MARKINGS_WIDTH)

        def line_symmetric(start, end):
            start_x, start_y = start
            end_x, end_y = end
            line((start_x, start_y), (end_x, end_y))
            line((-start_x, start_y), (-end_x, end_y))
            line((-start_x, -start_y), (-end_x, -end_y))
            line((start_x, -start_y), (end_x, -end_y))
            line((start_y, start_x), (end_y, end_x))
            line((-start_y, start_x), (-end_y, end_x))
            line((-start_y, -start_x), (-end_y, -end_x))
            line((start_y, -start_x), (end_y, -end_x))

        if self.images == None:
            images = [pygame.image.load(r"sr/"+str(name+2)+"b.png").convert() for name in range(4)]
            self.images = [pygame.transform.scale(picture, (picture.get_rect().width*5, picture.get_rect().height*5)) for picture in images]

        surface.blit(self.images[0], self.images[0].get_rect())
        surface.blit(self.images[1], self.images[1].get_rect().move(surface.get_width()-images[1].get_width()*5, 0))
        surface.blit(self.images[2], self.images[2].get_rect().move(surface.get_width()-images[2].get_width()*5, surface.get_height()-images[2].get_height()*5))
        surface.blit(self.images[3], self.images[3].get_rect().move(0, surface.get_height()-images[3].get_height()*5))

        line_symmetric((2, 4), (3, 3))
        """line_symmetric((3, 0.15), (4, 0.15))
        line_symmetric((1.5, 0.15), (0.825, 0.825))"""

