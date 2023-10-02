import json
from difflib import get_close_matches

def loadResponse(filePath: str) -> dict:
    with open(filePath, 'r') as file:
        data: dict = json.load(file)
    return data

def saveResponse(filePath: str, data: dict):
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=2)

def findBestMatches(userQuestion: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(userQuestion, questions, n=3, cutoff=0.6)
    return matches[0] if matches else None

def getAnswerForQuestion(question: str, Response: dict) -> str | None:
    for i in Response["question"]:
        if i["question"] == question:
            return i["answer"]

def chatBot():
    Response: dict = loadResponse('Response.json')

    while True:
        userInput: str = input('You: ')

        if userInput.lower() == 'quit':
            break

        bestMatch: str | None = findBestMatches(userInput, [i["question"] for i in Response["question"]])

        if bestMatch:
            answer: str = getAnswerForQuestion(bestMatch, Response)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know that... Can you teach me?')
            newAnswer: str = input('Type the answer or "skip" to skip: ')

            if newAnswer.lower() != 'skip':
                Response['question'].append({"question": userInput, "answer": newAnswer})
                saveResponse('Response.json', Response)
                print('Bot: Thank you!')

if __name__ == '__main__':
    chatBot()
