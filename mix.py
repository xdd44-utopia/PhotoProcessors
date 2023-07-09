from PIL import Image
import numpy as np
import os
import random

dirName = "Dark"
size = 1000

collection = []

for imagePath in os.listdir(dirName):
	if (imagePath.endswith(".jpg") or imagePath.endswith(".JPG") or imagePath.endswith(".Jpg")):
		im = Image.open(dirName + "/" + imagePath)
		if (min(im.size[0], im.size[1]) < size):
			im = im.resize((
				1000 if im.size[0] < im.size[1] else im.size[0] * 1000 // im.size[1],
				1000 if im.size[0] >= im.size[1] else im.size[1] * 1000 // im.size[0]
			))
		offset = (
			random.randint(0, im.size[0] - size),
			random.randint(0, im.size[1] - size)
		)
		imp = im.crop((offset[0], offset[1], offset[0] + size, offset[1] + size))
		collection.append(np.asarray(imp))

random.shuffle(collection)

for i in range(10):
	mix = []
	for j in range(8):
		mix.append(collection[i * 8 + j])
	mix = np.array(mix)
	avg = np.average(mix, axis = 0)
	result = Image.fromarray(avg.astype(np.uint8), "RGB")
	result.save(f"{dirName}Mix/{i}.jpg")