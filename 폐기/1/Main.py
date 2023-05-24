import tkinter as tk
from tkinter import ttk

분류 = ["모자","상의","하의","신발","장갑","망토","어깨장식","반지","포켓 아이템","벨트","펜던트","얼굴장식","눈장식","귀고리","뱃지","훈장","하트","무기","보조무기","엠블렘"]
option0 = ["힘","덱","인","럭","공","마","올","보","방","뎀","힢","뎊","잎","렆","옾","곺","맢"]

class Equipment:
    def __init__(self,분류):
        self.분류 = 분류

    def set(self,Opt,Num):
        if Opt == "힘":self.힘=Num
        elif Opt == "덱":self.덱=Num
        elif Opt == "인":self.인=Num
        elif Opt == "럭":self.럭=Num
        elif Opt == "공":self.공=Num
        elif Opt == "마":self.마=Num
        elif Opt == "올":self.올=Num
        elif Opt == "보":self.보=Num
        elif Opt == "방":self.방=Num
        elif Opt == "뎀":self.뎀=Num
        elif Opt == "힢":self.힢=Num
        elif Opt == "뎊":self.뎊=Num
        elif Opt == "잎":self.잎=Num
        elif Opt == "렆":self.렆=Num
        elif Opt == "옾":self.옾=Num
        elif Opt == "곺":self.곺=Num
        elif Opt == "맢":self.맢=Num

    def print(self,Opt):
        if Opt == "힘":return self.힘
        elif Opt == "덱":return self.덱
        elif Opt == "인":return self.인
        elif Opt == "럭":return self.럭
        elif Opt == "공":return self.공
        elif Opt == "마":return self.마
        elif Opt == "올":return self.올
        elif Opt == "보":return self.보
        elif Opt == "방":return self.방
        elif Opt == "뎀":return self.뎀
        elif Opt == "힢":return self.힢
        elif Opt == "뎊":return self.뎊
        elif Opt == "잎":return self.잎
        elif Opt == "렆":return self.렆
        elif Opt == "옾":return self.옾
        elif Opt == "곺":return self.곺
        elif Opt == "맢":return self.맢

class GUI:
    def __init__(self,master):
        self.master = master
        self.master.title("Merona")

        self.input_fields = []
        분류드롭다운 = ttk.Combobox(root, values=분류)
        분류드롭다운.grid()
        분류드롭다운선택값=tk.StringVar()

        for i, name in enumerate(option0):
            label = tk.Label(master, text=name)
            label.grid(row=i, column=0)
            input_field = tk.Entry(master)
            input_field.grid(row=i, column=1)
            self.input_fields.append(input_field)

        a = Equipment(분류드롭다운선택값.get())

        self.button = tk.Button(master, text="Enter", command=self.show_options)
        self.button.grid(row=len(option0), column=0, columnspan=2)

        self.result_text = tk.Text(master, height=5)
        self.result_text.grid(row=len(option0) + 1, column=0, columnspan=2)

    def open_input_window(self):
        input_window = tk.Toplevel(self.master)
        input_window.title("Input Window")

        # Add input widgets to input_window
        
    #def 장비등록(self,장비명,분류):

        
    def show_options(self):
        results = []
        for i, input_field in enumerate(self.input_fields):
            option = input_field.get()
            a.set(option0[i],option)
            results.append(f"{option0[i]}: {a.print(option0[i])}")
        result_str = "\n".join(results)
        self.result_text.delete(1.0, tk.END)  # 기존 결과 삭제
        self.result_text.insert(tk.END, result_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()