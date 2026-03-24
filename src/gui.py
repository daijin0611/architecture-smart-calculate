import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import sys
import os

from parser import read_column_data, load_load_coefficients
from calculator import calculate_matrix
from utils import save_results_to_excel

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')
        self.widget.update()

    def flush(self):
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("架构计算工具 - 荷载组合计算")
        self.geometry("700x500")
        self.resizable(True, True)

        self.source_file = tk.StringVar()
        self.coef_file = tk.StringVar()
        self.output_file = tk.StringVar(value="data/荷载组合结果.xlsx")

        self.create_widgets()

        # Redirect stdout
        sys.stdout = TextRedirector(self.console_text)
        sys.stderr = TextRedirector(self.console_text, "stderr")

    def create_widgets(self):
        # 顶部输入栏框架
        input_frame = ttk.LabelFrame(self, text="文件设置", padding=(10, 10))
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # 原数据文件 (SATWE .OUT)
        ttk.Label(input_frame, text="SATWE 原始文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.source_file, width=60).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="浏览...", command=self.browse_source).grid(row=0, column=2, pady=5)

        # 荷载系数 Excel
        ttk.Label(input_frame, text="荷载系数 Excel:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.coef_file, width=60).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="浏览...", command=self.browse_coef).grid(row=1, column=2, pady=5)

        # 输出目录
        ttk.Label(input_frame, text="输出 Excel 路径:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.output_file, width=60).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="另存为...", command=self.browse_output).grid(row=2, column=2, pady=5)

        # 按钮与进度条
        action_frame = ttk.Frame(self, padding=(10, 0))
        action_frame.pack(fill=tk.X, padx=10, pady=5)

        self.btn_run = ttk.Button(action_frame, text="开始计算", command=self.start_calculation)
        self.btn_run.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(action_frame, orient=tk.HORIZONTAL, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # 日志区
        console_frame = ttk.LabelFrame(self, text="运行日志", padding=(10, 10))
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.console_text = tk.Text(console_frame, wrap=tk.WORD, state='disabled', bg='black', fg='white', font=("Consolas", 10))
        self.console_text.tag_config("stderr", foreground="red")
        
        scrollbar = ttk.Scrollbar(console_frame, command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=scrollbar.set)
        
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def browse_source(self):
        file_path = filedialog.askopenfilename(title="选择 SATWE 原始数据文件 (<=200KB)")
        if file_path:
            # Check size
            try:
                if os.path.getsize(file_path) > 200 * 1024:
                    messagebox.showwarning("文件过大", "选择的文件超过200KB，可能会导致解析慢或异常。")
            except Exception:
                pass
            self.source_file.set(file_path)
    
    def browse_coef(self):
        file_path = filedialog.askopenfilename(title="选择荷载系数 Excel 文件", filetypes=[("Excel Files", "*.xlsx *.xls")])
        if file_path:
            self.coef_file.set(file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(title="选择结果保存路径", defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.output_file.set(file_path)

    def start_calculation(self):
        if not self.source_file.get():
            messagebox.showerror("错误", "请先选择 SATWE 原始文件。")
            return
        
        # Disable button and start progress bar
        self.btn_run.config(state=tk.DISABLED)
        self.progress.start(10)

        # Clear console
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')
        
        # Run in separate thread to prevent freezing
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        try:
            print("=== 开始运行架构工具 ===")

            source_path = self.source_file.get()
            coef_path = self.coef_file.get()
            output_path = self.output_file.get()

            # 1. 读原始数据
            print(f"读取原始数据文件: {source_path}")
            source_data = read_column_data(source_path)

            if not source_data:
                print("解析到的原始数据为空。")
                return

            # 2. 读系数
            if coef_path and os.path.exists(coef_path):
                print(f"读取荷载系数: {coef_path}")
                coef_data = load_load_coefficients(coef_path)
            else:
                print("未设置或找不到荷载系数文件，尝试使用默认 data/荷载系数.xlsx")
                coef_data = load_load_coefficients()
            
            if coef_data is None:
                print("获取荷载系数失败。")
                return

            # 3. 矩阵计算
            result = calculate_matrix(source_data, coef_data)

            if not result:
                print("荷载组合计算生成了空结果。")
                return

            # 4. 保存
            # ensure dir exists
            out_dir = os.path.dirname(output_path)
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir)

            save_results_to_excel(result, output_path)
            print("=== 程序执行完成 ===")
            messagebox.showinfo("完成", f"结果已成功保存到:\n{output_path}")

        except Exception as e:
            print(f"\n[错误] 发生异常: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("程序异常", f"执行期间发生错误:\n{e}")

        finally:
            self.progress.stop()
            self.btn_run.config(state=tk.NORMAL)


if __name__ == '__main__':
    app = App()
    app.mainloop()
