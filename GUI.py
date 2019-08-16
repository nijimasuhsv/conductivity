######################################################################
# cv2 import
import cv2
import csv
import pytz
import glob
import datetime
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

######################################################################
# tkinter import
import os,sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

######################################################################
# cv2 define
def Binarization(PictPath,CutRange):
	GreyImg = cv2.imread(PictPath, cv2.IMREAD_GRAYSCALE)

	pts1 = np.float32(CutRange)
	pts2 = np.float32(np.array([[0,0],[80,0],[0,40],[80,40]]))

	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(GreyImg,M,(80,40))

	decimalpoint = [37,40,35,58]
	decxmin, decxmax, decymin, decymax = decimalpoint
	dst[decymin:decymax+1, decxmin:decxmax+1] = dst[0, 0]

	blur = cv2.GaussianBlur(dst,(9,9),2)

	th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)

	kernel = np.ones((2,2),np.uint8)
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)

	return opening

def SegJudge(digit,binimg):
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

def ImgRecognition(binimg):
	thousand = np.array([[6,4,10,2],[6,19,10,2],[6,34,10,2],[4,6,2,13],[4,21,2,13],[16,6,2,13],[16,21,2,13]])
	hundred = np.array([[26,4,10,2],[26,19,10,2],[26,34,10,2],[24,6,2,13],[24,21,2,13],[36,6,2,13],[36,21,2,13]])
	ten = np.array([[46,4,10,2],[46,19,10,2],[46,34,10,2],[44,6,2,13],[44,21,2,13],[56,6,2,13],[56,21,2,13]])
	one = np.array([[66,4,10,2],[66,19,10,2],[66,34,10,2],[64,6,2,13],[64,21,2,13],[76,6,2,13],[76,21,2,13]])
	places = [thousand,hundred,ten,one]
	value = []

	for place in places:
		value.append(SegJudge(place,binimg))

	try:
		recvalue = value[0] * 1000 + value[1] * 100 + value[2] *10 + value[3]
	except TypeError:
		print(path + ' is unreadable')
		return 0

	return recvalue

def main():
	paths = glob.glob('c:/Users/Kenta.M/Desktop/python/image/*')

	cutrange = np.array([[129, 133], [196, 133], [126, 157], [194, 156]])

	output = []
###
	for path in paths:
		binimg = Binarization(path,cutrange)

		ans = ImgRecognition(binimg)

		output.append([ans])

		print('-',end='')
###

	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

	with open('c:/Users/Kenta.M/Desktop/python/output_csv/output_{0:%Y%m%d%H%M%S}.csv'.format(now),'w', newline="") as f:
		writer = csv.writer(f)
		writer.writerows(output)

	print('Done.')

######################################################################
# tkinter define

def SelectFile():
	iDir = os.path.abspath(os.path.dirname(__file__))
	dirpath = tk.filedialog.askdirectory(initialdir = iDir)
	imgdir.set(dirpath)


def DrawBinImage():
	dirpaths = imgdir.get() + '/*'
	print(dirpaths)
	#RangeCheck(dirpaths)

def GetXYCoordinates():
	XY = []
	XY[0] = tl_x.get()
	XY[1] = tl_y.get()
	XY[2] = tr_x.get()
	XY[3] = tr_y.get()
	XY[4] = bl_x.get()
	XY[5] = bl_y.get()
	XY[6] = br_x.get()
	XY[7] = br_y.get()
	
	


######################################################################
# tkinter main


root = tk.Tk()
root.title('Recognizing digits Program')
root.geometry('500x400')
root.resizable(0,0)

main1 = tk.LabelFrame(root,bd=2,text='1.Image Path')
main2 = tk.Frame(root)
main3 = tk.LabelFrame(root,bd=2,text='2.XY coordinates')
main4 = tk.LabelFrame(root,bd=2,text='3.Binarization test')
main5 = tk.LabelFrame(root,bd=2,text='4.Recognizing digits')

