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
        while round(self._body.angle/(pi/2)) < round(self.oldHeading/(pi/2)):
            self.faces.rotate_y(1)
            self.oldHeading += pi/2
            print "1current heading:", self._body.angle, ", old heading:", self.oldHeading
        while round(self._body.angle/(pi/2)) > round(self.oldHeading/(pi/2)):
            self.faces.rotate_y(0)
            self.oldHeading -= pi/2
            print "current heading:", self._body.angle, ", old heading:", self.oldHeading
        self.oldHeading = self._body.angle
        return self._body.angle

    @heading.setter
    def heading(self, _new_heading):
        if self._body is None:
            return # Slight hack: deal with the initial setting from the constructor
        self._body.angle = _new_heading
    
    def __init__(self, arena, number, damping):
        self.faces = None
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
        self.oldHeading = self._body.angle

    def grab(self, robot):
        if robot != None:
            self._body.angle = round(self._body.angle/(pi/2))*pi/2
            self.origHeading = self._body.angle
            robot_heading = round(robot.heading/(pi/2))+1
            #print (robot_heading-self._body.angle/(pi/2))
            for i in range(int(robot_heading-self._body.angle/(pi/2))%4):
                self.faces.rotate_y(0)
        self.grabbed = True

    def rotate(self, direction):
        if self.faces != None:
            if direction < 4:
                self.faces.roll(direction)
            else:
                self.heading = self.heading + pi/2
            self.face = self.faces[0]
        else:
            raise Exception("No. Not this game")

    def release(self, robot):
        if robot != None:
            self._body.angle = round(self._body.angle/(pi/2))*pi/2
            origHeading = round(self.origHeading/(pi/2))+1
            #print (origHeading-self._body.angle/(pi/2))
            for i in range(int(origHeading-self._body.angle/(pi/2))%4):
                self.faces.rotate_y(0)
        self.grabbed = False

    @property
    def surface_name(self):
        if self.faces != None:
            return 'sr/'+str(self.face%6)+'.png'
        else:
            return 'sr/token{0}.png'.format('_grabbed' if self.grabbed else '')

class WallMarker(GameObject):
    surface_name = 'sr/wall_marker.png'

    def __init__(self, arena, number, location=(0,0), heading=0):
        GameObject.__init__(self, arena)
        self.marker_info = create_marker_info_by_type(MARKER_ARENA, number)
        self.location = location
        self.heading = heading

