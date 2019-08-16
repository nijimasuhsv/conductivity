def RangeSelect(Rx,Ry,Rwidth,Rheight):
	r = Rectangle(Rx,Ry,Rwidth,Rheight,color='blue',fill=False)
	ax.add_patch(r)
	
# lh:left high
# ll:left low
# rh:right high
# rl:right low
# mh:middle high
# mm:middle middle
# ml:middle low

mh = [5,4,10,2]

x = mh[0]
y = mh[1]
width = mh[2]
height = mh[3]

RangeSelect(str(x),str(y),str(width),str(height))

plt.show()

###############################################################

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
     (1,0,1,1,1,1,1): 0
}

xmins = [5,3]
xmaxs = [15,5]
ymins = [4,6]
ymaxs = [6,19]

for xmin,xmax,ymin,ymax in zip(xmins,xmaxs,ymins,ymaxs):

    cut = opening[ymin:ymax, xmin:xmax]

    total = cv2.countNonZero(cut)

    print(total)

#####################################################################

# 画像をグレースケールで読み込み
img = cv2.imread('Desktop/python/test.jpg', cv2.IMREAD_GRAYSCALE)

# pts1:画像切り出しの4点を指定、pts2:切り出し後の画像サイズ(ピクセル)
pts1 = np.float32([[131, 130], [197, 130], [129, 155], [195, 155]])
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

thousand = np.array([[5,4,10,2],[5,19,10,2],[5,34,10,2],[3,6,2,13],[3,21,2,13],[15,6,2,13],[15,21,2,13]])
hundred = np.array([[25,4,10,2],[25,19,10,2],[25,34,10,2],[23,6,2,13],[23,21,2,13],[35,6,2,13],[35,21,2,13]])
ten = np.array([[45,4,10,2],[45,19,10,2],[45,34,10,2],[43,6,2,13],[43,21,2,13],[55,6,2,13],[55,21,2,13]])
one = np.array([[65,4,10,2],[65,19,10,2],[65,34,10,2],[63,6,2,13],[63,21,2,13],[75,6,2,13],[75,21,2,13]])
list = []
def test(digit):
    for t in range(7):
        xmin = digit[t,0]
        xmax = xmin + digit[t,2]
        ymin = digit[t,1]
        ymax = ymin + digit[t,3]
        cut = opening[ymin:ymax, xmin:xmax]
        total = cv2.countNonZero(cut)
        #print(total)
        if total < 26 * 0.2:
            bw = 1
        else:
            bw = 0
    
        list.append(bw)
    
    #print(list)    
    num = dictionary[tuple(list)]
    
    print(num)
    
plt.imshow(opening, cmap='gray')

plt.show()

test(thousand)
list = []
test(hundred)
list = []
test(ten)
list = []
test(one)

#############################################################################
ax.axvline(20, color = 'red')
ax.axvline(40, color = 'red')
ax.axvline(60, color = 'red')

r1 = Rectangle(xy=(5,4),width=10,height=2,ec='blue',fill=False)
r2 = Rectangle(xy=(25,4),width=10,height=2,ec='blue',fill=False)
r3 = Rectangle(xy=(45,4),width=10,height=2,ec='blue',fill=False)
r4 = Rectangle(xy=(65,4),width=10,height=2,ec='blue',fill=False)
r5 = Rectangle(xy=(5,19),width=10,height=2,ec='blue',fill=False)
r6 = Rectangle(xy=(25,19),width=10,height=2,ec='blue',fill=False)
r7 = Rectangle(xy=(45,19),width=10,height=2,ec='blue',fill=False)
r8 = Rectangle(xy=(65,19),width=10,height=2,ec='blue',fill=False)
r9 = Rectangle(xy=(5,34),width=10,height=2,ec='blue',fill=False)
r10 = Rectangle(xy=(25,34),width=10,height=2,ec='blue',fill=False)
r11 = Rectangle(xy=(45,34),width=10,height=2,ec='blue',fill=False)
r12 = Rectangle(xy=(65,34),width=10,height=2,ec='blue',fill=False)

r13 = Rectangle(xy=(3,6),width=2,height=13,ec='blue',fill=False)
r14 = Rectangle(xy=(3,21),width=2,height=13,ec='blue',fill=False)
r15 = Rectangle(xy=(15,6),width=2,height=13,ec='blue',fill=False)
r16 = Rectangle(xy=(15,21),width=2,height=13,ec='blue',fill=False)
r17 = Rectangle(xy=(23,6),width=2,height=13,ec='blue',fill=False)
r18 = Rectangle(xy=(23,21),width=2,height=13,ec='blue',fill=False)
r19 = Rectangle(xy=(35,6),width=2,height=13,ec='blue',fill=False)
r20 = Rectangle(xy=(35,21),width=2,height=13,ec='blue',fill=False)
r21 = Rectangle(xy=(43,6),width=2,height=13,ec='blue',fill=False)
r22 = Rectangle(xy=(43,21),width=2,height=13,ec='blue',fill=False)
r23 = Rectangle(xy=(55,6),width=2,height=13,ec='blue',fill=False)
r24 = Rectangle(xy=(55,21),width=2,height=13,ec='blue',fill=False)
r25 = Rectangle(xy=(63,6),width=2,height=13,ec='blue',fill=False)
r26 = Rectangle(xy=(63,21),width=2,height=13,ec='blue',fill=False)
r27 = Rectangle(xy=(75,6),width=2,height=13,ec='blue',fill=False)
r28 = Rectangle(xy=(75,21),width=2,height=13,ec='blue',fill=False)

