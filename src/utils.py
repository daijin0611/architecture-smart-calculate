# 工具函数模块
import os
import tkinter as tk
from tkinter import filedialog, messagebox

MAX_SIZE_KB = 200


def load_file() -> str:
    """
    弹出文件选择对话框，返回选中的文件路径。
    限制文件大小不超过 MAX_SIZE_KB。
    
    Returns:
        str: 文件路径，用户取消则返回 None
    """
    root = tk.Tk()
    root.withdraw()
    max_size_bytes = MAX_SIZE_KB * 1024

    while True:
        file_path = filedialog.askopenfilename(
            title=f"请选择一个不超过 {MAX_SIZE_KB} KB 的文件"
        )

        if not file_path:
            return None

        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            messagebox.showerror("错误", "无法读取文件大小！")
            continue

        if file_size > max_size_bytes:
            size_kb = file_size / 1024
            messagebox.showwarning(
                "文件过大",
                f"文件大小为 {size_kb:.2f} KB，超过限制 {MAX_SIZE_KB} KB。\n请重新选择。"
            )
            continue
        else:
            return file_path


def save_results_to_excel(result: dict, output_file: str = "data/荷载组合结果.xlsx"):
    """
    将计算结果保存到Excel文件，每个柱子一个sheet。
    
    Args:
        result: dict[str, pd.DataFrame]，计算结果
        output_file: 输出文件路径
    """
    import pandas as pd
    
    if not result:
        print("没有结果可保存")
        return
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for key, value in result.items():
            value.to_excel(writer, sheet_name=key, index=True)
            print(f"{key} 已保存")
    
    print(f"\n结果已保存到: {output_file}")
