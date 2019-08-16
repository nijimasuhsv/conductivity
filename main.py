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
	# 画像をグレースケールで読み込み
	GreyImg = cv2.imread(PictPath, cv2.IMREAD_GRAYSCALE)

	# pts1:画像切り出しの4点を指定、pts2:切り出し後の画像サイズ(ピクセル)
	pts1 = np.float32(CutRange)
	pts2 = np.float32(np.array([[0,0],[80,0],[0,40],[80,40]]))

	# 切り出し
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(GreyImg,M,(80,40))

	# 小数点の削除
	decimalpoint = [37,40,35,58]
	decxmin, decxmax, decymin, decymax = decimalpoint
	dst[decymin:decymax+1, decxmin:decxmax+1] = dst[0, 0]

	# 平滑化(ぼかし)
	blur = cv2.GaussianBlur(dst,(9,9),2)

	# 二値化
	th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)

	# モルフォロジー処理
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
		if total < 26 * 0.2:
			bw = 1
		else:
			bw = 0

		list.append(bw)

	try:
		num = dictionary[tuple(list)]
	except KeyError:
		return 'error'
	

	return num

def ImgRecognition():
	thousand = np.array([[6,4,10,2],[6,19,10,2],[6,34,10,2],[4,6,2,13],[4,21,2,13],[16,6,2,13],[16,21,2,13]])
	hundred = np.array([[26,4,10,2],[26,19,10,2],[26,34,10,2],[24,6,2,13],[24,21,2,13],[36,6,2,13],[36,21,2,13]])
	ten = np.array([[46,4,10,2],[46,19,10,2],[46,34,10,2],[44,6,2,13],[44,21,2,13],[56,6,2,13],[56,21,2,13]])
	one = np.array([[66,4,10,2],[66,19,10,2],[66,34,10,2],[64,6,2,13],[64,21,2,13],[76,6,2,13],[76,21,2,13]])
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