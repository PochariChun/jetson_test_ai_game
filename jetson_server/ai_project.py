
import cv2
import mediapipe as mp
import numpy as np
import torch
import math

# from utils import preprocess
# from dataset import ImageClassificationDataset
# ################################
# # MQTT_HOST = '192.168.240.22'
# MQTT_HOST = '192.168.100.100'
# MQTT_PASSWORD = 'student'
# MQTT_USER = 'student'
# MQTT_CLIENT = 'game' 
# MQTT_TOPIC = '/game'

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         client.connected_flag = True
#         #client.subscribe("/game")
#         print("Connected with code %d" % rc)

# mqtt_client = mqtt.Client(MQTT_CLIENT)
# mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
# mqtt_client.on_connect = on_connect
# mqtt_client.connect(MQTT_HOST,port=1883, keepalive=600)
# mqtt_client.loop_start()
# print("mqtt_client")
# ################################
# camera = USBCamera(width=224, height=224, capture_device=0)
# camera.running = True

# 初始化GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    return cap

def calculate_angle(vector1, vector2):
    # 计算两个向量之间的夹角（以弧度为单位）
    angle_radians = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))
    # 将夹角从弧度转换为度
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees

def detect_gestures(cap):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    frame_count = 0
    fire_action = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image from camera")
            break
        
        frame = cv2.flip(frame, 1)  # 水平翻转画面以反转左右方向
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_RGB)
        
        frame_height, frame_width, _ = frame.shape
        thumb_tip = None
        index_tip = None
        index_knuckle = None
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            index_knuckle = hand_landmarks.landmark[7]
        
        if thumb_tip and index_tip and index_knuckle:
            thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
            index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
            knuckle_x, knuckle_y = int(index_knuckle.x * frame_width), int(index_knuckle.y * frame_height)

            # 计算大拇指和食指之间的角度
            angle_rad = math.atan2(index_y - thumb_y, index_x - thumb_x)
            angle_deg = math.degrees(angle_rad)
            # 计算大拇指和食指之间的向量
            vector1 = np.array([index_x - thumb_x, index_y - thumb_y])
            
            # 计算食指第二关节和第三关节之间的向量
            vector2 = np.array([index_knuckle.x - index_x, index_knuckle.y - index_y])

            # 计算食指第三关节和第四关节之间的向量
            vector3 = np.array([index_tip.x - index_knuckle.x, index_tip.y - index_knuckle.y])

            
            # 计算两个向量之间的夹角
            angle_degrees = calculate_angle(vector1, vector2)

            # 计算两个向量之间的夹角
            angle_degrees_13 = calculate_angle(vector1, vector3)

            # 根据食指状态触发停止操作
            if angle_degrees < 130:
                direction = "stop"
            else:
                # 根据角度判断手势方向
                if -45 < angle_deg < 45:
                    direction = "Right"
                elif -135 <= angle_deg < -45:
                    direction = "Up"
                elif 45 <= angle_deg < 135:
                    direction = "Down"
                else:
                    direction = "Left"
            
            # 检测大拇指是否伸直
            # 根据食指状态触发开火或停火操作
            if angle_degrees_13 <= 45:
                fire_action = False
            else:
                fire_action = True

            # 显示方向
            cv2.putText(frame, f"Direction: {direction} {str(angle_degrees)}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 根据食指方向和大拇指状态触发开火或停火操作
            if fire_action:
                cv2.putText(frame, str(angle_degrees_13), (frame_width - 150, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame,  str(angle_degrees_13), (frame_width - 150, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
            

        cv2.imshow('Gesture Recognition', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera = initialize_camera()
    detect_gestures(camera)




    ################################
    # preprocessed = preprocess(image)
    # output = model(preprocessed)
    # output = F.softmax(output, dim=1).detach().cpu().numpy().flatten()
    # category_index = output.argmax()
    ################################

    ################################
    # current_time = time.time() 
    # if current_time - start_time > delta_time:
    #    previous_state ="" 
    # if previous_state != CATEGORIES[category_index]:
    #     print(CATEGORIES[category_index])
    #     previous_state = CATEGORIES[category_index]
    #     start_time = time.time()
    #     mqtt_client.publish(MQTT_TOPIC, CATEGORIES[category_index], qos=0)
    ################################

# ###################################
# """
# 這部分程式碼的作用是：

# 使用torchvision.models.resnet18(pretrained=True)來創建一個ResNet-18模型，
# 並使用預訓練的權重初始化它。這將模型的權重設置為在大型數據集（例如ImageNet）上訓練的權重，以便模型具有良好的特徵提取能力。

# 通過model.fc = torch.nn.Linear(512, len(dataset.categories))
# ，將模型的最後一個全連接層（Fully Connected Layer）的輸出維度更改為您的數據集的類別數。這是為了適應您的自定義數據集。

# 使用model.to(device)將模型移動到GPU（如果可用）或CPU上，以便在訓練和推理過程中使用相應的硬體。

# 使用model.load_state_dict(torch.load('/nvdli-nano/data/classification/game_model_2.pth'))從指定路徑加載預訓練模型的權重。
# 模型的權重存儲在'/nvdli-nano/data/classification/game_model_2.pth'文件中。

# 最後，使用model = model.eval()將模型設置為評估模式，這意味著模型將用於推理，不再進行梯度計算。

# 整個過程的目的是使用預訓練的ResNet-18模型來進行圖像分類任務，
# 並根據您的數據集進行微調。這樣，您可以在訓練過程中受益於預訓練模型的特徵提取能力。
# """
# device = torch.device('cuda')
# model = torchvision.models.resnet18(pretrained=True)
# model.fc = torch.nn.Linear(512, len(dataset.categories))
# model.to(device)

# # 要修改的模型的權重
# model.load_state_dict(torch.load('/nvdli-nano/data/classification/game_model_2.pth'))


# model = model.eval()
# print(f"model ready")
# ################################