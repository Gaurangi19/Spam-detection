# Spam-detection
Implementation of a Naïve Bayes classifier with the categories spam and ham (i.e., not spam).

1) nblearn.py writes to nbmodel.txt, which is then used by nbclassify.py to classify emails and write to nboutput.txt.  

2) The argument to nblearn.py is a data directory. The script searches through the directory recursively looking for subdirectories containing the folders: "ham" and "spam". "ham" and "spam" folders contain emails failing into the category of the folder name (i.e., a spam folder will contain only spam emails and a ham folder will contain only ham emails).

3) The argument to nbclassify.py is again a data directory. It reads the parameters of a naive Bayes model from the file nbmodel.txt, and classifies each ".txt" file in the data directory as "ham" or "spam", and writes the result to a text file called nboutput.txt in the format described below -
LABEL path_1
LABEL path_2
⋮
In the above format, LABEL is either “spam” or “ham” and path is the path to the file, and the name of filename (e.g., on Windows a path might be: "C:\dev\4\0001.2000-01-17.beck.txt").
