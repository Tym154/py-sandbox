from particle_class import Particle
from particle_types import PARTICLE_TYPES

class Grid:
    def __init__(self, height, width, particle_scale):
        self.height = height // particle_scale
        self.width = width // particle_scale
        self.contents = [[0 for i in range(self.height)] for j in range(self.width)]

    def update_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                self.contents

    def add_particle(self, x_cord, y_cord, particle_type):
        if self.contents != 0:
            return
        
        p_parameters = PARTICLE_TYPES[particle_type]

        self.contents[x_cord][y_cord] = Particle(p_parameters['color'], 'weight', 0, 0, particle_type)