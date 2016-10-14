#nblearn version2
import os
import mimetypes
import sys

#set directory for the files
my_directory = str(sys.argv[1])

#define spam and ham dictionaries
spam_dict = {}
ham_dict = {}
count_dict = {}

#define all counts
spam_count = 0
ham_count = 0
total_count = 0
spam_words_count = 0
ham_words_count = 0
total_words_count = 0

#read file and count words
def process_file(filepath, email_type):
    global spam_count, ham_count
    # Open a file
    infile = open(filepath, "r", encoding="latin1")
    file_text = infile.read();
    #print(email_type, ":", file_text)
    # Close opened file
    infile.close()
    if email_type == "spam":
        add_to_spam_dict(file_text)
        spam_count += 1
    elif email_type == "ham":
        add_to_ham_dict(file_text)
        ham_count += 1
    else:
        #do nothing
        print(filepath, "training data not classified as spam or ham")

def add_to_spam_dict(file_text):
    global spam_words_count
    words = file_text.split()
    for word in words:
        if word in spam_dict:
            spam_dict[word] += 1
        else:
            spam_dict[word] = 1
        spam_words_count += 1

def add_to_ham_dict(file_text):
    global ham_words_count
    words = file_text.split()
    for word in words:
        if word in ham_dict:
            ham_dict[word] += 1
        else:
            ham_dict[word] = 1
        ham_words_count += 1
            
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

#set values for count dictionary
total_words_count = spam_words_count + ham_words_count
total_count = spam_count + ham_count
count_dict["spam-count"] = spam_count
count_dict["ham-count"] = ham_count
count_dict["total-count"] = total_count
count_dict["spam-words-count"] = spam_words_count
count_dict["ham-words-count"] = ham_words_count
count_dict["total-words-count"] = total_words_count

#print("Spam Dict:", spam_dict)
#print("Ham Dict:", ham_dict)
#print("Count Dict:", count_dict)

#create output file to print the inference
output_file = open("nbmodel.txt", "w", encoding="latin1")

#write all counts to nbmodel.txt
for key in count_dict:
    output_file.write(str(key) + " " + str(count_dict[key]) + "\n")

#write count of spam and ham data
output_file.write(str(len(spam_dict)) + "\n")
output_file.write(str(len(ham_dict)) + "\n")

#write spam data to nbmodel.txt
for key in spam_dict:
    output_file.write(str(key) + " " + str(spam_dict[key]) + "\n")
    
#write ham data to nbmodel.txt
for key in ham_dict:
    output_file.write(str(key) + " " + str(ham_dict[key]) + "\n")

#close output file
output_file.close()
