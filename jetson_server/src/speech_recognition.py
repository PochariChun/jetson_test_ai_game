
import os
import sys
import speech_recognition as sr
from data_processing import read_ontology_words, read_stopwords
from jieba_operations import add_words_to_jieba, cut_words
from classification import calc_classification

#close system warning
os.close(sys.stderr.fileno())

coding_syntax, learning_environment, project_assignment = read_ontology_words()
stopwords = read_stopwords()

# 將 ontology 的詞加入 jieba 的字典
all_words_for_jieba = coding_syntax + learning_environment + project_assignment
add_words_to_jieba(all_words_for_jieba)

clear_counter = 0
r = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as source:
            print('請開始說話')
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=3)
            print('開始翻譯.....')
            text = r.recognize_google(audio, language='zh-TW')  # Convert speech to text using Google recognizer
            
            cs, le, pa, ot = calc_classification(list(cut_words(text)), coding_syntax, learning_environment, project_assignment, stopwords)
            
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
                break
    except:
        print('Error!')
        clear_counter += 1
        if clear_counter == 10:
            clear_counter = 0
            os.system('clear')
