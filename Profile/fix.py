from PIL import Image
import colorsys
from tqdm import tqdm

class Color:
	def __init__(self, color):
		self.color = color
		self.count = 1
	def increment(self):
		self.count += 1
	def __lt__(self, other):
		return self.count < other.count
	def __le__(self, other):
		return self.count <= other.count

def color_distance(c1, c2):
	(r1, g1, b1) = c1
	(r2, g2, b2) = c2
	(r1, g1, b1) = (r1 / 255.0, g1 / 255.0, b1 / 255.0)
	(r2, g2, b2) = (r2 / 255.0, g2 / 255.0, b2 / 255.0)
	(h1, s1, v1) = colorsys.rgb_to_hsv(r1, g1, b1)
	(h2, s2, v2) = colorsys.rgb_to_hsv(r2, g2, b2)
	if (s1 > 0.9) ^ (s2 > 0.9):
		return 1000000
	if (s1 > 0.9):
		return abs(h1 - h2)
	else:
		return abs(v1 - v2)

mask = Image.open("mask.png").convert("RGB")
pixels = mask.load()
w = mask.width
h = mask.height

given_colors = []
colors = []

for x in tqdm(range(w)):
	for y in range(h):
		color = pixels[x, y]
		done = False
		for i in range(len(colors)):
			if (colors[i].color == color):
				colors[i].increment()
				done = True
				break
		if (not done):
			colors.append(Color(color))
colors.sort(reverse=True)
for i in range(20):
	given_colors.append(colors[i].color)

print(given_colors)

for x in tqdm(range(w)):
	for y in range(h):
		pixels[x, y] = min(given_colors, key = lambda c: color_distance(c, pixels[x, y]))

mask.save("mask_fixed.png")