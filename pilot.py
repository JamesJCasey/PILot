#!/usr/env/python python3

from PIL import Image

from WaveSource import WaveSource
from PlaneWave import PlaneWave
from SlitSource import SlitSource
from Domain import Domain
from Canvas import Canvas
from Barrier import Barrier
from GenericWaveDrawer import GenericWaveDrawer

import numpy as np

def norm(array):
    return (array / np.max(np.abs(array)))

class PILTest_dist():
    def __init__(self):
        self.w = self.h = 500
        self.centre = np.array([100, 70])
        self.data = np.zeros((self.w, self.h, 3))
        self.r = np.random.choice([1, 2, 3, 4])

    def dist_func(self, array, pow):
        return (np.sum(np.abs(array)**pow))**(1/pow)

    def run(self):
        for x in range(self.w):
            for y in range(self.h):
                vec = self.centre - [x, y]
                dist = self.dist_func(vec, self.r)

                self.data[x, y, 0] = dist * np.cos(dist)
                self.data[x, y, 1] = dist * np.sin(dist)
                self.data[x, y, 2] = dist * 0.5 * (np.cos(dist) + np.sin(dist))

        self.data  = (1-norm(self.data)) * 255

        im = Image.fromarray(self.data.astype(np.uint8))
        im.save(f"test_euclid.png")

class PILTest_interference():
    def __init__(self, wavelength = 6):
        global IMAGE_SIZE
        IMAGE_SIZE = (700, 300)
        
        self.im_size = np.array((700, 300))
        
        self.canvas = Canvas(*self.im_size)
        
        self.im_domain = self.canvas.getDomain()

        self.wall_pos = 20
        self.wall_width = 4
        
        self.slit_width = 6
        
        self.slit_sep = 100
        
        # self.slit_pos_top = (self.wall_pos, (self.im_size[1] / 2) - (self.slit_sep / 2))
        # self.slit_pos_mid = (self.wall_pos, (self.im_size[1] / 2))
        # self.slit_pos_bot = (self.wall_pos, (self.im_size[1] / 2) + (self.slit_sep / 2))
        
        self.num_sources = 10

        self.low_threshold = 0
        self.high_threshold = 1

        self.wavelength = wavelength
        
        self.amplitude = 1
        
        self.image_domain = Domain(0, 0, *self.im_size)

        self.incoming_domain, self.interference_domain = self.image_domain.split_vertical(self.wall_pos)

        self.plane_wave = PlaneWave(self.wavelength, self.amplitude, self.incoming_domain, np.array([1.0, 0.0]))
        
        self.barrier = Barrier(Domain(self.wall_pos, 0, self.wall_pos + self.wall_width, IMAGE_SIZE[1]))
        self.barrier.setSlits(2, self.slit_width, self.slit_sep, self.interference_domain)
        
        self.wave_drawer = GenericWaveDrawer()
        # self.slit_1 = SlitSource(self.slit_pos_top, self.slit_width, self.num_sources, self.wavelength, self.amplitude/3, self.interference_domain)
        # self.slit_2 = SlitSource(self.slit_pos_mid, self.slit_width, self.num_sources, self.wavelength, self.amplitude/3, self.interference_domain)
        # self.slit_3 = SlitSource(self.slit_pos_bot, self.slit_width, self.num_sources, self.wavelength, self.amplitude/3, self.interference_domain)

    def draw_superficial_barrier(self, domain, data):
        self.canvas.drawData(np.full(domain.shape, 255), domain)

    def run(self):
        d_data = []
        
        self.wave_drawer.drawPlaneWaveData(self.plane_wave.get_wave_data(), self.incoming_domain, self.canvas)
        self.wave_drawer.drawPlaneWaveData(self.barrier.get_wave_data(), self.interference_domain, self.canvas)
        
        # self.draw_superficial_barrier(Domain(self.wall_pos-self.wall_width/2, 0, self.wall_pos + self.wall_width/2, self.slit_pos_top[1] - self.slit_width/2), self.canvas.getData())
        # self.draw_superficial_barrier(Domain(self.wall_pos-self.wall_width/2, self.slit_pos_top[1] + self.slit_width/2, self.wall_pos + self.wall_width/2, self.slit_pos_bot[1] - self.slit_width/2), self.canvas.getData())
        # self.draw_superficial_barrier(Domain(self.wall_pos-self.wall_width/2, self.slit_pos_bot[1] + self.slit_width/2, self.wall_pos + self.wall_width/2, self.im_size[1]), self.canvas.getData())
        
        im = self.canvas.getImage()
        if 1:
            im.save(f"test_interference_{self.wavelength}.png")
            im.show()
        return im

PILTest_interference().run()

# ims = []
# for i in range(1, 30):
#     ims.append(PILTest_interference(i).run())

# ims[0].save('diffractions_1.gif', save_all=True, append_images=ims[1:])