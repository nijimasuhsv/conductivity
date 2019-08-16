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
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def ImgRecognition(binimg,path):
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
		text1.insert(tk.END,path + ' is unreadable\n')
		return 0

	return recvalue

def main():
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	text1.insert(tk.END,'[{0:%Y/%m/%d %H:%M:%S}] start Reading\n'.format(now))
	
	if not imgdir.get():
		text1.insert(tk.END,'Please choose your input dir\n')
		return
	elif not outputpath.get():
		text1.insert(tk.END,'Please choose your output dir\n')
		return

	if not tl_x.get() or not tl_y.get() or not tr_x.get() or not tr_y.get() or not bl_x.get() or not bl_y.get() or not br_x.get() or not br_y.get():
		text1.insert(tk.END,'Please enter all coordinates\n')
		return

	inputpaths = imgdir.get() + '/*'
	outputpaths = outputpath.get() + '/output_{0:%Y%m%d%H%M%S}.csv'

	paths = glob.glob(inputpaths)

	cutrange = np.array([[tl_x.get(), tl_y.get()], [tr_x.get(), tr_y.get()], [bl_x.get(), bl_y.get()], [br_x.get(), br_y.get()]])

	output = []
###
	for path in paths:
		binimg = Binarization(path,cutrange)

		ans = ImgRecognition(binimg,path)

		output.append([ans])

		text1.insert(tk.END,'-')
