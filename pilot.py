#!/usr/env/python python3

from PIL import Image
import numpy as np

def norm(array):
	return (array / np.max(array))

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

		self.data  = (1-norm(self.data)) * 256

		im = Image.fromarray(self.data.astype(np.uint8))
		im.save(f"test_euclid.png")

class PILTest_interference():
	def __init__(self):
		self.im_size = (100, 100)
		self.slit1pos = (10, 10)
		self.slit2pos = (10, 90)

		self.wavelength = 10

		self.domain = (10, 0, self.im_size[0], self.im_size[1])

	def euclid(self, array):
		return (np.sum(np.abs(array)**2))**(1/2)

	def source(self, pos, domain):
		x_min, y_min, x_max, y_max = domain

		x = np.arange(x_min, x_max)
		y = np.arange(y_min, y_max)

		x -= pos[0]
		y -= pos[1]

		xx, yy = np.meshgrid(x, y)

		data = 1 + np.cos(2 * np.pi/self.wavelength * np.sqrt(xx**2 + yy**2))
		return data

	def run(self):
		slit1wavedata = self.source(self.slit1pos, self.domain)
		slit2wavedata = self.source(self.slit2pos, self.domain)

		wave_data = slit1wavedata + slit2wavedata

		tb_pad = (self.domain[1], self.im_size[1] - self.domain[3])
		lr_pad = (self.domain[0], self.im_size[0] - self.domain[2])

		data = np.pad(wave_data, [tb_pad, lr_pad], mode='constant')
		d = data[..., np.newaxis]
		d = np.resize(d, (d.shape[0], d.shape[1], 3))
		print(d)
		data = norm(data) * 256

		im = Image.fromarray(data.astype(np.uint8))
		im.save(f"test_interference.png")

# PILTest_dist().run()
PILTest_interference().run()