from game_object import GameObject
from vision import create_marker_info_by_type, MARKER_TOKEN, MARKER_ARENA
from math import pi

import pypybox2d

class Faces:

    def __init__(self, faces):
        # Middle, left, top, right, bottom, below
        # Teams 0, 1, 2, 3, and 4- no team
        self.faces = faces

    def __getitem__(self, number):
        return self.faces[number]
    
    def roll(self, direction):
        replaces = [[1,5,2,0,4,3], [2,1,5,3,0,4], [3,0,2,5,4,1], [4,1,0,3,5,2]]
        # Left, up, right, down
        self.faces = [self.faces[replaces[direction][i]] for i in range(6)]

    def rotate_y(self, direction):
        replaces = [[0,4,1,2,3,5],[0,2,3,4,1,5]]
        # 0 clockwise, 1 anticlockwise
        self.faces = [self.faces[replaces[direction][i]] for i in range(6)]

    def copy(self):
        return Faces(self.faces[:])

class Token(GameObject):
    grabbable = True

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
        if round(_new_heading/(pi/2)) < round(self.heading/(pi/2)):
            pass
        elif round(_new_heading/(pi/2)) > round(self.heading/(pi/2)):
            pass
    
    def __init__(self, arena, number, damping):
        self._body = arena._physics_world.create_body(position=(0, 0),
                                                      angle=0,
                                                      linear_damping=damping,
                                                      angular_damping=damping,
                                                      type=pypybox2d.body.Body.DYNAMIC)
        GameObject.__init__(self, arena)
        self.marker_info = create_marker_info_by_type(MARKER_TOKEN, number)
        self.grabbed = False
        self.face = 0
        WIDTH=0.08
        self.WIDTH = WIDTH
        self._body.create_polygon_fixture([(-WIDTH, -WIDTH),
                                           ( WIDTH, -WIDTH),
                                           ( WIDTH,  WIDTH),
                                           (-WIDTH,  WIDTH)],
                                          density=1,
                                          restitution=0.2,
                                          friction=0.3)

    def grab(self):
        self.grabbed = True

    def rotate(self, direction):
        self.faces.roll(direction)
        self.face = self.faces[0]

    def release(self):
        self.grabbed = False

    @property
    def surface_name(self):
        return 'sr/'+str(self.face%6)+'.png'

class WallMarker(GameObject):
    surface_name = 'sr/wall_marker.png'

    def __init__(self, arena, number, location=(0,0), heading=0):
        GameObject.__init__(self, arena)
        self.marker_info = create_marker_info_by_type(MARKER_ARENA, number)
        self.location = location
        self.heading = heading

