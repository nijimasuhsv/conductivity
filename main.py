%matplotlib inline
import cv2
import csv
import pytz
import glob
import datetime
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def Binarization(PictPath,CutRange):
	# �摜���O���[�X�P�[���œǂݍ���
	GreyImg = cv2.imread(PictPath, cv2.IMREAD_GRAYSCALE)

	# pts1:�摜�؂�o����4�_���w��Apts2:�؂�o����̉摜�T�C�Y(�s�N�Z��)
	pts1 = np.float32(CutRange)
	pts2 = np.float32(np.array([[0,0],[80,0],[0,40],[80,40]]))

	# �؂�o��
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(GreyImg,M,(80,40))

	# �����_�̍폜
	decimalpoint = [37,40,35,58]
	decxmin, decxmax, decymin, decymax = decimalpoint
	dst[decymin:decymax+1, decxmin:decxmax+1] = dst[0, 0]

	# ������(�ڂ���)
	blur = cv2.GaussianBlur(dst,(9,9),2)

	# ��l��
	th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)

	# �����t�H���W�[����
	kernel = np.ones((2,2),np.uint8)
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)

	return opening

def SegJudge(digit):
	list = []
	for t in range(7):
		xmin = digit[t,0]
		xmax = xmin + digit[t,2]
		ymin = digit[t,1]
		ymax = ymin + digit[t,3]
		cut = binimg[ymin:ymax, xmin:xmax]
		total = cv2.countNonZero(cut)
		#print(total)
		if total > 12 * 0.9:
			bw = 0
		else:
			bw = 1

		list.append(bw)

	try:
		num = dictionary[tuple(list)]
	except KeyError:
		return 'error'
	

	return num

def ImgRecognition():
	thousand = np.array([[9,1,2,6],[9,17,2,6],[9,33,2,6],[1,11,6,2],[1,27,6,2],[13,11,6,2],[13,27,6,2]])
	hundred = np.array([[29,1,2,6],[29,17,2,6],[29,33,2,6],[21,11,6,2],[21,27,6,2],[33,11,6,2],[33,27,6,2]])
	ten = np.array([[49,1,2,6],[49,17,2,6],[49,33,2,6],[41,11,6,2],[41,27,6,2],[53,11,6,2],[53,27,6,2]])
	one = np.array([[69,1,2,6],[69,17,2,6],[69,33,2,6],[61,11,6,2],[61,27,6,2],[73,11,6,2],[73,27,6,2]])
	places = [thousand,hundred,ten,one]
	value = []

	for place in places:
		value.append(SegJudge(place))

	try:
		recvalue = value[0] * 1000 + value[1] * 100 + value[2] *10 + value[3]
	except TypeError:
		print(path + ' is unreadable')
		return 0

	return recvalue

def main():
	dictionary = {
		# top, center, bottom, left top, left bottom, right top, right bottom
		(0,0,0,0,0,1,1): 1,
		(1,1,1,0,1,1,0): 2,
		(1,1,1,0,0,1,1): 3,
		(0,1,0,1,0,1,1): 4,
		(1,1,1,1,0,0,1): 5,
		(1,1,1,1,1,0,1): 6,
		(1,0,0,0,0,1,1): 7,
		(1,1,1,1,1,1,1): 8,
		(1,1,1,1,0,1,1): 9,
		(1,0,1,1,1,1,1): 0,
		(0,0,0,0,0,0,0): 0
	}

	paths = glob.glob('Desktop/python/image/*')

	cutrange = np.array([[129, 133], [196, 133], [126, 157], [194, 156]])

	output = []
###
	for path in paths:
		binimg = Binarization(path,cutrange)

		ans = ImgRecognition()

		output.append([ans])

		print('-',end='')
###

	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

	with open('Desktop/python/output_csv/output_{0:%Y%m%d%H%M%S}.csv'.format(now),'w', newline="") as f:
		writer = csv.writer(f)
		writer.writerows(output)

	print('Done.')