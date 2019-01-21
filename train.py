import sys
import operator
import numpy as np
import cv2


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

def ocr_start(contours,im,count):
        samples =  np.empty((0,1600))
        responses = []
        keys = [i for i in range(48,58)]
        # samples = np.loadtxt('train/generalsamples.data',np.float32)
        # responses = np.loadtxt('train/generalresponses.data',np.float32)
        # responses = responses.reshape((responses.size,1))
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
                    if abs(h-font_size) < 15:
                        cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),1)
                        roi = im[y:y+h,x:x+w]
                        roismall = cv2.resize(roi,(40,40))
                        cv2.imshow('im',im)
                        cv2.imshow('norm',roismall)
                        key = cv2.waitKey(0)

                        if key == 27:  # (escape to quit)
                            sys.exit()
                        elif key in keys:
                            responses.append(int(chr(key)))
                            print(roismall)
                            sample = roismall.reshape((1,1600))
                            print(sample)
                            samples = np.append(samples,sample,0)
                            print key
        responses = np.array(responses,np.float32)
        responses = responses.reshape((responses.size,1))
        print "training complete"
        np.savetxt('generalsamples'+str(count)+'.data',samples)
        np.savetxt('generalresponses'+str(count)+'.data',responses)

def distance(a, b):
        return np.sqrt( ((a[0] - b[0]) **2) + ((a[1] - b[1]) **2) )

def extract_contour(image):
        contours, h = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

def CutoutMaxContour(image):
        contours = extract_contour(image)
        return getContourCorners(max(contours, key=cv2.contourArea))

def show(img, windowName='Image'):
        screen_res = 1280.0, 720.0
        scale_width = screen_res[0] / img.shape[1]
        scale_height = screen_res[1] / img.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(img.shape[1] * scale)
        window_height = int(img.shape[0] * scale)

        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, window_width, window_height)

        cv2.imshow(windowName, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def getContourCorners(contour):
    bottom_right, _ = max(enumerate([point[0][0] + point[0][1] for point in contour]), key=operator.itemgetter(1))
    bottom_left , _ = max(enumerate([point[0][0] - point[0][1] for point in contour]), key=operator.itemgetter(1))
    top_right   , _ = min(enumerate([point[0][0] - point[0][1] for point in contour]), key=operator.itemgetter(1))
    top_left    , _ = min(enumerate([point[0][0] + point[0][1] for point in contour]), key=operator.itemgetter(1))

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

    # show(image)
    return image
    

def main():
    count=0
    for i in range (1,15):
        count+=1
        img = cv2.imread('sample/image'+str(i)+'.jpg')
        # show(img)
        preprocessed_image = preprocess(img)

        sudoku_corners = CutoutMaxContour(preprocessed_image)

        sudoku_img = Linear_transform_image(img, sudoku_corners)
        # show(sudoku_img)
        # cv2.imwrite('train/train.jpg',sudoku_img)
        sudoku_img = preprocess(sudoku_img)
        ocr_start(extract_contour(sudoku_img) ,sudoku_img,count)

if __name__ == '__main__':
    main()