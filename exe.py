import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# GUI 창 설정
root = tk.Tk()
root.title("Python to EXE 변환기")
root.geometry("500x350")

# 기본 설정
excluded_libs = ["matplotlib", "numpy", "pandas"]  # 제외할 라이브러리 목록
upx_path = ""  # UPX 경로 (설정 가능)
icon_path = ""  # 기본 아이콘 (사용자가 선택 가능)

# 파일 선택
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python 파일", "*.py")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# 아이콘 선택
def select_icon():
    global icon_path
    icon_file = filedialog.askopenfilename(filetypes=[("아이콘 파일", "*.ico")])
    if icon_file:
        icon_path = icon_file
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, icon_file)

# EXE 변환 실행
def convert_to_exe():
    py_file = file_entry.get().strip()
    
    if not py_file:
        messagebox.showerror("오류", "파일을 선택해주세요!")
        return

    file_name = os.path.basename(py_file).split('.')[0]  # 확장자 제거
    output_dir = os.path.dirname(py_file)  # 파일이 있는 폴더

    # 제외할 라이브러리 추가
    exclude_options = " ".join([f"--exclude {lib}" for lib in excluded_libs])

    # 아이콘 옵션 설정
    icon_option = f'--icon="{icon_path}"' if icon_path else ""

    # 1️⃣ PyInstaller 실행 (1차 변환)
    pyinstaller_cmd = (
        f'pyinstaller --onefile --noconsole {icon_option} {exclude_options} "{py_file}"'
    )
    subprocess.run(pyinstaller_cmd, shell=True)

    # 2️⃣ .spec 파일 수정하여 최적화
    spec_file = f"{file_name}.spec"
    if os.path.exists(spec_file):
        with open(spec_file, "r", encoding="utf-8") as f:
            spec_content = f.read()

        # 불필요한 데이터 제거
        spec_content = spec_content.replace("binaries=", "binaries=[],").replace("datas=", "datas=[],")
        
        with open(spec_file, "w", encoding="utf-8") as f:
            f.write(spec_content)

        # 최적화된 .spec 파일로 재컴파일
        subprocess.run(f"pyinstaller {spec_file}", shell=True)

    # 3️⃣ UPX 압축 적용
    exe_file = os.path.join(output_dir, "dist", f"{file_name}.exe")
    if os.path.exists(exe_file):
        upx_cmd = f'upx --best "{exe_file}"' if upx_path else ""
        if upx_cmd:
            subprocess.run(upx_cmd, shell=True)

    messagebox.showinfo("완료", "EXE 변환이 완료되었습니다!")

# 파일 입력창
tk.Label(root, text="Python 파일 선택:").pack(pady=5)
file_entry = tk.Entry(root, width=50)
file_entry.pack(pady=5)
tk.Button(root, text="파일 선택", command=select_file).pack(pady=5)

# 아이콘 선택창
tk.Label(root, text="아이콘 선택 (.ico):").pack(pady=5)
icon_entry = tk.Entry(root, width=50)
icon_entry.pack(pady=5)
tk.Button(root, text="아이콘 선택", command=select_icon).pack(pady=5)

# 변환 버튼
tk.Button(root, text="EXE 변환", command=convert_to_exe).pack(pady=10)

# GUI 실행
root.mainloop()
