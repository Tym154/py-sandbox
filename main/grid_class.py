from particle_class import Particle
from particle_types import PARTICLE_TYPES
import random
import math


class Grid:
    def __init__(self, height, width, particle_scale, gravity_acceleration, void_density):
        self.height = height // particle_scale
        self.width = width // particle_scale
        self.contents = [[0 for i in range(self.height)] for j in range(self.width)]
        self.gravity_acceleration = gravity_acceleration
        self.void_density = void_density

    def add_particle(self, x_cord, y_cord, particle_type):
        if self.contents[x_cord][y_cord] != 0:
            return
        
        p_parameters = PARTICLE_TYPES[particle_type]

        self.contents[x_cord][y_cord] = Particle(p_parameters['color'], p_parameters['density'], 0, 0, particle_type)

    def update_grid(self):
        updated_coords = [[0 for i in range(self.height)] for j in range(self.width)]

        for x in range(self.width-1, -1, -1):
            for y in range(self.height-1, -1, -1):
                particle = self.contents[x][y]

                if updated_coords[x][y]:
                    continue
                elif not particle:
                    continue
                elif not PARTICLE_TYPES[particle.p_type]['movable']:
                    continue


                if PARTICLE_TYPES[particle.p_type]['type'] == 'loose':
                    new_x, new_y = self.loose_movement(particle, x, y)
                    updated_coords[x][y] = 0
                    updated_coords[new_x][new_y] = 1

                elif PARTICLE_TYPES[particle.p_type]['type'] == 'liquid' or 'gas':
                    new_x, new_y = self.liquid_movement(particle, x, y)
                    updated_coords[x][y] = 0
                    updated_coords[new_x][new_y] = 1


    

    def loose_movement(self, particle, x_cord, y_cord):
        max_fall_speed = math.sqrt((2* particle.density * 1 * self.gravity_acceleration) / (self.void_density * 1 * 1))

        particle.velocity_y += particle.density * self.gravity_acceleration

        if particle.velocity_y > max_fall_speed: particle.velocity_y = max_fall_speed

        fall_steps = int(particle.velocity_y)

        current_x, current_y = x_cord, y_cord

        for i in range(fall_steps):
            if current_y + 1 >= self.height:
                break

            if self.contents[current_x][current_y + 1] == 0 or self.contents[current_x][current_y + 1].density < particle.density:
                self.swap_particles(current_x, current_y, current_x, current_y + 1)
                current_y += 1
            else:
                offsets = [-1, 1]
                random.shuffle(offsets)
                moved = False

                for offset in offsets:
                    new_x = current_x + offset
                    if 0 <= new_x < self.width and current_y + 1 < self.height:
                        if self.contents[new_x][current_y + 1] == 0 or self.contents[new_x][current_y + 1].density < particle.density:
                            self.swap_particles(current_x, current_y, new_x, current_y + 1)
                            current_x, current_y = new_x, current_y + 1
                            moved = True
                            break
                if not moved:
                    break

        return current_x, current_y

    def liquid_movement(self, particle, x_cord, y_cord):
        current_x, current_y = x_cord, y_cord

        density_diff = self.void_density - particle.density

        if abs(density_diff) < 0.01:
            return current_x, current_y

        if density_diff > 0:
            moves = [
                [(0, -1)],  # Up
                [(-1, -1), (1, -1)],  # Up-left, Up-right
                [(-1, 0), (1, 0)]  # Left, Right
            ]
        else:
            moves = [
                [(0, 1)],  # Down
                [(-1, 1), (1, 1)],  # Down-left, Down-right
                [(-1, 0), (1, 0)]  # Left, Right
            ]

        for move_vec in moves:
            random.shuffle(move_vec)

            for dx, dy in move_vec:
                new_x = current_x + dx
                new_y = current_y + dy

                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    if self.contents[new_x][new_y] == 0:
                        self.contents[new_x][new_y] = particle
                        self.contents[current_x][current_y] = 0
                        return new_x, new_y

        return current_x, current_y

    def swap_particles(self, x1, y1, x2, y2):
        temp = self.contents[x1][y1]
        self.contents[x1][y1] = self.contents[x2][y2]
        self.contents[x2][y2] = temp
        return
