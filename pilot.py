#!/usr/env/python python3

from PIL import Image

from WaveSource import WaveSource
from PlaneWave import PlaneWave
from SlitSource import SlitSource
from Domain import Domain
from Canvas import Canvas

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
    def __init__(self):
        self.im_size = np.array((700, 300))

        self.wall_pos = 20
        self.wall_width = 0

        self.low_threshold = 0
        self.high_threshold = 1

        self.wavelength = 6

        self.incoming_domain = (0, 0, self.wall_pos, self.im_size[1])
        self.interference_domain = (self.wall_pos + self.wall_width, 0, self.im_size[0], self.im_size[1])

        self.plane_wave = PlaneWave(self.wavelength, 1, self.incoming_domain, np.array([1.0, 0.0]))
        
        self.source_1 = WaveSource((self.wall_pos + self.wall_width, 100), self.wavelength, self.interference_domain, 0.5)
        self.source_2 = WaveSource((self.wall_pos + self.wall_width, 200), self.wavelength, self.interference_domain, 0.5)

    def run(self):
        slit1wavedata = self.source_1.get_wave_data()
        slit2wavedata = self.source_2.get_wave_data()

        wave_data = slit1wavedata + slit2wavedata
        
        d_data = []
        
        d_data.append((self.incoming_domain, self.plane_wave.get_wave_data()))
        d_data.append((self.interference_domain, wave_data))
        
        data = np.zeros((self.im_size[1], self.im_size[0], 3))
        
        for d in d_data:
            domain = d[0]
            datum = d[1]
            
            x0 = domain[0]
            y0 = domain[1]
            width = domain[3] - y0
            height = domain[2] - x0
            
            print("x0", x0)
            print("y0", y0)
            print("width", width)
            print("height", height)
            print("shape", datum.shape)
            
            for x in range(height):
                for y in range(width):
                    val = datum[y, x]
                    if val >= 0:
                        data[y0 + y, x0 + x, 0] = val
                    if val < 0:
                        data[y0 + y, x0 + x, 2] = -val

            print("=="*30)


        # tb_pad = (self.interference_domain[1], self.im_size[1] - self.interference_domain[3])
        # lr_pad = (self.interference_domain[0], self.im_size[0] - self.interference_domain[2])

        # data = np.pad(wave_data, [tb_pad, lr_pad], mode='constant')
        
        # print(ddata == data)
        
        data = norm(data)
        data[data < self.low_threshold] = 0
        data[data > self.high_threshold] = 1
        
        data *= 255
        
        im = Image.fromarray(data.astype(np.uint8))
        im.save(f"test_interference.png")
        im.show()

class PILTest_interference_adv():
    def __init__(self):
        self.im_size = np.array((700, 300))
        
        self.canvas = Canvas(*self.im_size)
        
        self.im_domain = Domain(0, 0, self.im_size[0], self.im_size[1])

        self.wall_pos = 20
        self.wall_width = 4
        
        self.slit_width = 6
        
        self.slit_sep = 100
        
        self.slit_pos_top = (self.wall_pos, (self.im_size[1] / 2) - (self.slit_sep / 2))
        self.slit_pos_bot = (self.wall_pos, (self.im_size[1] / 2) + (self.slit_sep / 2))
        
        self.num_sources = 10

        self.low_threshold = 0
        self.high_threshold = 1

        self.wavelength = 6
        
        self.amplitude = 1
        
        self.image_domain = Domain(0, 0, *self.im_size)

        # self.incoming_domain = (0, 0, self.wall_pos, self.im_size[1])
        # self.interference_domain = (self.wall_pos + self.wall_width, 0, self.im_size[0], self.im_size[1])
        self.incoming_domain, self.interference_domain = self.image_domain.split_vertical(self.wall_pos)

        self.plane_wave = PlaneWave(self.wavelength, self.amplitude, self.incoming_domain, np.array([1.0, 0.0]))
        
        self.slit_1 = SlitSource(self.slit_pos_top, self.slit_width, self.num_sources, self.wavelength, self.amplitude/2, self.interference_domain)
        self.slit_2 = SlitSource(self.slit_pos_bot, self.slit_width, self.num_sources, self.wavelength, self.amplitude/2, self.interference_domain)

    def draw_superficial_barrier(self, domain, data):
        self.canvas.drawData(np.full(domain.shape, 1), domain)
        
        # width = int(domain[3] - y0)
        # height = int(domain[2] - x0)
        
        # for x in range(height):
        #     for y in range(width):
        #         data[y0 + y, x0 + x, :] = 1

    def run(self):
        d_data = []
        
        d_data.append((self.incoming_domain, self.plane_wave.get_wave_data()))
        
        d_data.append((self.interference_domain, self.slit_1.get_wave_data() + self.slit_2.get_wave_data()))
        
        visual_data = np.zeros((self.im_size[1], self.im_size[0], 3))
        overlay_data = np.zeros((self.im_size[1], self.im_size[0], 3))
        
        for d in d_data:
            domain = d[0].getBounds()
            datum = d[1]
            
            x0 = domain[0]
            y0 = domain[1]
            width = domain[3] - y0
            height = domain[2] - x0
            
            print("x0", x0)
            print("y0", y0)
            print("width", width)
            print("height", height)
            print("shape", datum.shape)
            
            for x in range(height):
                for y in range(width):
                    val = datum[y, x]
                    if val >= 0:
                        visual_data[y0 + y, x0 + x, 0] = val
                    if val < 0:
                        visual_data[y0 + y, x0 + x, 2] = -val

            print("=="*30)
        
        # self.draw_superficial_barrier((self.wall_pos-self.wall_width/2, 0, self.wall_pos + self.wall_width/2, self.slit_pos_top[1] - self.slit_width/2), overlay_data)
        # self.draw_superficial_barrier((self.wall_pos-self.wall_width/2, self.slit_pos_top[1] + self.slit_width/2, self.wall_pos + self.wall_width/2, self.slit_pos_bot[1] - self.slit_width/2), overlay_data)
        # self.draw_superficial_barrier((self.wall_pos-self.wall_width/2, self.slit_pos_bot[1] + self.slit_width/2, self.wall_pos + self.wall_width/2, self.im_size[1]), overlay_data)
        
        self.im_domain.draw_domain(overlay_data)
        
        visual_data = norm(visual_data) * 255
        overlay_data = norm(overlay_data) * 255
        # data[data < self.low_threshold] = 0
        # data[data > self.high_threshold] = 1
        
        image_data = visual_data + overlay_data
        
        #self.canvas.getData()
        
        im = Image.fromarray(image_data.astype(np.uint8))
        im.save(f"test_interference_adv.png")
        im.show()

# PILTest_interference().run()
PILTest_interference_adv().run()