r29 = Rectangle(xy=(38,34),width=3,height=6,ec='blue',fill=False)
ax.add_patch(r1)
ax.add_patch(r2)
ax.add_patch(r3)
ax.add_patch(r4)
ax.add_patch(r5)
ax.add_patch(r6)
ax.add_patch(r7)
ax.add_patch(r8)
ax.add_patch(r9)
ax.add_patch(r10)
ax.add_patch(r11)
ax.add_patch(r12)
ax.add_patch(r13)
ax.add_patch(r14)
ax.add_patch(r15)
ax.add_patch(r16)
ax.add_patch(r17)
ax.add_patch(r18)
ax.add_patch(r19)
ax.add_patch(r20)
ax.add_patch(r21)
ax.add_patch(r22)
ax.add_patch(r23)
ax.add_patch(r24)
ax.add_patch(r25)
ax.add_patch(r26)
ax.add_patch(r27)
ax.add_patch(r28)
ax.add_patch(r29)

#############################################################################
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

	# 平滑化(ぼかし)
	blur = cv2.GaussianBlur(dst,(9,9),2)

	# 二値化
	th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)

	# モルフォロジー処理
	kernel = np.ones((2,2),np.uint8)
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	
	return opening

r1 = Rectangle(xy=(5,4),width=10,height=2,ec='blue',fill=False)
r2 = Rectangle(xy=(25,4),width=10,height=2,ec='blue',fill=False)
r3 = Rectangle(xy=(45,4),width=10,height=2,ec='blue',fill=False)
r4 = Rectangle(xy=(65,4),width=10,height=2,ec='blue',fill=False)
r5 = Rectangle(xy=(5,19),width=10,height=2,ec='blue',fill=False)
r6 = Rectangle(xy=(25,19),width=10,height=2,ec='blue',fill=False)
r7 = Rectangle(xy=(45,19),width=10,height=2,ec='blue',fill=False)
r8 = Rectangle(xy=(65,19),width=10,height=2,ec='blue',fill=False)
r9 = Rectangle(xy=(5,34),width=10,height=2,ec='blue',fill=False)
r10 = Rectangle(xy=(25,34),width=10,height=2,ec='blue',fill=False)
r11 = Rectangle(xy=(45,34),width=10,height=2,ec='blue',fill=False)
r12 = Rectangle(xy=(65,34),width=10,height=2,ec='blue',fill=False)

r13 = Rectangle(xy=(3,6),width=2,height=13,ec='blue',fill=False)
r14 = Rectangle(xy=(3,21),width=2,height=13,ec='blue',fill=False)
r15 = Rectangle(xy=(15,6),width=2,height=13,ec='blue',fill=False)
r16 = Rectangle(xy=(15,21),width=2,height=13,ec='blue',fill=False)
r17 = Rectangle(xy=(23,6),width=2,height=13,ec='blue',fill=False)
r18 = Rectangle(xy=(23,21),width=2,height=13,ec='blue',fill=False)
r19 = Rectangle(xy=(35,6),width=2,height=13,ec='blue',fill=False)
r20 = Rectangle(xy=(35,21),width=2,height=13,ec='blue',fill=False)
r21 = Rectangle(xy=(43,6),width=2,height=13,ec='blue',fill=False)
r22 = Rectangle(xy=(43,21),width=2,height=13,ec='blue',fill=False)
r23 = Rectangle(xy=(55,6),width=2,height=13,ec='blue',fill=False)
r24 = Rectangle(xy=(55,21),width=2,height=13,ec='blue',fill=False)
r25 = Rectangle(xy=(63,6),width=2,height=13,ec='blue',fill=False)
r26 = Rectangle(xy=(63,21),width=2,height=13,ec='blue',fill=False)
r27 = Rectangle(xy=(75,6),width=2,height=13,ec='blue',fill=False)
r28 = Rectangle(xy=(75,21),width=2,height=13,ec='blue',fill=False)

r29 = Rectangle(xy=(38,34),width=3,height=6,ec='blue',fill=False)

cutrange = np.array([[131, 130], [197, 130], [129, 155], [195, 155]])


paths = glob.glob('Desktop/python/image/*')
num = len(paths)
lists = [paths[0],paths[int(num) - 1]]

fig = plt.figure()
ax = plt.axes()

binimg = Binarization(lists[int(num)],cutrange)

ax.imshow(binimg, cmap='gray')

ax.axvline(20, color = 'red')
ax.axvline(40, color = 'red')
ax.axvline(60, color = 'red')

ax.add_patch(r1)
ax.add_patch(r2)
ax.add_patch(r3)
ax.add_patch(r4)
ax.add_patch(r5)
ax.add_patch(r6)
ax.add_patch(r7)
ax.add_patch(r8)
ax.add_patch(r9)
ax.add_patch(r10)
ax.add_patch(r11)
ax.add_patch(r12)
ax.add_patch(r13)
ax.add_patch(r14)
ax.add_patch(r15)
ax.add_patch(r16)
ax.add_patch(r17)
ax.add_patch(r18)
ax.add_patch(r19)
ax.add_patch(r20)
ax.add_patch(r21)
ax.add_patch(r22)
ax.add_patch(r23)
ax.add_patch(r24)
ax.add_patch(r25)
ax.add_patch(r26)
ax.add_patch(r27)
ax.add_patch(r28)
ax.add_patch(r29)

plt.show()

#######################################################################
def SelectFile(self):
	root.withdraw()
	fTyp = [("","*")]
	iDir = os.path.abspath(os.path.dirname(__file__))
	tk.messagebox.showinfo('program','plz choose file')
	dir = tk.filedialog.askdirectory(initialdir = iDir)
	return dir