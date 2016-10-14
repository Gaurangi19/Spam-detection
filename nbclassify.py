#nbclassify with add-one smoothing, with log, with add-one smoothing for unknown words
import os
import mimetypes
import math
from decimal import *

#define spam and ham dictionaries
spam_dict = {}
ham_dict = {}
count_dict = {}

#initialize counts for precision, recall and F1
correct_classify_spam = 0
classify_spam = 0
actual_class_spam = 0
correct_classify_ham = 0
classify_ham = 0
actual_class_ham = 0
unknown_words_count = 0

#read learning model file nbmodel.txt
input_file = open("nbmodel.txt", "r", encoding="latin1")
#file_text = input_file.read();
#print(file_text)

#populate count dictionary
for i in range(0, 6):
    input_line = input_file.readline().strip()
    input_line = input_line.split()
    count_dict[input_line[0]] = int(input_line[1])

#read spam and ham data counts
input_line = input_file.readline().strip()
spam_data_count = int(input_line)
input_line = input_file.readline().strip()
ham_data_count = int(input_line)

#populate spam dictionary
for i in range(0, spam_data_count):
    input_line = input_file.readline().strip()
    input_line = input_line.split()
    spam_dict[input_line[0]] = int(input_line[1])

#populate ham dictionary
for i in range(0, ham_data_count):
    input_line = input_file.readline().strip()
    input_line = input_line.split()
    ham_dict[input_line[0]] = int(input_line[1])

#print(count_dict)
#print(spam_dict)
#print(ham_dict)

#create vocabulary
vocab = {}
for key in spam_dict:
    vocab[key] = "spam"
for key in ham_dict:
    vocab[key] = "ham"     
vocab_size = len(vocab)
print("Vocab size:", vocab_size)

#calculate spam and ham probabilities
if vocab_size == 0:
    prob_spam = 0
    prob_ham = 0
else:
    prob_spam = math.log(Decimal(count_dict["spam-count"])/Decimal(count_dict["total-count"]))
    prob_ham = math.log(Decimal(count_dict["ham-count"])/Decimal(count_dict["total-count"]))
if prob_spam >= prob_ham:
    base_class = "spam"
else:
    base_class = "ham"

#set directory for the files
my_directory = "C:/USC stuff/Applied NLP/HW1/Spam or Ham/dev"
doc_count = 0
correct_count = 0

#read file and generate words list
def process_file(filepath, email_type):
    global doc_count, correct_count, actual_class_spam, actual_class_ham
    global correct_classify_spam, correct_classify_ham, classify_spam, classify_ham
    global unknown_words_count
    doc_count += 1
    # Open a file
    infile = open(filepath, "r", encoding="latin1")
    file_text = infile.read();
    #print(email_type, ":", file_text)
    # Close opened file
    infile.close()
    words = file_text.split()
    sum_words_spam = 0
    sum_words_ham = 0
    for word in words:
        if word in vocab:
            sum_words_spam += calculate_probability(word, "spam")
            sum_words_ham += calculate_probability(word, "ham")
        #for unknown words
        else:
            unknown_words_count += 1
            sum_words_spam += math.log(Decimal(1)/Decimal(count_dict["spam-words-count"] + vocab_size))
            sum_words_ham += math.log(Decimal(1)/Decimal(count_dict["ham-words-count"] + vocab_size))
    prob_msg_spam = prob_spam + sum_words_spam
    prob_msg_ham = prob_ham + sum_words_ham
    #print("spam prob:", prob_msg_spam)
    #print("ham prob:", prob_msg_ham)
    if prob_msg_spam > prob_msg_ham:
        class_type = "spam"
    elif prob_msg_spam < prob_msg_ham:
        class_type = "ham"
    else:
        class_type = base_class
    #print(class_type, filepath)
    output_file.write(str(class_type) + " " + str(filepath) + "\n")
    #calculate counts for metrics
    if class_type == email_type and class_type == "spam":
        correct_classify_spam += 1
        correct_count += 1
    if class_type == email_type and class_type == "ham":
        correct_classify_ham += 1
        correct_count += 1
    if class_type == "spam":
        classify_spam += 1
    if class_type == "ham":
        classify_ham += 1
    if email_type == "spam":
        actual_class_spam += 1
    if email_type == "ham":
        actual_class_ham += 1

def calculate_probability(word, class_type):
    if class_type == "spam":
        if word not in spam_dict:
            prob = Decimal(1)/Decimal(count_dict["spam-words-count"] + vocab_size)
        else:
            prob = Decimal(spam_dict[word] + 1)/Decimal(count_dict["spam-words-count"] + vocab_size)
    else:
        if word not in ham_dict:
            prob = Decimal(1)/Decimal(count_dict["ham-words-count"] + vocab_size)
        else:
            prob = Decimal(ham_dict[word] + 1)/Decimal(count_dict["ham-words-count"] + vocab_size)
    prob = math.log(prob)
    #print(word, prob)
    return prob


#create output file to print the inference
output_file = open("nboutput_part3_v1.txt", "w", encoding="latin1")

#search through the main directory for text files
for dirpath, dirnames, filenames in os.walk(my_directory):
    for filename in filenames:
        if mimetypes.guess_type(filename)[0] == 'text/plain':
            #print(os.path.join(dirpath, filename))
            filepath = os.path.join(dirpath, filename)
            #print(dirpath)
            email_type = os.path.basename(dirpath)
            #print(filepath)
            process_file(filepath, email_type)

print(correct_count, doc_count)
accuracy = Decimal(correct_count/doc_count)
print("Accuracy:", accuracy)

recall_spam = Decimal(correct_classify_spam/actual_class_spam)
recall_ham = Decimal(correct_classify_ham/actual_class_ham)

precision_spam = Decimal(correct_classify_spam/classify_spam)
precision_ham = Decimal(correct_classify_ham/classify_ham)

print("Precision spam:", precision_spam)
print("Precision ham:", precision_ham)
print("Recall spam:", recall_spam)
print("Recall ham:", recall_ham)

if (precision_spam != 0 or recall_spam != 0):
    F1_spam = Decimal((2 * precision_spam * recall_spam)/(precision_spam + recall_spam))
    print("F1 score spam:", F1_spam)
if (precision_ham != 0 and recall_ham != 0):
    F1_ham = Decimal((2 * precision_ham * recall_ham)/(precision_ham + recall_ham))
    print("F1 score ham:", F1_ham)

print("Unknown words count:", unknown_words_count)

#close output file
output_file.close()
