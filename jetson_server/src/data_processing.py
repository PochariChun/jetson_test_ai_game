
import csv

# Read ontology_words from CSV file
def read_ontology_words():
    coding_syntax = []
    learning_environment = []
    project_assignment = []
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
    return coding_syntax, learning_environment, project_assignment

# Read stop words
def read_stopwords():
    stopwords = []
    with open('stop_word.txt', encoding='utf-8-sig') as file:
        for line in file:
            stopwords.append(line.strip())
    return stopwords
