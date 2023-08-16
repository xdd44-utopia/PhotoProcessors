from PIL import Image
import os
import random
import colorsys
from tqdm import tqdm

class Component:
	def __init__(self, mask):
		pixels = mask.load()

		min_x, min_y = mask.width, mask.height
		max_x, max_y = 0, 0

		for x in range(mask.width):
			for y in range(mask.height):
				r, g, b, a = pixels[x, y]
				if r == 255 and g == 255 and b == 255:  # Check for white pixels
					min_x = min(min_x, x)
					min_y = min(min_y, y)
					max_x = max(max_x, x)
					max_y = max(max_y, y)

		# Crop the mask to the bounding box
		self.mask = mask.crop((min_x, min_y, max_x + 1, max_y + 1))
		self.position = (min_x, min_y)
	
	def update_image(self, image):
		if (image.width / image.height > self.mask.width / self.mask.height):
			self.image = image.resize((image.width * self.mask.height // image.height, self.mask.height))
		else:
			self.image = image.resize((self.mask.width, self.mask.width * image.height // image.width))
		image = image.resize(mask.size)
		self.image = image.resize(self.mask.size)


mask = Image.open("mask_fixed.png")
pixels = mask.load()
w, h = mask.width, mask.height

colors = [(64, 64, 64), (0, 0, 0), (173, 173, 173), (205, 205, 205), (134, 134, 134), (92, 92, 92), (48, 48, 48), (150, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 255), (255, 0, 132), (0, 255, 119), (255, 255, 0), (255, 129, 0), (0, 255, 255), (0, 0, 255), (0, 129, 255), (255, 0, 255), (144, 144, 144)]
colors_norm = list(map(lambda c: (c[0] / 255.0, c[1] / 255.0, c[2] / 255.0), colors))
colors_hsv = list(map(lambda c: colorsys.rgb_to_hsv(c[0], c[1], c[2]), colors_norm))

n = len(colors)
split_masks = []
split_masks_pixels = []
for c in colors:
	m = Image.new('RGBA', (w, h), (0, 0, 0, 0))
	split_masks.append(m)
	split_masks_pixels.append(m.load())

for x in tqdm(range(w)):
	for y in range(h):
		for i in range(n):
			if pixels[x, y] == colors[i]:
				split_masks_pixels[i][x, y] = (255, 255, 255, 255)

components = list(map(lambda mask: Component(mask), split_masks))

dark_path = "../DarkMix/"
dark_images = []
light_path = "../LightMix/"
light_images = []
for image_path in os.listdir(dark_path):
	if (image_path.endswith(".jpg")):
		dark_images.append(Image.open(os.path.join(dark_path, image_path)).convert('RGBA'))
for image_path in os.listdir(light_path):
	if (image_path.endswith(".jpg")):
		light_images.append(Image.open(os.path.join(light_path, image_path)).convert('RGBA'))

result = mask.copy()
for i in tqdm(range(n)):
	pick = random.randint(0, 10000)
	components[i].update_image(light_images[pick % len(light_images)] if colors_hsv[i][1] > 0.9 else dark_images[pick % len(dark_images)])
	result.paste(components[i].image, components[i].position, components[i].mask)

result.save("result.png")