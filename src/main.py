# 这是一个示例 Python 脚本。

import numpy as np
import math
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# 读取文件大小限制，单位KB
MAX_SIZE_KB = 200

# 加载文件，限制大小200KB
def load_file():
    import os
    root = tk.Tk()
    root.withdraw()
    max_size_bytes = MAX_SIZE_KB * 1024  # 转换为字节

    while True:
        file_path = filedialog.askopenfilename(
            title=f"请选择一个不超过 {MAX_SIZE_KB} KB 的文件"
        )

        # 用户点击“取消”
        if not file_path:
            return None

        # 获取文件大小
        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            messagebox.showerror("错误", "无法读取文件大小！")
            continue

        # 检查是否超限
        if file_size > max_size_bytes:
            size_mb = file_size / 1024
            messagebox.showwarning(
                "文件过大",
                f"文件大小为 {size_mb:.2f} KB，超过限制 {MAX_SIZE_KB} KB。\n请重新选择。"
            )
            continue  # 重新弹出选择框
        else:
            with open(file_path, "rb") as f:
                return f  # 合规，返回路径

# 计算最终结果
def calculate_result():
    # === E-LC1(单向偏心x轴) 构件基本参数 ===

    # 轴力相关
    N_test = 3258  # 轴力试验值 (kN)
    M_u = 667.18  # 极限弯矩值 (kN·m)
    gamma_Q355 = 1.125  # Q355钢材抗力分项系数
    N_design = N_test / gamma_Q355  # 轴力设计值 (kN)

    # 弯矩设计值
    MY_design = M_u / gamma_Q355  # 构件绕工程坐标系y轴弯矩设计值 (kN·m)
    Mx_design = 524.612604237573  # 构件绕形心主轴x弯矩设计值 (kN·m)
    My_design = 276.565724715513  # 构件绕形心主轴y弯矩设计值 (kN·m)

    # 材料与截面特性
    E = 206000.0  # 弹性模量 (MPa)
    f = 305.0  # 钢材设计强度 (MPa)
    A = 18494.0  # 截面积 (mm²)
    L = 4420.0  # 杆长 (mm)

    # 惯性矩
    Ix = 434951975.694101  # x主惯性矩 (mm⁴)
    Iy = 201839459.161942  # y主惯性矩 (mm⁴)

    # 扭转与翘曲常数
    It = 1611474.66666667  # 扭转常数 (mm⁴)
    Iw = 1509267318274.58  # 翘曲常数 (mm⁶)

    # 不对称常数
    beta_x = 145.1702474  # 关于X轴不对称常数
    beta_y = 74.6339493  # 关于Y轴不对称常数

    # 截面模量
    Wx = 1503396.00931591  # 形心主轴x截面模量 (mm³)
    Wy = 957075.12411876  # 形心主轴y截面模量 (mm³)

    # 换算长细比
    lambda_ = 71.6472448398353  # 换算长细比 λ（可能为组合）
    lambda_x = 28.821530683574  # 换算长细比 λx
    lambda_y = 42.3091849493257  # 换算长细比 λy


    # 稳定系数
    phi_y = 0.8995  # y轴受压构件稳定系数
    phi_bx = 1.0  # x轴受弯构件稳定系数

    # 塑性发展系数
    gamma_x = 1.05  # 截面塑性发展系数 γx
    gamma_y = 1.05  # 截面塑性发展系数 γy
    eta = 1.0  # 截面影响系数 η

    # 等效弯矩系数
    beta_my = 1.0  # 等效弯矩系数 βmy

    # 最终结果（用于判断）
    N_Ey = (math.pow(math.pi,2) * E * A) / (1.1 * math.pow(lambda_y,2))  # N'Ey (kN)，即等效屈服轴力
    print(f"N_Ey: {N_Ey}")

    # 最终结果计算公式
    N_Ey_ratio = (N_test * 1000) / (phi_y * A * f) \
        + (eta * Mx_design * 1000000) / (phi_bx * gamma_x * Wx * f) \
        + (beta_my * My_design * 1000000) / (gamma_y * Wy * f * (1 - 0.8 * N_test * 1000/N_Ey))
    print(f"N_Ey_ratio: {N_Ey_ratio}")
    return N_Ey, N_Ey_ratio

if __name__ == '__main__':
    file = load_file()
    if file:
        calculate_result()

    # 程序结束后等待用户输入，防止控制台窗口关闭
    print("\n程序执行完成，请按任意键退出...")
    input()
