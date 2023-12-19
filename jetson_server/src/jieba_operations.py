
import jieba

# 將 ontology 的詞加入 jieba 的字典
def add_words_to_jieba(all_words_for_jieba):
    for word in all_words_for_jieba:
        jieba.add_word(word, freq=100)

# 修改使用jieba進行斷詞的函數
def cut_words(sentence):
    return jieba.cut(sentence, cut_all=False)
