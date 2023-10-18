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
# circleGroups = [
# 	(CircleGroup((640, 400), (0, 400), (w, 750), 240, 1.2), random.randint(0, 100), random.randint(0, 500)),
# 	(CircleGroup((320, 800), (1200, h), (800, 0), 200, 1.2), random.randint(0, 100), random.randint(0, 500)),
# 	(CircleGroup((500, 350), (800, 0), (1250, h), 300, 1), random.randint(0, 100), random.randint(0, 500)),
# 	(CircleGroup((1200, 320), (640, 0), (320, h), 160, 0.8), random.randint(0, 100), random.randint(0, 500)),
# 	(CircleGroup((400, 400), (w, 1600), (0, 1000), 275, 0.8), random.randint(0, 100), random.randint(0, 500))
# ]

for i in range(32):
	pick = random.randint(0, 3)
	s, t = None, None
	if (pick == 0):
		s = (0, random.randint(0, h))
		t = (w, random.randint(0, h))
	elif (pick == 1):
		s = (w, random.randint(0, h))
		t = (0, random.randint(0, h))
	elif (pick == 2):
		s = (random.randint(0, w), 0)
		t = (random.randint(0, w), h)
	else:
		s = (random.randint(0, w), h)
		t = (random.randint(0, w), 0)
	circleGroups.append(
		(
			CircleGroup(
				(random.randint(160, 640), random.randint(160, 640)),
				s,
				t,
				random.uniform(0.2, 1),
				random.uniform(0.4, 1.25)
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