import numpy as np
import cv2
from tqdm import tqdm
import random
import os
import shutil

from pattern import CircleGroup
from settings import w, h, totalFrame
from image import getCollection, sampleCollection, applyPattern

circleGroups = []

for i in range(40):
	pick = random.randint(0, 1)
	s, t = None, None
	# if (pick == 0):
	s = (0, random.randint(- h / 2, h))
	t = (w, random.randint(- h / 2, h))
	# else:
	# 	s = (w, random.randint(0, h))
	# 	t = (0, random.randint(0, h))
	# elif (pick == 2):
	# 	s = (random.randint(0, w), 0)
	# 	t = (random.randint(0, w), h)
	# else:
	# 	s = (random.randint(0, w), h)
	# 	t = (random.randint(0, w), 0)
	circleGroups.append(
		(
			CircleGroup(
				(random.randint(320, 800), random.randint(160, 640)),
				s,
				t,
				random.uniform(0.25, 5),
				random.uniform(0.5, 1.4)
			),
			random.randint(0, totalFrame)
		)
	)

circleGroups.sort(key = lambda x: - x[0].scale)

backgroundCollection = getCollection("../DarkMix")
foregroundCollection = getCollection("../LightMix")

try:
	shutil.rmtree('./Frames')
except:
	pass
os.makedirs('./Frames')

print("Testing...")

for frame in tqdm(range(totalFrame)):

	result = sampleCollection(backgroundCollection, frame)

	for circleGroup, sampleOffset in circleGroups:
		circleGroup.update(frame + sampleOffset)

		mask = circleGroup.getMask()

		layer = sampleCollection(foregroundCollection, frame + sampleOffset)
		result = applyPattern(result, layer, mask)

		cv2.imwrite(f"Frames/{'{:0>3}'.format(frame)}.jpg", result)

os.system("ffmpeg -y -r 25 -f image2 -i Frames/%03d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p Results/test.mp4")

try:
	shutil.rmtree('./Frames')
except:
	pass
os.makedirs('./Frames')