# 这是一个示例 Python 脚本。
import math
import tkinter as tk
import pandas as pd
import json
from tkinter import filedialog, messagebox
from zai import ZhipuAiClient


# 读取文件大小限制，单位KB
MAX_SIZE_KB = 200
API_KEY = "a5838f8742e74e7e8673398089478388.es38Ass8Snsaub2c"
MODEL_NAME = "glm-4.6"
# 调用大模型提取数据并返回DataFrame
def load_data_ai(file_path):

    client = ZhipuAiClient(api_key=API_KEY)
    print("client build successfully")
    with open(file_path) as f:
        text = f.read()
        system_prompt = """作为一个文本处理专家，擅长从文本中提取数据。"""
        json_example = """{
  "metadata": {
    "project_name": "",
    "software": "SATWE2025R1.0 中文版",
    "calculation_date": "2025/12/15 15:44:43",
    "file_name": "WWNL1.OUT",
    "units": "m, kN, kN.m 和 Rad（弧度）"
  },
  "columns": [
    {
      "N-C": 1,
      "Node-i": 5,
      "Node-j": 1,
      "DL": 3.300,
      "Angle": 0.000,
      "internal_forces": [
        { "iCase": "1*", "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 18.0, "Mx-Btm": -0.0, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "1",  "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 18.0, "Mx-Btm": -0.0, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "2*", "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 17.8, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "2",  "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 17.8, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "3*", "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": 18.2, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.7 },
        { "iCase": "3",  "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": 18.2, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.7 },
        { "iCase": "4*", "Shear-X": -0.0, "Shear-Y": -4.2, "Axial": 90.0, "Mx-Btm": 20.7, "My-Btm": -0.0, "Mx-Top": -7.0, "My-Top": -0.0 },
        { "iCase": "4",  "Shear-X": -0.0, "Shear-Y": -4.2, "Axial": 90.0, "Mx-Btm": 20.7, "My-Btm": -0.0, "Mx-Top": -7.0, "My-Top": -0.0 },
        { "iCase": "5*", "Shear-X": -0.0, "Shear-Y": -3.9, "Axial": 88.3, "Mx-Btm": 20.0, "My-Btm": -0.1, "Mx-Top": -7.1, "My-Top": 0.1 },
        { "iCase": "5",  "Shear-X": -0.0, "Shear-Y": -3.9, "Axial": 88.3, "Mx-Btm": 20.0, "My-Btm": -0.1, "Mx-Top": -7.1, "My-Top": 0.1 },
        { "iCase": "6*", "Shear-X": 0.0, "Shear-Y": -4.4, "Axial": 91.7, "Mx-Btm": 21.4, "My-Btm": 0.1, "Mx-Top": -6.8, "My-Top": -0.1 },
        { "iCase": "6",  "Shear-X": 0.0, "Shear-Y": -4.4, "Axial": 91.7, "Mx-Btm": 21.4, "My-Btm": 0.1, "Mx-Top": -6.8, "My-Top": -0.1 },
        { "iCase": "7",  "Shear-X": -0.9, "Shear-Y": 0.0, "Axial": 3.1, "Mx-Btm": -0.0, "My-Btm": -1.9, "Mx-Top": -0.0, "My-Top": 1.1 },
        { "iCase": "8",  "Shear-X": 0.0, "Shear-Y": -9.3, "Axial": 165.2, "Mx-Btm": 41.1, "My-Btm": -0.0, "Mx-Top": -10.3, "My-Top": -0.0 },
        { "iCase": "9",  "Shear-X": 0.5, "Shear-Y": 0.0, "Axial": -70.0, "Mx-Btm": -0.0, "My-Btm": 0.5, "Mx-Top": -0.0, "My-Top": -1.1 },
        { "iCase": "10", "Shear-X": 0.0, "Shear-Y": 0.0, "Axial": -1.4, "Mx-Btm": -0.0, "My-Btm": 0.0, "Mx-Top": -0.0, "My-Top": -0.1 }
      ]
    },
    {
      "N-C": 2,
      "Node-i": 7,
      "Node-j": 3,
      "DL": 3.300,
      "Angle": 0.000,
      "internal_forces": [
        { "iCase": "1*", "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -18.0, "Mx-Btm": 0.0, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "1",  "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -18.0, "Mx-Btm": 0.0, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "2*", "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -17.8, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "2",  "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -17.8, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "3*", "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": -18.2, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.7 },
        { "iCase": "3",  "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": -18.2, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.7 },
        { "iCase": "4*", "Shear-X": -0.0, "Shear-Y": -4.2, "Axial": 90.0, "Mx-Btm": 20.7, "My-Btm": -0.0, "Mx-Top": -7.0, "My-Top": 0.0 },
        { "iCase": "4",  "Shear-X": -0.0, "Shear-Y": -4.2, "Axial": 90.0, "Mx-Btm": 20.7, "My-Btm": -0.0, "Mx-Top": -7.0, "My-Top": 0.0 },
        { "iCase": "5*", "Shear-X": -0.0, "Shear-Y": -4.4, "Axial": 91.7, "Mx-Btm": 21.4, "My-Btm": -0.1, "Mx-Top": -6.8, "My-Top": 0.1 },
        { "iCase": "5",  "Shear-X": -0.0, "Shear-Y": -4.4, "Axial": 91.7, "Mx-Btm": 21.4, "My-Btm": -0.1, "Mx-Top": -6.8, "My-Top": 0.1 },
        { "iCase": "6*", "Shear-X": 0.0, "Shear-Y": -3.9, "Axial": 88.3, "Mx-Btm": 20.0, "My-Btm": 0.1, "Mx-Top": -7.1, "My-Top": -0.1 },
        { "iCase": "6",  "Shear-X": 0.0, "Shear-Y": -3.9, "Axial": 88.3, "Mx-Btm": 20.0, "My-Btm": 0.1, "Mx-Top": -7.1, "My-Top": -0.1 },
        { "iCase": "7",  "Shear-X": -0.9, "Shear-Y": -0.0, "Axial": -3.1, "Mx-Btm": 0.0, "My-Btm": -1.9, "Mx-Top": 0.0, "My-Top": 1.1 },
        { "iCase": "8",  "Shear-X": -0.0, "Shear-Y": -9.3, "Axial": 165.2, "Mx-Btm": 41.1, "My-Btm": -0.0, "Mx-Top": -10.3, "My-Top": 0.0 },
        { "iCase": "9",  "Shear-X": -0.5, "Shear-Y": 0.0, "Axial": -70.0, "Mx-Btm": -0.0, "My-Btm": -0.5, "Mx-Top": -0.0, "My-Top": 1.1 },
        { "iCase": "10", "Shear-X": -0.0, "Shear-Y": 0.0, "Axial": -1.4, "Mx-Btm": -0.0, "My-Btm": -0.0, "Mx-Top": -0.0, "My-Top": 0.1 }
      ]
    },
    {
      "N-C": 3,
      "Node-i": 6,
      "Node-j": 2,
      "DL": 3.300,
      "Angle": 0.000,
      "internal_forces": [
        { "iCase": "1*", "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 18.0, "Mx-Btm": -0.0, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "1",  "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 18.0, "Mx-Btm": -0.0, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "2*", "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 18.2, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.7 },
        { "iCase": "2",  "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": 18.2, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.7 },
        { "iCase": "3*", "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": 17.8, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "3",  "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": 17.8, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "4*", "Shear-X": 0.0, "Shear-Y": -4.2, "Axial": -90.0, "Mx-Btm": 20.7, "My-Btm": 0.0, "Mx-Top": -7.0, "My-Top": 0.0 },
        { "iCase": "4",  "Shear-X": 0.0, "Shear-Y": -4.2, "Axial": -90.0, "Mx-Btm": 20.7, "My-Btm": 0.0, "Mx-Top": -7.0, "My-Top": 0.0 },
        { "iCase": "5*", "Shear-X": 0.0, "Shear-Y": -3.9, "Axial": -88.3, "Mx-Btm": 20.0, "My-Btm": 0.1, "Mx-Top": -7.1, "My-Top": -0.1 },
        { "iCase": "5",  "Shear-X": 0.0, "Shear-Y": -3.9, "Axial": -88.3, "Mx-Btm": 20.0, "My-Btm": 0.1, "Mx-Top": -7.1, "My-Top": -0.1 },
        { "iCase": "6*", "Shear-X": -0.0, "Shear-Y": -4.4, "Axial": -91.7, "Mx-Btm": 21.4, "My-Btm": -0.1, "Mx-Top": -6.8, "My-Top": 0.1 },
        { "iCase": "6",  "Shear-X": -0.0, "Shear-Y": -4.4, "Axial": -91.7, "Mx-Btm": 21.4, "My-Btm": -0.1, "Mx-Top": -6.8, "My-Top": 0.1 },
        { "iCase": "7",  "Shear-X": -0.9, "Shear-Y": 0.0, "Axial": 3.1, "Mx-Btm": -0.0, "My-Btm": -1.9, "Mx-Top": -0.0, "My-Top": 1.1 },
        { "iCase": "8",  "Shear-X": -0.0, "Shear-Y": -9.3, "Axial": -165.2, "Mx-Btm": 41.1, "My-Btm": 0.0, "Mx-Top": -10.3, "My-Top": 0.0 },
        { "iCase": "9",  "Shear-X": 0.5, "Shear-Y": -0.0, "Axial": -70.0, "Mx-Btm": 0.0, "My-Btm": 0.5, "Mx-Top": 0.0, "My-Top": -1.1 },
        { "iCase": "10", "Shear-X": 0.0, "Shear-Y": -0.0, "Axial": -1.4, "Mx-Btm": 0.0, "My-Btm": 0.0, "Mx-Top": 0.0, "My-Top": -0.1 }
      ]
    },
    {
      "N-C": 4,
      "Node-i": 8,
      "Node-j": 4,
      "DL": 3.300,
      "Angle": 0.000,
      "internal_forces": [
        { "iCase": "1*", "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -18.0, "Mx-Btm": 0.0, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "1",  "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -18.0, "Mx-Btm": 0.0, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.8 },
        { "iCase": "2*", "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -18.2, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.7 },
        { "iCase": "2",  "Shear-X": -4.8, "Shear-Y": -0.0, "Axial": -18.2, "Mx-Btm": 0.1, "My-Btm": -10.2, "Mx-Top": 0.0, "My-Top": 5.7 },
        { "iCase": "3*", "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": -17.8, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "3",  "Shear-X": -4.8, "Shear-Y": 0.0, "Axial": -17.8, "Mx-Btm": -0.1, "My-Btm": -10.2, "Mx-Top": -0.0, "My-Top": 5.8 },
        { "iCase": "4*", "Shear-X": 0.0, "Shear-Y": -4.2, "Axial": -90.0, "Mx-Btm": 20.7, "My-Btm": 0.0, "Mx-Top": -7.0, "My-Top": -0.0 },
        { "iCase": "4",  "Shear-X": 0.0, "Shear-Y": -4.2, "Axial": -90.0, "Mx-Btm": 20.7, "My-Btm": 0.0, "Mx-Top": -7.0, "My-Top": -0.0 },
        { "iCase": "5*", "Shear-X": 0.0, "Shear-Y": -4.4, "Axial": -91.7, "Mx-Btm": 21.4, "My-Btm": 0.1, "Mx-Top": -6.8, "My-Top": -0.1 },
        { "iCase": "5",  "Shear-X": 0.0, "Shear-Y": -4.4, "Axial": -91.7, "Mx-Btm": 21.4, "My-Btm": 0.1, "Mx-Top": -6.8, "My-Top": -0.1 },
        { "iCase": "6*", "Shear-X": -0.0, "Shear-Y": -3.9, "Axial": -88.3, "Mx-Btm": 20.0, "My-Btm": -0.1, "Mx-Top": -7.1, "My-Top": 0.1 },
        { "iCase": "6",  "Shear-X": -0.0, "Shear-Y": -3.9, "Axial": -88.3, "Mx-Btm": 20.0, "My-Btm": -0.1, "Mx-Top": -7.1, "My-Top": 0.1 },
        { "iCase": "7",  "Shear-X": -0.9, "Shear-Y": -0.0, "Axial": -3.1, "Mx-Btm": 0.0, "My-Btm": -1.9, "Mx-Top": 0.0, "My-Top": 1.1 },
        { "iCase": "8",  "Shear-X": 0.0, "Shear-Y": -9.3, "Axial": -165.2, "Mx-Btm": 41.1, "My-Btm": 0.0, "Mx-Top": -10.3, "My-Top": -0.0 },
        { "iCase": "9",  "Shear-X": -0.5, "Shear-Y": -0.0, "Axial": -70.0, "Mx-Btm": 0.0, "My-Btm": -0.5, "Mx-Top": 0.0, "My-Top": 1.1 },
        { "iCase": "10", "Shear-X": -0.0, "Shear-Y": -0.0, "Axial": -1.4, "Mx-Btm": 0.0, "My-Btm": -0.0, "Mx-Top": 0.0, "My-Top": 0.1 }
      ]
    }
  ]
}"""
        prompt = f"""{{
            "task": "根据文本text文本提取出其中的N-C（柱子）相关的数据，并将其整理为json格式",
            "text": {text},
            "role": ["输出格式为纯json文本，不要附带任何多余信息！", json格式：{json_example}]
        }}"""
        print("加载文件成功，开始读取数据...")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            thinking={
                "type": "false",  # 启用深度思考模式
            },
            response_format={
                "type": "json",
            },
            stream=False,  # 启用流式输出
        )
        content = response.choices[0].message.content
        split_content = content.split('```json')[1].split('```')[0].strip()
        print(f"大模型输出结果：{split_content}")

        # 提取json数据
        json_data = json.loads(split_content)

        # 构建 DataFrame 行列表
        rows = []
        for col in json_data["columns"]:
            base_info = {
                "N-C": col["N-C"],
                "Node-i": col["Node-i"],
                "Node-j": col["Node-j"],
                "DL": col["DL"],
                "Angle": col["Angle"]
            }
            for force in col["internal_forces"]:
                row = {**base_info, **force}
                rows.append(row)

        # 创建 DataFrame
        df = pd.DataFrame(rows)

        # 可选：调整列顺序，使其更易读
        column_order = ["N-C", "Node-i", "Node-j", "DL", "Angle", "iCase", "Shear-X", "Shear-Y", "Axial", "Mx-Btm",
                        "My-Btm", "Mx-Top", "My-Top"]
        df = df[column_order]

        # 查看前几行
        print(df.head())
        return df

# 加载文件，限制大小200KB。并通过大模型提取数据。
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
            return load_data_ai(file_path)  # 合规，返回路径

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
    # 加载原始数据
    source_data = load_file()


    # 计算最终结果
    # calculate_result()

    # 程序结束后等待用户输入，防止控制台窗口关闭
    print("\n程序执行完成，请按任意键退出...")
    input()
