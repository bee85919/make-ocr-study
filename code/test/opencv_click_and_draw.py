import cv2
import pandas as pd
img_path = 'C:\Users\bee85\Desktop\make\make-ocr-study\data\img\prescription.png'
db_path = 'C:\Users\bee85\Desktop\make\make-ocr-study\data\db\test.csv'
title = 'test'

drawing = False # 마우스가 클릭된 상태 확인용
img_x, img_y = -1, -1
img_history = [] # 이미지 이력을 저장할 리스트
img_coordinates = [] #이미지 포인트 저장

# 마우스 콜백 함수
def draw_rectangle(event, x, y, flags, param):
    global img_x,img_y,drawing,img_history

    if event == cv2.EVENT_LBUTTONDOWN: # 마우스를 누른 상태
        drawing = True 
        img_x,img_y = x,y
        img_history.append(img.copy()) # 복사본 저장
    elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
        if drawing == True: # 마우스를 누른 상태 일경우
            img[:] = img_history[-1][:] # 마지막 저장된 이미지로 복원
            cv2.rectangle(img,(img_x,img_y),(x,y),(0,0,255),2) # 빨간색으로 테두리 그리기
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False; # 마우스를 때면 상태 변경
        cv2.rectangle(img,(img_x,img_y),(x,y),(0,0,255),2) # 빨간색으로 테두리 그리기
        img_coordinates.append({ 'id' : len(img_coordinates) , 'x1' : img_x, 'y1' : img_y, 'x2' : x, 'y2' : y})
        print(f"start : ({img_x},{img_y}), end : ({x},{y})")

img = cv2.imread(img_path)
cv2.namedWindow(title)
cv2.setMouseCallback(title,draw_rectangle)

while True:
    cv2.imshow(title,img)
    k = cv2.waitKey(10) & 0xFF
    if k == 27: # ESC 키를 누르면 종료
        break
    elif k == ord('z') and len(img_history) >= 1: # Ctrl + z를 누르면 마지막 그림을 지움
       
        img[:] = img_history[-1][:] # 마지막 저장된 이미지로 복원
        img_history.pop() # 가장 최근의 이력 제거
        img_coordinates.pop()
        
    elif k == ord('s'): # s를 누르면 이미지 저장
        cv2.imwrite('saved_image.jpg', img)

cv2.destroyAllWindows()
df = pd.DataFrame(img_coordinates)
df.to_csv(db_path, index=False)

