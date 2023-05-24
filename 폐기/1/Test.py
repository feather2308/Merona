import tkinter as tk

# 윈도우 생성
win = tk.Tk()

# 윈도우 크기 설정
win.geometry("400x300")

# 윈도우 타이틀 설정
win.title("My Window")

# 버튼 클릭시 실행될 함수
def display_input():
    # Entry 위젯에서 입력된 값을 가져옵니다.
    input_value = entry.get()

    # 콘솔에 입력된 값을 출력합니다.
    print("입력된 값은:", input_value)

# 버튼 생성
button = tk.Button(win, text="입력된 값 확인", command=display_input)

# 버튼 배치
button.pack()

# Entry 위젯 생성
entry = tk.Entry(win)

# Entry 위젯 배치
entry.pack()

# 라벨 생성
label = tk.Label(win, text="Enter your name:")

# 라벨 배치
label.pack()

# 텍스트 박스 생성
textbox = tk.Entry(win, text="John Smith")

# Entry 위젯에 기본값 추가
textbox.insert(0, "기본값")

# 텍스트 박스 배치
textbox.pack()

# 윈도우 실행
win.mainloop()
