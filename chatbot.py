import os
import openai
from textblob import TextBlob
import re

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 부적절한 단어 리스트 (예시)
inappropriate_words = ["나쁜말1", "나쁜말2", "나쁜말3"]

# 대화 기록을 저장할 리스트
conversation_history = []

def get_chatgpt_response(prompt):
    try:
        messages = [{"role": "system", "content": "당신은 자폐 스펙트럼 장애인을 위한 의사소통 교육 보조 시스템입니다. 친절하고 이해하기 쉬운 말로 대화해주세요."}] + conversation_history + [{"role": "user", "content": prompt}]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"ChatGPT API 오류: {e}")
        return None

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.1:
        return "긍정적"
    elif sentiment < -0.1:
        return "부정적"
    else:
        return "중립적"

def filter_response(response):
    for word in inappropriate_words:
        response = re.sub(word, "[부적절한 단어]", response, flags=re.IGNORECASE)
    return response

def log_feedback(prompt, response, rating):
    # 데이터베이스나 파일에 피드백 저장
    # 예: 파일에 저장
    with open("feedback_log.txt", "a") as f:
        f.write(f"Prompt: {prompt}\nResponse: {response}\nRating: {rating}\n\n")

def communication_training():
    print("필로봇 : 자폐 스펙트럼 장애인 감정교육 서비스에 오신 것을 환영합니다.")
    print("대화를 시작하려면 아무 말이나 입력해주세요. 종료하려면 '끝'을 입력하세요.")

    while True:
        user_input = input("사용자: ")
        if user_input.lower() == '끝':
            print("교육을 종료합니다. 고생했어요:)")
            break

        prompt = f"다음은 자폐 스펙트럼 장애가 있는 사람의 말입니다. 적절하게 응답해주세요: '{user_input}'"
        response = get_chatgpt_response(prompt)

        if response:
            filtered_response = filter_response(response)
            sentiment = analyze_sentiment(filtered_response)

            print(f"시스템: {filtered_response}")
            print(f"감정 분석: 이 응답은 {sentiment}인 것으로 보입니다.")
            print("이 응답이 적절한지 평가해주세요. (1: 매우 나쁨, 5: 매우 좋음)")
            rating = input("평가 (1-5): ")

            if rating:
                log_feedback(prompt, filtered_response, rating)

            # 대화 기록 업데이트
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})

            # 대화 기록이 너무 길어지지 않도록 관리 (예: 최근 10개 메시지만 유지)
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
        else:
            print("미안해 무슨 소리인지 못 알아 들었어.")

if __name__ == "__main__":
    communication_training()
