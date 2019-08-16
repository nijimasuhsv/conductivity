def Binarization(PictPath,CutRange):

	# �摜���O���[�X�P�[���œǂݍ���
	img = cv2.imread(PictPath, cv2.IMREAD_GRAYSCALE)

	# pts1:�摜�؂�o����4�_���w��Apts2:�؂�o����̉摜�T�C�Y(�s�N�Z��)
	pts1 = np.float32(CutRange)
	pts2 = np.float32([[0,0],[80,0],[0,40],[80,40]])

	# �؂�o��
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(img,M,(80,40))

	# �����_�̍폜
	decimalpoint = [37,40,35,58]
	xmin, xmax, ymin, ymax = decimalpoint
	dst[ymin:ymax+1, xmin:xmax+1] = dst[0, 0]

	# ������(�ڂ���)
	blur = cv2.GaussianBlur(dst,(9,9),2)

	# ��l��
	th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)

	# �����t�H���W�[����
	kernel = np.ones((2,2),np.uint8)
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	
	return opening
	
path = 'Desktop/python/test2.jpg'
cut = [[131, 130], [197, 130], [129, 155], [195, 155]]

binimg = Binarization(path,cut)

plt.imshow(binimg, cmap='gray')

plt.show()