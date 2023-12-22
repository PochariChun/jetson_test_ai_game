
import os
import pygame
from Player import Player
from Missile import Missile
from Enemy import  Enemy
from Enemy import  Bullet
import paho.mqtt.client as mqtt
import threading
import jieba
import cv2
import mediapipe as mp
import math

text = None
should_continue = True
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def voice_translate(r,audio,stopwords,coding_syntax,learning_environment,project_assignment):
    global text
    # 修改使用jieba進行斷詞的函數
    def cut_words(sentence):
        return jieba.cut(sentence, cut_all=False)
    def calc_classification(word_sentence_list):
        ret_cs = []
        ret_le = []
        ret_pa = []
        other = []
        for word in word_sentence_list:
            if word not in stopwords:
                ### eliminate stopsword
                if word in coding_syntax:
                    ret_cs.append(word)
                elif word in learning_environment:
                    ret_le.append(word)
                elif word in project_assignment:
                    ret_pa.append(word)
                else:
                    other.append(word)
            
        return ret_cs , ret_le , ret_pa , other
    try:
        # 在新线程中进行语音识别
        print('開始翻譯.....')
        text = r.recognize_google(audio, language='zh-TW')
        print('结果：', text)
        # 这里可以添加更多处理识别结果的逻辑
                        
                
        cs, le, pa, ot = calc_classification(list(cut_words(text)))
                
        print('原句：', text)
        print('coding_syntax:', cs)
        print('learning_environment:', le)
        print('project_assignment:', pa)
        print('其他詞語:', ot)
                
        clear_counter += 1
        if clear_counter == 10:
            clear_counter = 0
            os.system('clear')
                
        if '退出' in text:
            should_continue = False  # 更新变量来通知主循环停止

    except Exception as e:
        print('Error:', e)

def voice_recognition():
    global text
    import csv
    import os
    import sys
    import jieba
    import speech_recognition as sr

    # Read ontology_words from CSV file
    coding_syntax = []
    learning_environment = []
    project_assignment = []
    all_words_for_jieba = []

    #close system warning
    os.close(sys.stderr.fileno())

    first_row = False
    with open('ontology_words.csv','r',encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if(first_row):
                if(row[0] != ''):
                    coding_syntax.append(row[0])
                if(row[1] != ''):
                    learning_environment.append(row[1])
                if(row[2] != ''):
                    project_assignment.append(row[2])
            if(first_row == False):
                first_row = True
                
    print('coding_syntax：' + str(len(coding_syntax)) ,
        '\nlearning_environment：' + str(len(learning_environment)) , 
        '\nproject_assignment：' + str(len(project_assignment)))

    # 將 ontology 的詞加入 jieba 的字典
    for word in all_words_for_jieba:
        jieba.add_word(word, freq=100)



    # Read stop words
    stopwords = []
    file = open('stop_word.txt', encoding='utf-8-sig').readlines()   
    for lines in file:
        stopwords.append(lines.strip())
    print('stopwords讀取完成一共'+ str(len(stopwords)) + '筆')

    

    #from IPython.display import clear_output  ##用來清理一下output
    clear_counter = 0
    r = sr.Recognizer()

    while should_continue:
        try:
            with sr.Microphone() as source:
                print('請開始說話')
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, phrase_time_limit=1)
                threading.Thread(target=voice_translate, args=(r,audio,stopwords,coding_syntax,learning_environment,project_assignment), daemon=True).start()
                print('Global原句：', text)

        except:
            print('Error!')
            clear_counter += 1
            if clear_counter == 10:
                clear_counter = 0
                os.system('clear')



def hand_recognition():
    global text
    import cv2
    import mediapipe as mp
    import math
    cap = cv2.VideoCapture(0)            # 讀取攝影機
    fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
    lineType = cv2.LINE_AA               # 印出文字的邊框

    # mediapipe 啟用偵測手掌
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        w, h = 540, 310                                  # 影像尺寸
        while True:
            ret, img = cap.read()
            img = cv2.resize(img, (w,h))                 # 縮小尺寸，加快處理效率
            if not ret:
                print("Cannot receive frame")
                break
            [img2] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
            results = hands.process(img2)                # 偵測手勢

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列
                    for i in hand_landmarks.landmark:
                        thumb_tip_x = i[mp.solutions.hands.HandLandmark.THUMB_TIP].x
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x*w
                        y = i.y*h
                        finger_points.append((x,y))
                    if finger_points:
                        finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                        #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                        text = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                        cv2.putText(img, text, (30,120), fontFace, 5, (255,255,255), 10, lineType) # 印出文字

            cv2.imshow('oxxostudio', img)
            if cv2.waitKey(5) == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
