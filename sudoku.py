import cv2
import sys
import numpy as np
import sudoku_solver 
import operator

#######   training part    ############### 
sudoku = np.zeros((9,9))
model = cv2.ml.KNearest_create()
print('Started training model...')
for i in range (2,6):
	samples   = np.loadtxt('train/generalsamples'+str(i)+'.data',np.float32)
	responses = np.loadtxt('train/generalresponses'+str(i)+'.data',np.float32)
	responses = responses.reshape((responses.size,1))
	model.train(samples,cv2.ml.ROW_SAMPLE,responses)
print('Model trained.')

####### sudoku extraction part ###########
def check_square(x,y,h):
	sq_size=h/9
	square=[x/sq_size,y/sq_size]
	return square

def check_for_font(font_h):
		max,font_size = -1, 0
		for i in font_h:
			count=0
			for j in font_h:
				if abs(j-i)<10:
					count+=1
			if count>max:
				max=count
				font_size=i
		return font_size

def ocr_start(contours,im):

		out = np.zeros(im.shape,np.uint8)
		height=im.shape[0]
		font_h=[]
		thresh = height/9
		contour_rect=[]
		for cnt in contours:
			if cv2.contourArea(cnt)>50:
				[x,y,w,h] = cv2.boundingRect(cnt)
				if h<thresh-10 and h>thresh/4 and w>thresh/6 and w<thresh-10 :       	
					font_h.append(h)
					contour_rect.append([x,y,w,h])
		font_size = check_for_font(font_h)
		for rect in contour_rect:
					[x,y,w,h] = rect
					if abs(h-font_size) < thresh/10:
						cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),1)
						roi = im[y:y+h,x:x+w]
						roismall = cv2.resize(roi,(40,40))
						roismall = roismall.reshape((1,1600)).astype(np.float32)
						retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
						square = check_square(x+w/2,y+h/2,height)
						sudoku [square[1]][square[0]]=results[0][0]


def distance(a, b):
		return np.sqrt( ((a[0] - b[0]) **2) + ((a[1] - b[1]) **2) )

def extract_contour(image):
		contours, h = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		return contours

def CutoutMaxContour(image):
        contours = extract_contour(image)
        return getContourCorners(max(contours, key=cv2.contourArea))

def getContourCorners(contour):
	bottom_right, _ = max(enumerate([point[0][0] + point[0][1] for point in contour]), key=operator.itemgetter(1))
	bottom_left	, _ = max(enumerate([point[0][0] - point[0][1] for point in contour]), key=operator.itemgetter(1))
	top_right	, _ = min(enumerate([point[0][0] - point[0][1] for point in contour]), key=operator.itemgetter(1))
	top_left	, _ = min(enumerate([point[0][0] + point[0][1] for point in contour]), key=operator.itemgetter(1))

	sudoku_corners=[contour[top_left][0],contour[top_right][0],contour[bottom_left][0],contour[bottom_right][0]]
	return sudoku_corners

def Linear_transform_image(image, crop_rectangle):
	
	side = max(distance(pointA,pointB) for pointA in crop_rectangle for pointB in crop_rectangle)

	source_polygon = np.array(crop_rectangle, dtype='float32')
	dest_square = np.array([[0, 0],[0, side - 1],[side - 1, 0],[side - 1, side - 1],], dtype='float32')
 
	m = cv2.getPerspectiveTransform(source_polygon, dest_square)
	return cv2.warpPerspective(image, m, (int(side), int(side)))


def preprocess(image):

	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
	image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

	blur=len(image)/100
	blur = blur+(blur+1)%2;
	image = cv2.GaussianBlur(image,(blur,blur), 0)

	image = 255 - cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 17, 5)

	return image
	

def main():
		if len(sys.argv) != 2:
			print('Execution style: python sudoku.py sample/image1.jpg')
			return
		img = cv2.imread(sys.argv[1])
		preprocessed_image = preprocess(img)

		sudoku_corners = CutoutMaxContour(preprocessed_image)

		sudoku_img = Linear_transform_image(img, sudoku_corners)

		sudoku_img = preprocess(sudoku_img)

		ocr_start(extract_contour(sudoku_img) ,sudoku_img)
		
		sudoku_solver.start_solving(sudoku)


if __name__ == '__main__':
	main()