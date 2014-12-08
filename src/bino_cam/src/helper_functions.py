
import os
import numpy as np
import cv2

width = 1280/2 
height = 720

def getFrames(cams):
	return (__getFrame(cams[0]), __getFrame(cams[1]))

def getDistance(window, taskbarName):
	position = cv2.getTrackbarPos(taskbarName, window)
	if(position == -1):
		return 0
	else:
		return position

def getHeight():
	return height
	
def getWidth():
	return width
		
def disableAutoFocus():
	## If that doesn't work try, sudo apt-get install v4l-utils
	os.system('v4l2-ctl -d 0 -c focus_auto=0')
	os.system('v4l2-ctl -d 0 -c focus_absolute=20')
	os.system('v4l2-ctl -d 1 -c focus_auto=0')
	os.system('v4l2-ctl -d 1 -c focus_absolute=20')

def setFocus(cam, focus):
	os.system('v4l2-ctl -d '+ str(cam) +' -c focus_absolute=' + str(focus))
	
def setCameraResolutions(cams, w, h):
	if(__cameraValid(cams[0])):
		__setCameraResolution(cams[0], w, h)
	if(__cameraValid(cams[1])):
		__setCameraResolution(cams[1], w, h)

def setCameraResolutions16x9(cams, h):
	w = 16 * (h/9)
	if(__cameraValid(cams[0])):
		__setCameraResolution(cams[0], w, h)
	if(__cameraValid(cams[1])):
		__setCameraResolution(cams[1], w, h)

def callback(value):
	pass

def sideBySide(frames):
	image = None
	imagePart1 = __returnValidImage(frames[0])
	imagePart2 = __returnValidImage(frames[1])
	image = np.hstack((imagePart1, imagePart2))
	return image

def redGreen(distance, frames):
	image = None
	imagePart1 = __getRedImage(frames[0])
	imagePart2 = __getGreenBlueImage(frames[1])
	image = __combineImages(distance, imagePart1, imagePart2)
	return image
	
def __getFrame(cam):
	try:
		ret, frame = cam.read()
		return frame
	except:
		return None

def __cameraValid(cam):
	return cam != None and cam.isOpened()

def __setCameraResolution(cam, w, h):
	global width, height 
	cam.set(3, w)
	cam.set(4, h)
	width = int(cam.get(3))
	height = int(cam.get(4))

def __returnValidImage(image):
	if image != None:
		return image
	else:
		blank_image = np.zeros((height, width, 3), np.uint8)
		return blank_image

def __getRedImage(image=None): 
	red = np.zeros((height, width, 3), np.uint8)
	if image != None:
		red[:,:,2] = image[:,:,2]	#(B, G, R)
	return red
	
def __getGreenBlueImage(image=None): 
	greenBlue = np.zeros((height, width, 3), np.uint8)
	if image != None:
		greenBlue[:,:,:2] = image[:,:,:2]	# (B, G, R)
	return  greenBlue

def __combineImages(distance, image1, image2):
	totalWidth = width + distance
	image = np.zeros((height, totalWidth, 3), np.uint8)
	image[:, :width, 2] = image1[:, :, 2]
	image[:, distance:, :2] = image2[:, :, :2]
	return image
