
def calc_classification(word_sentence_list, coding_syntax, learning_environment, project_assignment, stopwords):
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
