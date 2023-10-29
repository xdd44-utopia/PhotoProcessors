import cv2
import random
from tqdm import tqdm
import os
import numpy as np
import math

from settings import w, h

speed = 0.1

def getCollection(dirName):
	collection = []
	print("Loading images...")
	for imagePath in tqdm(os.listdir(dirName)):
		if (imagePath.endswith(".jpg") or imagePath.endswith(".JPG") or imagePath.endswith(".Jpg")):
			im = cv2.imread(dirName + "/" + imagePath)
			canvasRatio = w / h
			imageRatio = im.shape[1] / im.shape[0]
			im = cv2.resize(im, (
				w if imageRatio < canvasRatio else int(h * imageRatio),
				h if imageRatio > canvasRatio else int(w / imageRatio)
			))
			offset = (
				random.randint(0, im.shape[1] - w),
				random.randint(0, im.shape[0] - h)
			)
			im = im[offset[1] : offset[1] + h, offset[0] : offset[0] + w, :]
			collection.append(im)

	random.shuffle(collection)
	return collection

def norm(x, mean):
	sd = 1.21
	var = float(sd) ** 2
	denom = (2 * math.pi * var) ** 0.5
	num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
	return int(num * 775 / denom)

def sampleCollection(collection, f):
	sample = cv2.cvtColor(np.zeros((h, w), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
	f *= speed
	while (f > len(collection)):
		f -= len(collection)
	for i in range(len(collection)):
		alpha = max(
			norm(i, f),
			norm(i, f - len(collection)),
			norm(i, f + len(collection))
		)
		if (alpha > 0):
			alpha /= 256.0
			sample = cv2.addWeighted(collection[i], alpha, sample, 1 - alpha, 0)
	return sample

def applyPattern(origin, layer, mask):
	roi = cv2.bitwise_and(layer, layer, mask=mask)
	mask_inv = cv2.bitwise_not(mask)
	background = cv2.bitwise_and(origin, origin, mask=mask_inv)
	composited = cv2.add(roi, background)
	return composited

# print(norm(0, 0, 1.21))
# print(norm(4, 0, 1.21))