###

	with open(outputpaths.format(now),'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(output)

	text1.insert(tk.END,'Done.\n')

######################################################################
# binarization test

def MakeGraphs():
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	text1.insert(tk.END,'[{0:%Y/%m/%d %H:%M:%S}] test Drawing\n'.format(now))
	
	if not imgdir.get():
		text1.insert(tk.END,'Please choose your input dir\n')
		return

	if not tl_x.get() or not tl_y.get() or not tr_x.get() or not tr_y.get() or not bl_x.get() or not bl_y.get() or not br_x.get() or not br_y.get():
		text1.insert(tk.END,'Please enter all coordinates\n')
		return

	inputpaths = imgdir.get() + '/*'

	paths = glob.glob(inputpaths)

	cutrange = []
	cutrange = np.array([[tl_x.get(), tl_y.get()], [tr_x.get(), tr_y.get()], [bl_x.get(), bl_y.get()], [br_x.get(), br_y.get()]])

	num = len(paths)
	lists = [paths[0],paths[int(num) - 1]]

	testbinimg0 = Binarization(lists[0],cutrange)
	testbinimg1 = Binarization(lists[1],cutrange)

	ax0.cla()
	ax1.cla()

	ax0.imshow(testbinimg0, cmap='gray')
	ax1.imshow(testbinimg1, cmap='gray')
	
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
	ax1.add_patch(r57)

	canvas.draw()

######################################################################
# tkinter define

def SelectFile():
	iDir = os.path.abspath(os.path.dirname(__file__))
	dirpath = tk.filedialog.askdirectory(initialdir = iDir)
	imgdir.set(dirpath)

def SelectOFile():
	iDir = os.path.abspath(os.path.dirname(__file__))
	dirpath = tk.filedialog.askdirectory(initialdir = iDir)
	outputpath.set(dirpath)

######################################################################
# tkinter main

root = tk.Tk()
root.title('Recognizing digits Program')
root.geometry('900x550')
root.resizable(0,0)

main1 = tk.LabelFrame(root,bd=2,text='1.Image Path')
main2 = tk.Frame(root)
main3 = tk.LabelFrame(root,bd=2,text='2.XY coordinates')
main4 = tk.LabelFrame(root,bd=2,text='3.Binarization test')
main5 = tk.LabelFrame(root,bd=2,text='4.Recognizing digits')
main6 = tk.Frame(root,bd=2)

button1 = ttk.Button(main1,text='Brows',command=SelectFile)
button2 = ttk.Button(main4,text='Draw',command=MakeGraphs,width=20)
button3 = ttk.Button(main5,text='Read',command=main,width=20)
button4 = ttk.Button(main1,text='Brows',command=SelectOFile)

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
label17 = ttk.Label(main1,text='input  :')
label18 = ttk.Label(main1,text='output :')

imgdir = tk.StringVar()
imgdir_entry = ttk.Entry(main1, textvariable=imgdir, width=50)
imgdir_entry.insert(tk.END,'C:/Users/Kenta.M/Desktop/python/image')
outputpath = tk.StringVar()
outputpath_entry = ttk.Entry(main1, textvariable=outputpath, width=50)
outputpath_entry.insert(tk.END,'C:/Users/Kenta.M/Desktop/python/output_csv')
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
tl_x_entry.insert(tk.END,'129')
tl_y_entry.insert(tk.END,'133')
tr_x_entry.insert(tk.END,'196')
tr_y_entry.insert(tk.END,'133')
bl_x_entry.insert(tk.END,'126')
bl_y_entry.insert(tk.END,'157')
br_x_entry.insert(tk.END,'194')
br_y_entry.insert(tk.END,'156')

text1 = tk.Text(main6, width=60, height=7,bd=5)

scrollbar = tk.Scrollbar(main6, command=text1.yview)

fig = plt.figure(figsize=(4, 5))
ax0 = fig.add_subplot(2,1,1)
ax1 = fig.add_subplot(2,1,2)
canvas = FigureCanvasTkAgg(fig, master=main2)

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
r30 = Rectangle(xy=(5,4),width=10,height=2,ec='blue',fill=False)
r31 = Rectangle(xy=(25,4),width=10,height=2,ec='blue',fill=False)
r32 = Rectangle(xy=(45,4),width=10,height=2,ec='blue',fill=False)
r33 = Rectangle(xy=(65,4),width=10,height=2,ec='blue',fill=False)
r34 = Rectangle(xy=(5,19),width=10,height=2,ec='blue',fill=False)
r35 = Rectangle(xy=(25,19),width=10,height=2,ec='blue',fill=False)
r36 = Rectangle(xy=(45,19),width=10,height=2,ec='blue',fill=False)
r37 = Rectangle(xy=(65,19),width=10,height=2,ec='blue',fill=False)
r38 = Rectangle(xy=(5,34),width=10,height=2,ec='blue',fill=False)
r39 = Rectangle(xy=(25,34),width=10,height=2,ec='blue',fill=False)
r40 = Rectangle(xy=(45,34),width=10,height=2,ec='blue',fill=False)
r41 = Rectangle(xy=(65,34),width=10,height=2,ec='blue',fill=False)
r42 = Rectangle(xy=(3,6),width=2,height=13,ec='blue',fill=False)
r43 = Rectangle(xy=(3,21),width=2,height=13,ec='blue',fill=False)
r44 = Rectangle(xy=(15,6),width=2,height=13,ec='blue',fill=False)
r45 = Rectangle(xy=(15,21),width=2,height=13,ec='blue',fill=False)
r46 = Rectangle(xy=(23,6),width=2,height=13,ec='blue',fill=False)
r47 = Rectangle(xy=(23,21),width=2,height=13,ec='blue',fill=False)
r48 = Rectangle(xy=(35,6),width=2,height=13,ec='blue',fill=False)
r49 = Rectangle(xy=(35,21),width=2,height=13,ec='blue',fill=False)
r50 = Rectangle(xy=(43,6),width=2,height=13,ec='blue',fill=False)
r51 = Rectangle(xy=(43,21),width=2,height=13,ec='blue',fill=False)
r52 = Rectangle(xy=(55,6),width=2,height=13,ec='blue',fill=False)
r53 = Rectangle(xy=(55,21),width=2,height=13,ec='blue',fill=False)
r54 = Rectangle(xy=(63,6),width=2,height=13,ec='blue',fill=False)
r55 = Rectangle(xy=(63,21),width=2,height=13,ec='blue',fill=False)
r56 = Rectangle(xy=(75,6),width=2,height=13,ec='blue',fill=False)
r57 = Rectangle(xy=(75,21),width=2,height=13,ec='blue',fill=False)

root.grid_columnconfigure((0,1,2), weight=1)
root.grid_rowconfigure((0, 1, 2, 3), weight=1)

main1.grid(row=0,column=1,columnspan=2,padx=10,pady=10,sticky='nsew')
main2.grid(row=0,column=0,rowspan=4,padx=10,pady=10,sticky='nsew')
main3.grid(row=1,column=1,rowspan=2,padx=10,pady=10,sticky='nsew')
main4.grid(row=1,column=2,padx=10,pady=10,sticky='nsew')
main5.grid(row=2,column=2,padx=10,pady=10,sticky='nsew')
main6.grid(row=3,column=1,columnspan=2,padx=10,pady=10,sticky='nsew')

button1.grid(row=0,column=2)
button2.grid(row=0,column=0,padx=10,pady=10)
button3.grid(row=0,column=0,padx=10,pady=10)
button4.grid(row=1,column=2)

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
label18.grid(row=1,column=0)

imgdir_entry.grid(row=0, column=1)
outputpath_entry.grid(row=1, column=1)
tl_x_entry.grid(row=0,column=2)
tl_y_entry.grid(row=0,column=4)
tr_x_entry.grid(row=1,column=2)
tr_y_entry.grid(row=1,column=4)
bl_x_entry.grid(row=2,column=2)
bl_y_entry.grid(row=2,column=4)
br_x_entry.grid(row=3,column=2)
br_y_entry.grid(row=3,column=4)

scrollbar.grid(row=0,column=1,sticky='ns')

text1.grid(row=0,column=0)
text1.config(yscrollcommand=scrollbar.set)

canvas.get_tk_widget().grid(row=0,column=0)

starttime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
text1.insert(tk.END,'[{0:%Y/%m/%d %H:%M:%S}] system startup\n'.format(starttime))

MakeGraphs()

root.mainloop()