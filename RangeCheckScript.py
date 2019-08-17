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
	r1 = Rectangle(xy=(9,1),width=2,height=7,ec='blue',fill=False)
	r2 = Rectangle(xy=(29,1),width=2,height=7,ec='blue',fill=False)
	r3 = Rectangle(xy=(49,1),width=2,height=7,ec='blue',fill=False)
	r4 = Rectangle(xy=(69,1),width=2,height=7,ec='blue',fill=False)
	r5 = Rectangle(xy=(9,16),width=2,height=8,ec='blue',fill=False)
	r6 = Rectangle(xy=(29,16),width=2,height=8,ec='blue',fill=False)
	r7 = Rectangle(xy=(49,16),width=2,height=8,ec='blue',fill=False)
	r8 = Rectangle(xy=(69,16),width=2,height=8,ec='blue',fill=False)
	r9 = Rectangle(xy=(9,32),width=2,height=7,ec='blue',fill=False)
	r10 = Rectangle(xy=(29,32),width=2,height=7,ec='blue',fill=False)
	r11 = Rectangle(xy=(49,32),width=2,height=7,ec='blue',fill=False)
	r12 = Rectangle(xy=(69,32),width=2,height=7,ec='blue',fill=False)
	r13 = Rectangle(xy=(1,11),width=6,height=2,ec='blue',fill=False)
	r14 = Rectangle(xy=(1,27),width=6,height=2,ec='blue',fill=False)
	r15 = Rectangle(xy=(13,11),width=6,height=2,ec='blue',fill=False)
	r16 = Rectangle(xy=(13,27),width=6,height=2,ec='blue',fill=False)
	r17 = Rectangle(xy=(21,11),width=6,height=2,ec='blue',fill=False)
	r18 = Rectangle(xy=(21,27),width=6,height=2,ec='blue',fill=False)
	r19 = Rectangle(xy=(33,11),width=6,height=2,ec='blue',fill=False)
	r20 = Rectangle(xy=(33,27),width=6,height=2,ec='blue',fill=False)
	r21 = Rectangle(xy=(41,11),width=6,height=2,ec='blue',fill=False)
	r22 = Rectangle(xy=(41,27),width=6,height=2,ec='blue',fill=False)
	r23 = Rectangle(xy=(53,11),width=6,height=2,ec='blue',fill=False)
	r24 = Rectangle(xy=(53,27),width=6,height=2,ec='blue',fill=False)
	r25 = Rectangle(xy=(61,11),width=6,height=2,ec='blue',fill=False)
	r26 = Rectangle(xy=(61,27),width=6,height=2,ec='blue',fill=False)
	r27 = Rectangle(xy=(73,11),width=6,height=2,ec='blue',fill=False)
	r28 = Rectangle(xy=(73,27),width=6,height=2,ec='blue',fill=False)

	r29 = Rectangle(xy=(9,1),width=2,height=7,ec='blue',fill=False)
	r30 = Rectangle(xy=(29,1),width=2,height=7,ec='blue',fill=False)
	r31 = Rectangle(xy=(49,1),width=2,height=7,ec='blue',fill=False)
	r32 = Rectangle(xy=(69,1),width=2,height=7,ec='blue',fill=False)
	r33 = Rectangle(xy=(9,16),width=2,height=8,ec='blue',fill=False)
	r34 = Rectangle(xy=(29,16),width=2,height=8,ec='blue',fill=False)
	r35 = Rectangle(xy=(49,16),width=2,height=8,ec='blue',fill=False)
	r36 = Rectangle(xy=(69,16),width=2,height=8,ec='blue',fill=False)
	r37 = Rectangle(xy=(9,32),width=2,height=7,ec='blue',fill=False)
	r38 = Rectangle(xy=(29,32),width=2,height=7,ec='blue',fill=False)
	r39 = Rectangle(xy=(49,32),width=2,height=7,ec='blue',fill=False)
	r40 = Rectangle(xy=(69,32),width=2,height=7,ec='blue',fill=False)
	r41 = Rectangle(xy=(1,11),width=6,height=2,ec='blue',fill=False)
	r42 = Rectangle(xy=(1,27),width=6,height=2,ec='blue',fill=False)
	r43 = Rectangle(xy=(13,11),width=6,height=2,ec='blue',fill=False)
	r44 = Rectangle(xy=(13,27),width=6,height=2,ec='blue',fill=False)
	r45 = Rectangle(xy=(21,11),width=6,height=2,ec='blue',fill=False)
	r46 = Rectangle(xy=(21,27),width=6,height=2,ec='blue',fill=False)
	r47 = Rectangle(xy=(33,11),width=6,height=2,ec='blue',fill=False)
	r48 = Rectangle(xy=(33,27),width=6,height=2,ec='blue',fill=False)
	r49 = Rectangle(xy=(41,11),width=6,height=2,ec='blue',fill=False)
	r50 = Rectangle(xy=(41,27),width=6,height=2,ec='blue',fill=False)
	r51 = Rectangle(xy=(53,11),width=6,height=2,ec='blue',fill=False)
	r52 = Rectangle(xy=(53,27),width=6,height=2,ec='blue',fill=False)
	r53 = Rectangle(xy=(61,11),width=6,height=2,ec='blue',fill=False)
	r54 = Rectangle(xy=(61,27),width=6,height=2,ec='blue',fill=False)
	r55 = Rectangle(xy=(73,11),width=6,height=2,ec='blue',fill=False)
	r56 = Rectangle(xy=(73,27),width=6,height=2,ec='blue',fill=False)

	fig = plt.figure(figsize=(12, 8))
	ax0 = fig.add_subplot(1,2,1)
	ax1 = fig.add_subplot(1,2,2)

	ax0.axvline(20, color = 'red')
	ax0.axvline(40, color = 'red')
	ax0.axvline(60, color = 'red')

	ax1.axvline(20, color = 'red')
	ax1.axvline(40, color = 'red')
	ax1.axvline(60, color = 'red')

	ax0.add_patch(r1)
	ax0.add_patch(r2)
	ax0.add_patch(r3)
	ax0.add_patch(r4)
	ax0.add_patch(r5)
	ax0.add_patch(r6)
	ax0.add_patch(r7)
	ax0.add_patch(r8)
	ax0.add_patch(r9)
	ax0.add_patch(r10)
	ax0.add_patch(r11)
	ax0.add_patch(r12)
	ax0.add_patch(r13)
	ax0.add_patch(r14)
	ax0.add_patch(r15)
	ax0.add_patch(r16)
	ax0.add_patch(r17)
	ax0.add_patch(r18)
	ax0.add_patch(r19)
	ax0.add_patch(r20)
	ax0.add_patch(r21)
	ax0.add_patch(r22)
	ax0.add_patch(r23)
	ax0.add_patch(r24)
	ax0.add_patch(r25)
	ax0.add_patch(r26)
	ax0.add_patch(r27)
	ax0.add_patch(r28)

	ax1.add_patch(r29)
	ax1.add_patch(r30)
	ax1.add_patch(r31)
	ax1.add_patch(r32)
	ax1.add_patch(r33)
	ax1.add_patch(r34)
	ax1.add_patch(r35)
	ax1.add_patch(r36)
	ax1.add_patch(r37)
	ax1.add_patch(r38)
	ax1.add_patch(r39)
	ax1.add_patch(r40)
	ax1.add_patch(r41)
	ax1.add_patch(r42)
	ax1.add_patch(r43)
	ax1.add_patch(r44)
	ax1.add_patch(r45)
	ax1.add_patch(r46)
	ax1.add_patch(r47)
	ax1.add_patch(r48)
	ax1.add_patch(r49)
	ax1.add_patch(r50)
	ax1.add_patch(r51)
	ax1.add_patch(r52)
	ax1.add_patch(r53)
	ax1.add_patch(r54)
	ax1.add_patch(r55)
	ax1.add_patch(r56)

	paths = glob.glob('Desktop/python/image/*')
	num = len(paths)
	lists = [paths[0],paths[int(num) - 1]]

	cutrange = np.array([[129, 133], [196, 133], [126, 157], [194, 156]])

	binimg0 = Binarization(lists[0],cutrange)
	binimg1 = Binarization(lists[1],cutrange)

	ax0.imshow(binimg0, cmap='gray')
	ax1.imshow(binimg1, cmap='gray')

	cutrange = 0

	plt.show()

RangeCheck()