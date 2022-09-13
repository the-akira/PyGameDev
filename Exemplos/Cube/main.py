from dataclasses import dataclass
from operator import itemgetter
import sys, math, pygame

# Code reference: https://github.com/codentronix

@dataclass
class Face:
    x: int 
    y: int
    z: int
    w: int

class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotate_x(self, angle):
        """ 
        Rotates the point around the X axis by the given angle in degrees.
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotate_y(self, angle):
        """ 
        Rotates the point around the Y axis by the given angle in degrees.
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotate_z(self, angle):
        """ 
        Rotates the point around the Z axis by the given angle in degrees.
        """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, width, height, field_of_view, viewer_distance):
        """ 
        Transforms this 3D point to 2D using a perspective projection.
        """
        factor = field_of_view / (viewer_distance + self.z)
        x = self.x * factor + width / 2
        y = -self.y * factor + height / 2
        return Point3D(x, y, self.z)

class Simulation:
    def __init__(self, width=640, height=480):
        pygame.init()
        pygame.display.set_caption("Rotating Cube Simulation")
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]
        # Define the vertices that compose each of the 6 faces. 
        # These numbers are indices to the vertices list defined above.
        self.faces  = [
            Face(0,1,2,3),
            Face(1,5,6,2),
            Face(5,4,7,6),
            Face(4,0,3,7),
            Face(0,4,5,1),
            Face(3,2,6,7),
        ]
        # Define colors for each face and the angle.
        self.colors = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]
        self.angle = 0

    def run(self):
        # Main Loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill((20,20,20))

            # t will hold transformed vertices.
            t = []
            for v in self.vertices:
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                r = v.rotate_x(self.angle).rotate_y(self.angle).rotate_z(self.angle)
                # Transform the point from 3D to 2D.
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                # Put the point in the list of transformed vertices.
                t.append(p)

            # Calculate the average Z values of each face.
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f.x].z + t[f.y].z + t[f.z].z + t[f.w].z) / 4.0
                avg_z.append([i,z])
                i += 1

            # Draw the faces using the Painter's Algorithm:
            # Distant faces are drawn before the closer ones.
            for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                point_list = [(t[f.x].x, t[f.x].y), (t[f.y].x, t[f.y].y),
                             (t[f.y].x, t[f.y].y), (t[f.z].x, t[f.z].y),
                             (t[f.z].x, t[f.z].y), (t[f.w].x, t[f.w].y),
                             (t[f.w].x, t[f.w].y), (t[f.x].x, t[f.x].y)]
                pygame.draw.polygon(self.screen, self.colors[face_index], point_list)

            self.angle += 1
            pygame.display.flip()

if __name__ == "__main__":
    Simulation().run()