%matplotlib inline
import cv2
import glob
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def Binarization(PictPath,CutRange):

	# 画像をグレースケールで読み込み
	img = cv2.imread(PictPath, cv2.IMREAD_GRAYSCALE)

	# pts1:画像切り出しの4点を指定、pts2:切り出し後の画像サイズ(ピクセル)
	pts1 = np.float32(CutRange)
	pts2 = np.float32([[0,0],[80,0],[0,40],[80,40]])

	# 切り出し
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(img,M,(80,40))

	# 小数点の削除
	decimalpoint = [37,40,35,58]
	xmin, xmax, ymin, ymax = decimalpoint
	dst[ymin:ymax+1, xmin:xmax+1] = dst[0, 0]

	# 平滑化(ぼかし)
	blur = cv2.GaussianBlur(dst,(9,9),2)

	# 二値化
	th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)

	# モルフォロジー処理
	kernel = np.ones((2,2),np.uint8)
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	
	return opening

def RangeCheck():
	fig = plt.figure(figsize=(12, 8))
	ax0 = fig.add_subplot(1,1,1)

	for i in range(80):
		ax0.axvline(i, color = 'lightgrey')

	for i in range(40):
		ax0.axhline(i, color = 'lightgrey')

	for i in range(5):
		ax0.axvline(i*20, color = 'red')

	paths = glob.glob('Desktop/python/image/*')
	list = paths[0]

	cutrange = np.array([[129, 133], [196, 133], [126, 157], [194, 156]])

	binimg0 = Binarization(list,cutrange)

	ax0.imshow(binimg0, cmap='gray')

	cutrange = 0

	plt.show()

RangeCheck()