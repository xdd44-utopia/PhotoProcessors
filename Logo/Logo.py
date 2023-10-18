from PIL import Image
import os
from os import listdir

logo = Image.open("logo.png")

for imagePath in os.listdir("./"):
	if (imagePath.endswith(".jpg")):
		im = Image.open(imagePath).convert('RGBA')
		im = im.resize((6000, im.size[1] * 6000 // im.size[0]) if im.size[0] > im.size[1] else (im.size[0] * 6000 // im.size[1], 6000))
		im.paste(logo, ((im.size[0] - 750) // 2, im.size[1] - 120), logo)
		im = im.convert('RGB')
		im.save(imagePath[:-3] + "_marked.jpg")
