import cv2
import numpy as np

# 載入人臉偵測模型和帽子、葉子圖片
detector = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
hat = cv2.imread('images/bird-hat.png', -1)  # 帽子圖片
leaf1 = cv2.imread('images/leaf.png', -1)  # 第一張葉子圖片（左邊）
leaf2 = cv2.imread('images/leaf2.png', -1)  # 第二張葉子圖片（上方）

cap = cv2.VideoCapture(0)  # 開啟攝影機

# 設定葉子掉落的初始位置
leaf1_x, leaf1_y = -1, -1  # 第一張葉子初始位置
leaf2_x, leaf2_y = -1, -1  # 第二張葉子初始位置

while True:
    ret, frame = cap.read()  # 讀取每一幀
    if not ret:
        break

    # 轉換為灰階圖片
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 偵測人臉
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # 計算帽子的位置
        hat_width = w  # 帽子的寬度等於臉部的寬度
        hat_height = int(hat.shape[0] * (hat_width / hat.shape[1]))  # 調整帽子的高度
        resized_hat = cv2.resize(hat, (hat_width, hat_height))

        # 設定帽子位置
        hat_x = x
        hat_y = y - int(hat_height * 0.3)  # 稍微讓帽子放得高一點

        # 確保帽子不會超出畫面
        if hat_y < 0:
            hat_y = 0

        # 帽子圖層處理
        for c in range(0, 3):  # 3個通道：BGR
            frame[hat_y:hat_y + resized_hat.shape[0], hat_x:hat_x + resized_hat.shape[1], c] = \
                frame[hat_y:hat_y + resized_hat.shape[0], hat_x:hat_x + resized_hat.shape[1], c] * \
                (1 - resized_hat[:, :, 3] / 255.0) + \
                resized_hat[:, :, c] * (resized_hat[:, :, 3] / 255.0)

    # 計算葉子1的位置（左邊）
    if leaf1_x == -1 and leaf1_y == -1:
        leaf1_x = 50  # 設定葉子1在畫面的左邊
        leaf1_y = 50  # 初始位置稍微上方

    leaf1_y += 1  # 每幀葉子1下落的速度

    # 確保葉子1不會超出畫面
    height, width = frame.shape[:2]
    if leaf1_y + leaf1.shape[0] > height:
        leaf1_y = height - leaf1.shape[0]

    # 計算葉子2的位置（上方）
    if leaf2_x == -1 and leaf2_y == -1:
        leaf2_x = width - 100  # 設定葉子2在畫面的右邊
        leaf2_y = 50  # 初始位置稍微上方

    leaf2_y += 1  # 每幀葉子2下落的速度

    # 確保葉子2不會超出畫面
    if leaf2_y + leaf2.shape[0] > height:
        leaf2_y = height - leaf2.shape[0]

    # 葉子圖層處理：第一張葉子 (左邊)
    for c in range(0, 3):  # 3個通道：BGR
        frame[leaf1_y:leaf1_y + leaf1.shape[0], leaf1_x:leaf1_x + leaf1.shape[1], c] = \
            frame[leaf1_y:leaf1_y + leaf1.shape[0], leaf1_x:leaf1_x + leaf1.shape[1], c] * \
            (1 - leaf1[:, :, 3] / 255.0) + \
            leaf1[:, :, c] * (leaf1[:, :, 3] / 255.0)

    # 葉子圖層處理：第二張葉子 (上方)
    for c in range(0, 3):  # 3個通道：BGR
        frame[leaf2_y:leaf2_y + leaf2.shape[0], leaf2_x:leaf2_x + leaf2.shape[1], c] = \
            frame[leaf2_y:leaf2_y + leaf2.shape[0], leaf2_x:leaf2_x + leaf2.shape[1], c] * \
            (1 - leaf2[:, :, 3] / 255.0) + \
            leaf2[:, :, c] * (leaf2[:, :, 3] / 255.0)

    # 設定邊框顏色：白灰色 (RGB: 200, 200, 200)
    border_color = (200, 200, 200)  # 白灰色
    thickness = 10  # 邊框的厚度
    height, width = frame.shape[:2]

    # 固定的邊框大小，從畫面的最邊邊繪製
    frame = cv2.rectangle(frame, (0, 0), (width, height), border_color, thickness)

    # 顯示畫面
    cv2.imshow("Face with Hat, Falling Leaves (Left and Top)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝影機並關閉所有視窗
cap.release()
cv2.destroyAllWindows()