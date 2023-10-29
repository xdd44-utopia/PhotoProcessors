import numpy as np

from settings import shapeCoords

isLogo = False

def isInside(p): #Currenty only for my logo

	x, y = p
	x1, y1 = shapeCoords[0][0]
	x2, y2 = shapeCoords[1][0]
	x3, y3 = shapeCoords[2][0]

	m1 = (y2 - y1) / (x2 - x1)
	c1 = y1 - m1 * x1
	
	m2 = (y3 - y2) / (x3 - x2)
	c2 = y2 - m2 * x2
	
	m3 = (y3 - y1) / (x3 - x1)
	c3 = y1 - m3 * x1

	return (y <= m1 * x + c1) and (y <= m2 * x + c2) and (y >= m3 * x + c3)

def distSegment(p, line):

	x, y = p
	((sx, sy), (tx, ty)) = line

	sqLength = (tx - sx) ** 2 + (ty - sy) ** 2
	t = ((x - sx) * (tx - sx) + (y - sy) * (ty - sy)) / sqLength
	t = max(0, min(1, t))

	proj_x = sx + t * (tx - sx)
	proj_y = sy + t * (ty - sy)

	return np.sqrt((x - proj_x)**2 + (y - proj_y)**2)

def distShape(p):

	if (isLogo and isInside(p)):
		return 0
	else:
		return min(distSegment(p, line) for line in shapeCoords)

def mapShape(p):
	return 1 / (distShape(p) / 20 + 1)