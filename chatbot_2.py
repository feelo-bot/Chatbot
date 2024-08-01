import os
import pandas as pd
import random

def load_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')

def shuffle_choices(correct_answer, wrong_answers):
    choices = [correct_answer] + wrong_answers
    random.shuffle(choices)
    return choices

def ask_question(item, question_number, total_questions):
    choices = shuffle_choices(item['answer'], [item['wrong1'], item['wrong2']])
    print(f"\n질문 {question_number}/{total_questions}")
    print(f"Situation: {item['situation']}")
    for i, choice in enumerate(choices):
        print(f"{i + 1}. {choice}")
    print("0. 프로그램 종료")
    return choices

def get_user_choice(choices):
    while True:
        user_choice = input("정답을 골라주세요 (번호로 입력, 0은 종료): ")
        if user_choice == '0':
            return 'exit'
        try:
            choice_index = int(user_choice) - 1
            if 0 <= choice_index < len(choices):
                return choice_index
            else:
                print("올바른 번호를 입력해주세요.")
        except ValueError:
            print("번호로 대답해주세요.")

def show_result(is_correct, item):
    if is_correct:
        print("정답이에요! 비슷한 표현으로는 이런 게 있어요:")
        print(f"1. {item['similar1']}")
        print(f"2. {item['similar2']}")
        print(f"3. {item['similar3']}")
    else:
        print(f"틀렸어요. 힌트: {item['hint']}")

def ask_continue():
    while True:
        continue_prompt = input("문제를 더 풀고 싶어요? (좋아요/싫어요/종료): ").strip().lower()
        if continue_prompt in ['좋아요', '싫어요', '종료']:
            return continue_prompt
        print("'좋아요', '싫어요' 또는 '종료'로 대답해주세요.")

def main():
    print("필로봇에 오신 여러분을 환영합니다!")
    
    file_path = r"C:\Users\vnfma\Desktop\새싹톤\myproject\myapp\response_6.csv"
    try:
        data = load_data_from_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return

    indices = list(range(len(data)))
    random.shuffle(indices)

    total_questions = len(indices)
    for question_number, index in enumerate(indices, 1):
        item = data[index]
        while True:
            choices = ask_question(item, question_number, total_questions)
            choice = get_user_choice(choices)
            if choice == 'exit':
                print("프로그램을 종료합니다. 다음에 또 만나요!")
                return
            is_correct = choices[choice] == item['answer']
            show_result(is_correct, item)
            if is_correct:
                break

        continue_choice = ask_continue()
        if continue_choice == '싫어요' or continue_choice == '종료':
            print("연습하느라 고생했어요!")
            break

    print("프로그램을 종료합니다. 다음에 또 만나요!")

if __name__ == "__main__":
    main()