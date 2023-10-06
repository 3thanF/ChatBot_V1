import json #Import the json
from difflib import get_close_matches #Import the difflib to get the close matches

#Function to transform the given Json file as a dictionary
def load_knowledge(file_path: str) -> dict: 
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

#Function to save the given Json file
def save_knowledge(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

#Function to look up for the best match in the Json file
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

#Function to get the answer for the given question
def get_answer(question: str, knowledge: dict) -> str | None:
    for q in knowledge["questions"]:
        if q["question"] == question:
            return q["answer"]
        
def chat_bot():
    knowledge: dict = load_knowledge('knowledge.json')

    while True:
        user_input: str = input('You: ')

        if user_input == 'exit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge["questions"]])

        if best_match:
            answer: str = get_answer(best_match, knowledge)
            print(f'Bot: {answer}')
        else:
            print(f'Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer != 'skip':
                knowledge["questions"].append({"question":user_input, "answer": new_answer})
                save_knowledge('knowledge.json', knowledge)
                print(f'Bot: Thank you! I have learned a new answer.')

if __name__ == '__main__':
    chat_bot()