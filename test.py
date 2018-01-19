import csv
import urllib.request

api =  "https://opentdb.com/api.php?amount=10"
webpage = list(urllib.request.urlopen(api))
all_questions = webpage[0]

print(all_questions[3])