#!/usr/bin/env python
# coding: utf-8

# ### 讀取所有ontology words  還有一些stop words

# In[2]:


import csv
import os
import sys

coding_syntax = []
learning_environment = []
project_assignment = []
all_words_for_ckiptagger = []

# close system warning
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

### 新增ontology所有的字詞 給ckiptagger 防止切詞把他切斷
all_words_for_ckiptagger.extend(coding_syntax)
all_words_for_ckiptagger.extend(learning_environment)
all_words_for_ckiptagger.extend(project_assignment)
new_dict = {x: 100 for x in all_words_for_ckiptagger}
print('取得要新增的字詞一共:' + str(len(new_dict)))

### 讀stop words 感謝林濤♥
stopwords = []
file = open('stop_word.txt', encoding='utf-8-sig').readlines()   
for lines in file:
    stopwords.append(lines.strip())
print('stopwords讀取完成一共'+ str(len(stopwords)) + '筆')


# ### 文字分詞
# 
# `pip install ckiptagger`

# In[41]:


from ckiptagger import construct_dictionary
from ckiptagger import WS

def cut_words(sentence, dict1):
    print(sentence)
    ws = WS('./data/')
    #s = '請問這個程式碼要怎麼編譯'
    input_string = [sentence.lower()]
    reg_dict = construct_dictionary(dict1)
    word_sentence_list = ws(input_string, recommend_dictionary=reg_dict)
    return word_sentence_list[0]


# In[30]:


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


# In[31]:


###get current to seconds
from datetime import datetime

def get_currenttime_to_second():
    reg = datetime.now()
    reg = reg.strftime("%H:%M:%S")
    reg = reg.split(':')
    current_time_second = int(reg[0])*3600 + int(reg[1])*60 + int(reg[2])*1
    return current_time_second



# In[32]:


import requests

def send_to_server(group, time, said, ontology):
    url = 'http://192.168.36.137:8000/member_info2/'

    myobj = {'who': group, 'said':said, 'time':time, 'ontology':ontology}

    headers = {'content-type': 'application/json'}
    x = requests.post(url, json = myobj , headers=headers)

    return x.text


# ### 即時翻譯一段文字

# In[7]:


import speech_recognition as sr
import os
#from IPython.display import clear_output  ##用來清理一下output
clear_counter = 0
group_id = 1  # 1~4


r = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as source:
            print('請開始說話')
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=3)
            print('開始翻譯.....')
            text = r.recognize_google(audio, language='zh-TW') #Speech to text google recognizer
            cs, le, pa, ot = calc_classification(cut_words(text, new_dict))
            print('原句： ' +text +'\n 經過ontology後', cs, le, pa, ot)
            current_time = get_currenttime_to_second()
            print('id：' + str(group_id) , 'time：' + str(current_time))
            
            ## post 給server
            server_response = send_to_server(group_id, current_time, text, [cs, le, pa, ot])
            print('server接收：' + server_response)
            #print(text) #This is what you actually said
            
            ### 如果印出10筆了  就clear一下  這樣比較好審視
            clear_counter += 1
            if(clear_counter == 10):
                clear_counter = 0
                os.system('clear')
            
            
            
            if('退出' in text):
                break
    except:
        print('Error!')
        clear_counter += 1
        if(clear_counter == 10):
            clear_counter = 0
            #clear_output()
            os.system('clear')


# In[47]:


group_id = 2
current_time = get_currenttime_to_second()
text = 'I am handsome'
cs, le, pa, ot = calc_classification(cut_words(text, new_dict))

#server_response = send_to_server(group_id, current_time, text, [cs, le, pa, ot])
print(cs, le, pa, ot)
#print('server接收：' + server_response)


# In[ ]:




