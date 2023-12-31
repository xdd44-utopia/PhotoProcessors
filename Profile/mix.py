from PIL import Image
import numpy as np
import os
import random
from tqdm import tqdm

dirName = "../Dark"
dirName = "../Light"
size = 1000

collection = []

for imagePath in tqdm(os.listdir(dirName)):
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

for i in tqdm(range(100)):
	mix = []
	for j in range(5):
		pick = random.randint(0, 10000)
		mix.append(collection[pick % len(collection)])
	mix = np.array(mix)
	avg = np.average(mix, axis = 0)
	result = Image.fromarray(avg.astype(np.uint8), "RGB")
	result.save(f"{dirName}Mix/{i}.jpg")