#############################################


# 启动语音识别线程
threading.Thread(target=voice_recognition, daemon=True).start()

# # 启动语音识别线程
# threading.Thread(target=hand_recognition, daemon=True).start()

WIDTH = 640
HEIGHT = 480
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
score = 0



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI project")
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
bg_img = pygame.image.load(os.path.join(img_folder, 'bg.png')).convert()

game_run = True
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

MISSILES = []




# 创建敌人
enemy = Enemy(320, 80)
# 子弹群组
bullet_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()





# 載入圖片
left_image = pygame.image.load(os.path.join(img_folder, 'christmas_bell.png'))
left_image2 = pygame.image.load(os.path.join(img_folder, 'christmas_tree.png'))
right_image = pygame.image.load(os.path.join(img_folder, 'right_Light_bulb.png'))

#調整圖片大小
left_image = pygame.transform.scale(left_image, (70, 70))
left_image2 = pygame.transform.scale(left_image2, (70, 70))
right_image = pygame.transform.scale(right_image, (70, 70))



merry_christmas_img = pygame.image.load(os.path.join(img_folder, '聖誕快樂圖.jpg')).convert()
merry_christmas_img = pygame.transform.scale(merry_christmas_img, (WIDTH, HEIGHT))  # 調整圖片大小以適應螢幕

game_over_img = pygame.image.load(os.path.join(img_folder, '聖誕快樂gameover圖.png')).convert()
game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))  # 調整圖片大小以適應螢幕

while game_run:
    if text =='左邊'or text =='左左左' or text =='左左左左':
        player.move_left()
    if text =='右邊'or text =='右'or text =='右右右右'or text =='右右右':
        player.move_right()
    if text =='發射' or text =='發' or text =='射'or text =='發射發射' :
        text = ''
        position = player.get_position()
        for i in range(10):   
            MISSILES.append(Missile(position[0], position[1]+i*10))
    if enemy.health <= 0:
        while True:
            screen.blit(merry_christmas_img, (0, 0))  # 顯示遊戲結束的圖片
            pygame.display.flip()  # 更新畫面
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    if player.health <= 0:
        while True:
            screen.blit(game_over_img, (0, 0))  # 顯示遊戲結束的圖片
            pygame.display.flip()  # 更新畫面
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()



    clock.tick(FPS)
    screen.blit(bg_img, (0, 0))

    # 畫左邊的圖
    for i in range(4):
        screen.blit(left_image,left_image.get_rect(topleft=(-10, 0+i*120)))
        screen.blit(left_image2,left_image2.get_rect(topleft=(0, 50+i*120)))
    # 畫右邊的圖
    for i in range(8):       
        screen.blit(right_image, right_image.get_rect(topleft=(580, i*70)))



    for mis in MISSILES:
        if mis.is_on_screen():
            screen.blit(mis.image, mis.rect)
            mis.update()
        else:
            MISSILES.remove(mis)

    all_sprites.update()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT] or event.key == pygame.K_LEFT :
                player.move_left()
            if keys[pygame.K_RIGHT] or event.key == pygame.K_RIGHT:
                player.move_right()
            if keys[pygame.K_SPACE] or event.key == pygame.K_SPACE:
                position = player.get_position()
                MISSILES.append(Missile(position[0], position[1]))
            
    # 更新敌人位置和射击
    enemy.update()
    enemy.shoot(bullets)

    # 更新子弹位置
    bullets.update()
    bullets.draw(screen)
    

    # 繪製敵人
    screen.blit(enemy.image, enemy.rect)

    
    
    player.draw_health_bar(screen, player.rect.x-10, player.rect.y-10, player.health)  # 玩家血條
    enemy.draw_health_bar(screen, enemy.rect.x, enemy.rect.y - 10, enemy.health)  # 敵人血條


    # 玩家被擊中
    for bullet in bullets:
        if player.collider(bullet):
            bullets.remove(bullet)
            player.health -= 10  # 減少玩家血量


    


    # 敵人被擊中
    for missile in MISSILES:
        if pygame.sprite.collide_rect(missile, enemy):
            enemy.health -= 10  # 減少敵人血量
            MISSILES.remove(missile)
                


    all_sprites.draw(screen)
    pygame.display.flip()






pygame.quit()






























