from jetcam.usb_camera import USBCamera
import speech_recognition as sr
import torch
import torchvision
from utils import preprocess
import torch.nn.functional as F
import torchvision.transforms as transforms
from dataset import ImageClassificationDataset
import paho.mqtt.client as mqtt
import time
import threading
import cv2

MQTT_HOST = '192.168.240.22'
MQTT_PASSWORD = 'mqtt_password'
MQTT_USER = 'mqtt_user'
MQTT_CLIENT = 'game'
MQTT_TOPIC = '/game'
CATEGORIES = ['move_left', 'move_right', 'stop', 'launch_missile']

# MQTT连接回调函数
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("已连接，返回代码：%d" % rc)

# 创建MQTT客户端并设置连接回调函数
mqtt_client = mqtt.Client(MQTT_CLIENT)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect

# 连接到MQTT服务器
mqtt_client.connect(MQTT_HOST, port=1883, keepalive=600)
mqtt_client.loop_start()

# 聲音識別線程
def audio_thread():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, phrase_time_limit=3)
                text = r.recognize_google(audio, language='zh-TW')
                if text in ["左邊", "右邊"]:
                    mqtt_client.publish(MQTT_TOPIC, text, qos=1)
        except:
            pass

# 影像識別線程

def video_thread():
    camera = USBCamera(width=224, height=224, capture_device=0)
    camera.running = True

    TRANSFORMS = transforms.Compose([
        transforms.ColorJitter(0.2, 0.2, 0.2, 0.2),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    datasets = {}
    datasets['A'] = ImageClassificationDataset(
        '/nvdli-nano/data/classification/game_A', CATEGORIES, TRANSFORMS
    )
    dataset = datasets['A']

    device = torch.device('cuda')
    model = torchvision.models.resnet18(pretrained=True)
    model.fc = torch.nn.Linear(512, len(dataset.categories))
    model.to(device)
    model.load_state_dict(torch.load('/nvdli-nano/data/classification/game_model_2.pth'))
    model = model.eval()

    while True:
        image = camera.value
        preprocessed = preprocess(image)
        output = model(preprocessed)
        output = F.softmax(output, dim=1).detach().cpu().numpy().flatten()
        category_index = output.argmax()

        # 將攝像頭捕獲的numpy陣列轉換為OpenCV圖像
        image_cv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 在圖像上顯示辨識結果
        cv2.putText(image_cv, CATEGORIES[category_index], (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 顯示影像
        cv2.imshow("Camera", image_cv)

        # 發送MQTT消息
        mqtt_client.publish(MQTT_TOPIC, CATEGORIES[category_index], qos=0)

        if cv2.waitKey(1) == 27:  # 按ESC鍵退出
            break

    camera.running = False
    cv2.destroyAllWindows()


# 主函數
def main():
    threading.Thread(target=audio_thread).start()
    threading.Thread(target=video_thread).start()

if __name__ == "__main__":
    main()