button1 = ttk.Button(main1,text='Brows',command=SelectFile)
button2 = ttk.Button(main4,text='Draw',command=DrawBinImage,width=20)
button3 = ttk.Button(main5,text='Read',command=main,width=20)

label1 = ttk.Label(main3,text='Top left :')
label2 = ttk.Label(main3,text='Top right :')
label3 = ttk.Label(main3,text='Bottom left :')
label4 = ttk.Label(main3,text='Bottom right :')
label5 = ttk.Label(main3,text='(')
label6 = ttk.Label(main3,text='(')
label7 = ttk.Label(main3,text='(')
label8 = ttk.Label(main3,text='(')
label9 = ttk.Label(main3,text=',')
label10 = ttk.Label(main3,text=',')
label11 = ttk.Label(main3,text=',')
label12 = ttk.Label(main3,text=',')
label13 = ttk.Label(main3,text=')')
label14 = ttk.Label(main3,text=')')
label15 = ttk.Label(main3,text=')')
label16 = ttk.Label(main3,text=')')

label17 = ttk.Label(main2,text='test')

imgdir = tk.StringVar()
imgdir_entry = ttk.Entry(main1, textvariable=imgdir, width=50)
tl_x = tk.StringVar()
tl_x_entry = ttk.Entry(main3,textvariable=tl_x,width=5)
tl_y = tk.StringVar()
tl_y_entry = ttk.Entry(main3,textvariable=tl_y,width=5)
tr_x = tk.StringVar()
tr_x_entry = ttk.Entry(main3,textvariable=tr_x,width=5)
tr_y = tk.StringVar()
tr_y_entry = ttk.Entry(main3,textvariable=tr_y,width=5)
bl_x = tk.StringVar()
bl_x_entry = ttk.Entry(main3,textvariable=bl_x,width=5)
bl_y = tk.StringVar()
bl_y_entry = ttk.Entry(main3,textvariable=bl_y,width=5)
br_x = tk.StringVar()
br_x_entry = ttk.Entry(main3,textvariable=br_x,width=5)
br_y = tk.StringVar()
br_y_entry = ttk.Entry(main3,textvariable=br_y,width=5)

root.grid_columnconfigure((0,1), weight=1)
root.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

main1.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky="nsew")
main2.grid(row=1,column=0,columnspan=2,rowspan=2,padx=10,pady=10,sticky="nsew")
main3.grid(row=3,column=0,rowspan=2,padx=10,pady=10,sticky="nsew")
main4.grid(row=3,column=1,padx=10,pady=10,sticky="nsew")
main5.grid(row=4,column=1,padx=10,pady=10,sticky="nsew")

button1.grid(row=0,column=2)
button2.grid(row=0,column=0,padx=10,pady=10)
button3.grid(row=0,column=0,padx=10,pady=10)

label1.grid(row=0,column=0)
label2.grid(row=1,column=0)
label3.grid(row=2,column=0)
label4.grid(row=3,column=0)
label5.grid(row=0,column=1)
label6.grid(row=1,column=1)
label7.grid(row=2,column=1)
label8.grid(row=3,column=1)
label9.grid(row=0,column=3)
label10.grid(row=1,column=3)
label11.grid(row=2,column=3)
label12.grid(row=3,column=3)
label13.grid(row=0,column=5)
label14.grid(row=1,column=5)
label15.grid(row=2,column=5)
label16.grid(row=3,column=5)

label17.grid(row=0,column=0)

imgdir_entry.grid(row=0, column=1)
tl_x_entry.grid(row=0,column=2)
tl_y_entry.grid(row=0,column=4)
tr_x_entry.grid(row=1,column=2)
tr_y_entry.grid(row=1,column=4)
bl_x_entry.grid(row=2,column=2)
bl_y_entry.grid(row=2,column=4)
br_x_entry.grid(row=3,column=2)
br_y_entry.grid(row=3,column=4)

root.mainloop()