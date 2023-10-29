import cv2
import numpy as np

from settings import w, h, uw, uh, unit, totalFrame
from shape import distSegment, mapShape

class CircleGroup:
	def __init__(self, dim, s, t, speed, scale):
		self.w, self.h = dim

		s = (
			s[0] - self.w - unit if s[0] == 0 else s[0] + self.w + unit if s[0] == w else s[0],
			s[1] - self.h - unit if s[1] == 0 else s[1] + self.h + unit if s[1] == h else s[1]
		)
		t = (
			t[0] - self.w - unit if t[0] == 0 else t[0] + self.w + unit if t[0] == w else t[0],
			t[1] - self.h - unit if t[1] == 0 else t[1] + self.h + unit if t[1] == h else t[1]
		)

		self.s = s
		self.t = t
		self.x, self.y = self.s

		self.speed = speed
		self.scale = scale

	def isInside(self, p):
		x, y = p
		return (x >= self.x) and (x <= self.x + self.w) and (y >= self.y) and (y <= self.y + self.h)
	
	def distGroup(self, p):
		if (self.isInside(p)):
			return 0
		else:
			return min(
				distSegment(p, ((self.x, self.y), (self.x + self.w, self.y))),
				distSegment(p, ((self.x, self.y), (self.x, self.y + self.h))),
				distSegment(p, ((self.x + self.w, self.y + self.h), (self.x + self.w, self.y))),
				distSegment(p, ((self.x + self.w, self.y + self.h), (self.x, self.y + self.h)))
			)
	
	def mapGroup(self, p):
		return 2 / (self.distGroup(p) / 100 + 1) - 1

	def update(self, f):
		tt = ((f * self.speed) % totalFrame) / totalFrame
		self.x = (self.t[0] - self.s[0]) * tt + self.s[0]
		self.y = (self.t[1] - self.s[1]) * tt + self.s[1]

	def getMask(self):
		mask = np.zeros((h, w), dtype=np.uint8)

		for i in range(
			int(self.x // unit),
			int((self.x + self.w) // unit + 2)
		):
			for j in range(
				int(self.y // unit),
				int((self.y + self.h) // unit + 2)
			):
				p = (i * unit, j * unit)
				r = int(unit * self.mapGroup(p) * mapShape(p) * self.scale / 2)
				
				if (i >= 0 and i < uw and j >= 0 and j < uh and r > 0):
					cv2.circle(mask, (i * unit, j * unit), r, (255), -1)
		
		return mask