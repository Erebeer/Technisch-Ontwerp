import csv
import urllib.request
import json
import helpers

questions = helpers.generate()

# Set score
score = 0


for x in questions:
    correct_answer = questions[x][1].lower()
    print(correct_answer)
    print(questions[x][0])
    print("Your Answer: ")
    answer = input()

    if answer == correct_answer:
        print("Correct!")
        score = score + 100
    elif answer == "pass":
        print("passed, you'll lose 50 points")
        score = score - 50
    else:
        score = score - 100
        print("Wrong, you'll lose 100 points")
    print("current score: ",score)

print("Total Score: ", score)


