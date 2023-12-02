from datetime import datetime

# 텍스트 파일 경로
file_path = 'C:/Users/KIN/Desktop/Uni/2-2/창의공학설계/13주차/1.txt'

# 사용자 입력 값 및 추가하는 문자열
name = input('추가하고자 하는 제품명을 입력하세요: ')
day = input('현재 남은 날짜를 입력하세요:')
str = name + ' | ' + day + 'Day(' + datetime.now().strftime("%Y-%m-%d")

# 파일 열기 (읽기 모드)
with open(file_path, 'r', encoding='utf-8') as file:
    # 파일 내용 읽기
    content = [line.strip() for line in file if line.strip()]

# 파일 열기 (쓰기 모드)
with open(file_path, 'w', encoding='utf-8') as file:
    # 편집된 내용을 파일에 쓰기
    for item in content:
        file.write(item + '\n')
    file.write(str + '\n')