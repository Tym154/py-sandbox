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

                elif PARTICLE_TYPES[particle.p_type]['type'] == 'liquid':
                    new_x, new_y = self.liquid_movement(particle, x, y)
                    updated_coords[x][y] = 0
                    updated_coords[new_x][new_y] = 1

                elif PARTICLE_TYPES[particle.p_type]['type'] == 'gas':
                    new_x, new_y = self.gas_movement(particle, x, y)
                    updated_coords[x][y] = 0
                    updated_coords[new_x][new_y] = 1

    

    def loose_movement(self, particle, x_cord, y_cord):
        max_fall_speed = math.sqrt((2* particle.density * 1 * self.gravity_acceleration) / (self.void_density * 1 * 1))

        particle.velocity_y += particle.density * self.gravity_acceleration

        if particle.velocity_y > max_fall_speed: particle.velocity_y = max_fall_speed

        fall_steps = int(particle.velocity_y)

        current_x, current_y = x_cord, y_cord

        for _ in range(fall_steps):
            if current_y + 1 >= self.height:
                break

            if self.contents[current_x][current_y + 1] == 0:
                self.contents[current_x][current_y + 1] = particle
                self.contents[current_x][current_y] = 0
                current_y += 1
            else:
                offsets = [-1, 1]
                random.shuffle(offsets)
                moved = False
                for offset in offsets:
                    new_x = current_x + offset
                    if 0 <= new_x < self.width and current_y + 1 < self.height:
                        if self.contents[new_x][current_y + 1] == 0:
                            self.contents[new_x][current_y + 1] = particle
                            self.contents[current_x][current_y] = 0
                            current_x, current_y = new_x, current_y + 1
                            moved = True
                            break
                if not moved:
                    break

        return current_x, current_y

    def liquid_movement(self, particle, x_cord, y_cord):
        max_fall_speed = min(particle.density, 8)

        particle.velocity_y += self.gravity_acceleration
        if particle.velocity_y > max_fall_speed:
            particle.velocity_y = max_fall_speed

        fall_steps = int(particle.velocity_y)

        current_x, current_y = x_cord, y_cord

        for _ in range(fall_steps):
            if current_y + 1 >= self.height:
                break
            if self.contents[current_x][current_y + 1] == 0:
                self.contents[current_x][current_y + 1] = particle
                self.contents[current_x][current_y] = 0
                current_y += 1

            else:
                offsets = [-1, 1]
                random.shuffle(offsets)
                moved = False

                for offset in offsets:
                    new_x = current_x + offset
                    if 0 <= new_x < self.width and self.contents[new_x][current_y] == 0:
                        self.contents[new_x][current_y] = particle
                        self.contents[current_x][current_y] = 0
                        current_x = new_x
                        moved = True
                        break

                if not moved:
                    break

        return current_x, current_y


    def gas_movement(self, particle, x_cord, y_cord):
        buoyancy_acceleration = self.gravity_acceleration * (self.void_density - particle.density) / self.void_density

        particle.velocity_y -= buoyancy_acceleration

        max_rise_speed = min(6, abs(buoyancy_acceleration * 10))

        if abs(particle.velocity_y) > max_rise_speed:
            particle.velocity_y = -max_rise_speed

        rise_steps = int(abs(particle.velocity_y))
        if rise_steps == 0:
            return x_cord, y_cord 

        current_x, current_y = x_cord, y_cord

        for _ in range(rise_steps):
            if current_y - 1 < 0:
                break  # reached top of grid

            if self.contents[current_x][current_y - 1] == 0:
                # Move up
                self.contents[current_x][current_y - 1] = particle
                self.contents[current_x][current_y] = 0
                current_y -= 1

            else:
                # Try spreading left or right randomly
                offsets = [-1, 1]
                random.shuffle(offsets)
                moved = False

                for offset in offsets:
                    new_x = current_x + offset
                    if 0 <= new_x < self.width and self.contents[new_x][current_y] == 0:
                        self.contents[new_x][current_y] = particle
                        self.contents[current_x][current_y] = 0
                        current_x = new_x
                        moved = True
                        break

                if not moved:
                    break  # fully blocked

        return current_x, current_y