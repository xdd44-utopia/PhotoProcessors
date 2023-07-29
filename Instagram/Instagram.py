from PIL import Image
import os
from os import listdir

for imagePath in os.listdir("./"):
	if (imagePath.endswith(".jpg")):
		im = Image.open(imagePath)
		im = im.resize((4000, im.size[1] * 4000 // im.size[0]) if im.size[0] > im.size[1] else (im.size[0] * 4000 // im.size[1], 4000))
		output = Image.new("RGB", (5000, 5000), (0, 0, 0))
		output.paste(im, ((5000 - im.size[0]) // 2, (5000 - im.size[1]) // 2))
		output.save(imagePath[:-3] + "_padded.jpg")
