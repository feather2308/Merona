import tkinter as tk
import tkinter.messagebox as messagebox
import json

# 장비 저장
def save_devices():
    with open("devices.json", "w") as f:
        json.dump(devices, f)

# 장비 불러오기
def load_devices():
    global devices
    try:
        with open("devices.json", "r") as f:
            devices = json.load(f)
    except FileNotFoundError:
        devices = []

# 새창을 생성하여 장비 옵션을 입력받고 등록하는 함수
def register_device():
    # 새로운 창 생성
    top = tk.Toplevel()
    top.title("장비 등록")

    # 장비 정보 입력을 위한 라벨 및 엔트리 위젯 생성
    tk.Label(top, text="장비 이름:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    device_name_entry = tk.Entry(top)
    device_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(top, text="장비 모델:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    device_model_entry = tk.Entry(top)
    device_model_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # 장비 옵션 입력을 위한 라벨 및 엔트리 위젯 생성
    tk.Label(top, text="장비 옵션", font=("Helvetica", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="w")
    option_names = ["STR", "DEX", "INT", "LUK", "공격력", "마력", "올스탯"]
    option_entries = {}
    for i, option_name in enumerate(option_names):
        tk.Label(top, text=option_name, font=("Helvetica", 10)).grid(row=4+i, column=0, padx=5, pady=5, sticky="e")
        option_entry = tk.Entry(top, font=("Helvetica", 10))
        option_entry.grid(row=4+i, column=1, padx=5, pady=5, sticky="w")
        option_entries[option_name] = option_entry

    # 장비 등록 버튼
    def add_device():
        # 엔트리 위젯에서 입력된 정보를 가져와서 장비 리스트에 추가
        device = {
            "name": device_name_entry.get(),
            "model": device_model_entry.get(),
            "options": {option_name: option_entry.get() for option_name, option_entry in option_entries.items()}
        }
        devices.append(device)
        top.destroy()

    # 장비 등록 버튼 생성
    tk.Button(top, text="장비 등록", command=add_device).grid(row=11, column=1, padx=5, pady=5, sticky="e")

# 장비 목록을 출력하는 함수
def show_devices():
    # 장비 목록을 출력할 새로운 창 생성
    top = tk.Toplevel()
    top.title("등록된 장비 목록")

    # 장비 목록 출력
    for i, device in enumerate(devices):
        tk.Label(top, text=f"{i+1}. {device['name']} ({device['model']})").grid(row=i, column=0, padx=5, pady=5, sticky="w")

        # 장비 옵션 수정 버튼
        def edit_options(device=device):
            # 새로운 창 생성
            edit_top = tk.Toplevel()
            edit_top.title("장비 옵션 수정")

            # 장비 정보 출력
            tk.Label(edit_top, text=f"장비 이름: {device['name']} ({device['model']})").grid(row=0, column=0, padx=5, pady=5)

            # 기존 옵션 값 출력 및 수정 가능한 엔트리 위젯 생성
            option_names = ["STR", "DEX", "INT", "LUK", "공격력", "마력", "올스탯"]
            option_entries = {}
            for i, option_name in enumerate(option_names):
                tk.Label(edit_top, text=option_name).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
                option_entry = tk.Entry(edit_top)
                option_entry.insert(0, device['options'][option_name])
                option_entry.grid(row=i+1, column=1, padx=5, pady=5, sticky="e")
                option_entries[option_name] = option_entry

            # 옵션 수정 버튼
            def update_options():
                # 수정된 옵션 값을 가져와서 해당 장비의 options 딕셔너리에 반영
                for option_name, option_entry in option_entries.items():
                    device['options'][option_name] = option_entry.get()
                save_devices()
                edit_top.destroy()

        # 장비 삭제 버튼 함수
        def delete_device(device=device):
            answer = messagebox.askquestion("장비 삭제", f"{device['name']} ({device['model']})을(를) 삭제하시겠습니까?")
            if answer == "yes":
                devices.remove(device)
                messagebox.showinfo("장비 삭제", f"{device['name']} ({device['model']})이(가) 삭제되었습니다.")
                top.destroy()
                show_devices()

        # 장비 옵션 수정, 삭제 버튼 생성
        tk.Button(top, text="옵션 수정", command=edit_options).grid(row=i, column=1)
        tk.Button(top, text="삭제", command=lambda device=device: delete_device(device)).grid(row=i, column=2)

# 등록된 옵션 값을 모두 합쳐서 출력하는 함수 추가
def show_options():
    # 등록된 옵션 값을 출력할 새로운 창 생성
    top = tk.Toplevel()
    top.title("등록된 옵션 값들")

    # 옵션 값 출력
    option_values = {"STR": 0, "DEX": 0, "INT": 0, "LUK": 0, "공격력": 0, "마력": 0, "올스탯": 0}
    for device in devices:
        for option_name, option_value in device['options'].items():
            if option_value != "":
                option_values[option_name] += int(option_value)  # 빈 문자열이 아닌 경우에만 값을 더합니다.
    for option_name, option_value in option_values.items():
        tk.Label(top, text=f"{option_name}: {option_value}").pack()

# 창 닫을때 실행되는 함수
def on_closing():
    if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
        save_devices()  # 장비 목록을 파일에 저장합니다.
        root.destroy()  # 윈도우 창을 닫습니다.

# 장비 리스트를 저장할 리스트
devices = []

# 프로그램 시작 시 저장된 장비 목록 불러오기
load_devices()

# 메인 창 생성
root = tk.Tk()
root.title("장비 목록")

# 메인 창 버튼에 "저장" 버튼 추가
tk.Button(root, text="장비 등록", command=register_device).grid(row=0, column=0, padx=5, pady=5)
tk.Button(root, text="등록된 장비 목록 보기", command=show_devices).grid(row=1, column=0, padx=5, pady=5)
tk.Button(root, text="스펙 보기", command=show_options).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
tk.Button(root, text="저장", command=save_devices).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)  # 윈도우 창의 X 버튼을 누르면 on_closing 함수가 실행됩니다.

root.mainloop()
