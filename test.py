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

# 修改使用jieba進行斷詞的函數
def cut_words(sentence):
    return jieba.cut(sentence, cut_all=False)

# Read stop words
stopwords = []
file = open('stop_word.txt', encoding='utf-8-sig').readlines()   
for lines in file:
    stopwords.append(lines.strip())
print('stopwords讀取完成一共'+ str(len(stopwords)) + '筆')

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

#from IPython.display import clear_output  ##用來清理一下output
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
                break
    except:
        print('Error!')
        clear_counter += 1
        if clear_counter == 10:
            clear_counter = 0
            os.system('clear')
