import openai
from textblob import TextBlob
import re
import os
# test 
# 환경 변수에서 OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 부적절한 단어 리스트 (예시)
inappropriate_words = ["나쁜말1", "나쁜말2", "나쁜말3"]

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "당신은 자폐 스펙트럼 장애인을 위한 의사소통 교육 보조 시스템입니다. 친절하고 이해하기 쉬운 말로 대화해주세요."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
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

def communication_training():
    print("필로봇 : 자폐 스펙트럼 장애인 감정교육 서비스에 오신 것을 환영합니다.")
    print("대화를 시작하려면 아무 말이나 입력해주세요. 종료하려면 '끝'을 입력하세요.")

    while True:
        user_input = input("사용자: ")
        if user_input.lower() == '끝':
            print("교육을 종료합니다. 고생했어요!")
            break

        # ChatGPT 응답 생성
        prompt = f"다음은 자폐 스펙트럼 장애가 있는 사람의 말입니다. 적절하게 응답해주세요: '{user_input}'"
        response = get_chatgpt_response(prompt)

        if response:
            # 응답 필터링
            filtered_response = filter_response(response)

            # 감정 분석
            sentiment = analyze_sentiment(filtered_response)

            print(f"시스템: {filtered_response}")
            print(f"감정 분석: 이 응답은 {sentiment}인 것으로 보입니다.")
            print("이 응답이 적절한지 평가해주세요. (1: 매우 나쁨, 5: 매우 좋음)")
            rating = input("평가 (1-5): ")

            # 여기에 사용자 피드백을 바탕으로 한 추가적인 학습 로직을 구현할 수 있다.
        else:
            print("미안해 무슨 소리인지 못 알아 들었어.")

if __name__ == "__main__":
    communication_training()
