import numpy as np
import cv2
from tqdm import tqdm

from pattern import CircleGroup
from settings import w, h, unit
from image import getCollection, sampleCollection, applyPattern

circleGroup = CircleGroup((640, 400), (0, 400), (w, 750), 100)

dirName = "../DarkMix"
collection = getCollection(dirName)


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("Results/test.mp4", fourcc, 25, (w, h))

print("Testing...")

for frame in tqdm(range(100)):

	result = cv2.cvtColor(np.zeros((w, h), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
	circleGroup.update(frame)
	mask = circleGroup.getMask()
	layer = sampleCollection(collection, frame)
	result = applyPattern(result, layer, mask)
	
	out.write(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))

out.release()