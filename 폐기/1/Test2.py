import tkinter as tk

option_names = ["Attack", "Defense", "HP"]

class GearOptionGUI:
    def __init__(self, master):
        # 창 생성
        self.master = master
        self.master.title("Gear Options")

        # 입력 필드 생성
        self.input_fields = []
        for i, name in enumerate(option_names):
            label = tk.Label(master, text=name)
            label.grid(row=i, column=0)
            input_field = tk.Entry(master)
            input_field.grid(row=i, column=1)
            self.input_fields.append(input_field)

        # 입력 버튼 생성
        self.button = tk.Button(master, text="Enter", command=self.show_options)
        self.button.grid(row=len(option_names), column=0, columnspan=2)

        # 결과 텍스트 박스 생성
        self.result_text = tk.Text(master, height=5)
        self.result_text.grid(row=len(option_names) + 1, column=0, columnspan=2)

    # 입력된 옵션 표시 함수
    def show_options(self):
        results = []
        for i, input_field in enumerate(self.input_fields):
            option = input_field.get()
            results.append(f"{option_names[i]}: {option}")
        result_str = "\n".join(results)
        self.result_text.delete(1.0, tk.END)  # 기존 결과 삭제
        self.result_text.insert(tk.END, result_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = GearOptionGUI(root)
    root.mainloop()
