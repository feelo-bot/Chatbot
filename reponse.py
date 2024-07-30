import pandas as pd
import mysql.connector

# MySQL 데이터베이스 연결
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # 실제 MySQL 사용자 이름으로 변경
            password="your_password",  # 실제 MySQL 비밀번호로 변경
            database="my_database"  # 실제 데이터베이스 이름으로 변경
        )
        print("MySQL 서버에 성공적으로 연결되었습니다.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 연결 테스트
connection = create_connection()
if connection:
    print("연결 성공")
    connection.close()
else:
    print("연결 실패")

# CSV 파일 읽기
def load_csv_to_mysql(csv_file):
    # CSV 파일을 DataFrame으로 읽기 (인코딩 지정)
    df = pd.read_csv(csv_file, encoding='utf-8')

    # MySQL 데이터베이스에 연결
    connection = create_connection()
    cursor = connection.cursor()

    # DataFrame의 각 행을 MySQL 테이블에 삽입
    for index, row in df.iterrows():
        sql = """
        INSERT INTO responses (situation, answer, wrong1, wrong2, similar1, similar2, similar3)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, tuple(row))

    # 변경 사항 커밋 및 연결 종료
    connection.commit()
    cursor.close()
    connection.close()

# CSV 파일 경로
csv_file_path = r"C:\Users\vnfma\Desktop\새싹톤\Chatbot\response_2.csv"  # CSV 파일 경로를 지정하세요

# CSV 파일을 MySQL에 저장
load_csv_to_mysql(csv_file_path)

print("CSV 파일이 MySQL 데이터베이스에 성공적으로 저장되었습니다.")
