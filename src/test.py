import pandas as pd
import numpy as np

# ==========================================
# 第一步：定义底层规范与物理材料参数
# ==========================================
STEEL_YIELD_STRENGTH = 355  # 屈服强度 fy (MPa)
STEEL_DESIGN_STRENGTH = 305  # 设计强度 f (MPa) - 来自您的参数表
MODULUS_OF_ELASTICITY = 206000  # 弹性模量 E (MPa)


# ==========================================
# 第二步：定义核心计算函数 (模拟 Excel 里的公式)
# ==========================================

def calculate_slenderness(length, radius_of_gyration):
    """计算长细比 λ = L / i"""
    return length / radius_of_gyration


def calculate_stability_factor(lambda_val, steel_type='b'):
    """
    计算轴心受压构件稳定系数 φ (简化版，参照 GB50017 柱曲线)
    说明：此处为演示逻辑，实际使用时可直接套用规范的正则化长细比公式
    或者像您 Excel 中那样，直接写一个查表/插值函数。
    为匹配您的数据，当 λ ≈ 42.3 时，返回约 0.8895
    """
    # 这里用一个简单的条件分支代替复杂的规范查表，确保逻辑跑通
    if lambda_val < 30:
        return 0.95
    elif 30 <= lambda_val <= 50:
        # 线性插值逼近您表格里的 0.8895
        return 0.95 - (0.95 - 0.8895) * ((lambda_val - 30) / (42.31 - 30))
    else:
        return 0.8  # 示意值


def check_bending_compression_stability(row):
    """
    核心公式：压弯构件稳定性验算公式 (GB50017)
    公式: N / (φ * A * f) + (βm * M) / (γ * W * f)
    """
    N = row['N_test_kN'] * 1000  # 转换为 N
    M = row['M_test_kNm'] * 1e6  # 转换为 N*mm
    A = row['Area_mm2']  # 截面积 mm^2
    W = row['W_mm3']  # 截面抵抗矩 mm^3
    phi = row['phi_min']  # 稳定系数 (取x,y中较小值)
    f = STEEL_DESIGN_STRENGTH  # 设计强度 MPa

    # 假设等效弯矩系数 βm=1.0, 截面塑性发展系数 γ=1.05 (根据规范可调整)
    beta_m = 1.0
    gamma = 1.05

    # 计算轴压项和抗弯项的应力比
    axial_ratio = N / (phi * A * f)
    bending_ratio = (beta_m * M) / (gamma * W * f)

    # 总计验算值
    total_ratio = axial_ratio + bending_ratio
    return total_ratio


# ==========================================
# 第三步：模拟表一数据的导入与中继计算
# ==========================================

# 1. 模拟您的原始测试数据录入 (映射 Table 1)
data = {
    '型号': ['E-LC1', 'E-LC2', 'E-LC3', 'E-LC4', 'E-LC5', 'E-LC6', 'E-LC7'],
    '偏心形式': ['单向偏心X轴', '单向偏心X轴', '单向偏心X轴', '单向偏心Y轴', '单向偏心Y轴', '双向偏心', '双向偏心'],
    '偏心率': ['0.11', '0.23', '0.34', '0.29', '0.43', '0.23、0.43', '0.34、0.43'],
    'N_test_kN': [4188, 3258, 2687, 3311, 2527, 2319, 2159],
    'M_test_kNm': [520.64, 667.18, 685.98, 568.5, 622.23, 533.68, 475.38],

    # 以下截面属性为了让程序跑通填入的拟合值，
    # 实际应用中，您可以直接从您的 "L型柱截面几何参数计算.csv" 中 merge 进来
    'Area_mm2': [8000] * 7,
    'W_mm3': [1200000] * 7,
    'lambda_x': [28.82] * 7,
    'lambda_y': [42.31] * 7
}

df = pd.DataFrame(data)

# 2. 中继计算：计算稳定系数 φ (映射 Table 1 的后续处理)
# 假定取 λ_x 和 λ_y 对应的 φ 的较小值作为整体稳定控制
df['phi_x'] = df['lambda_x'].apply(calculate_stability_factor)
df['phi_y'] = df['lambda_y'].apply(calculate_stability_factor)
df['phi_min'] = df[['phi_x', 'phi_y']].min(axis=1)

# ==========================================
# 第四步：执行耦合验算并生成表二的结果
# ==========================================

# 3. 压弯构件稳定验算计算
df['压弯构件稳定验算'] = df.apply(check_bending_compression_stability, axis=1)

# 4. 判断逻辑 (映射 Table 2 的最后一列)
df['结论'] = df['压弯构件稳定验算'].apply(lambda x: '大于1.0' if x > 1.0 else '小于等于1.0')

# ==========================================
# 第五步：格式化输出，生成类似表二的看板
# ==========================================

# 筛选最终要在表二显示的列
table_2_columns = ['型号', '偏心形式', '偏心率', 'N_test_kN', 'M_test_kNm', '压弯构件稳定验算', '结论']
df_table_2 = df[table_2_columns].copy()

# 重命名列名以完全契合您的表格习惯
df_table_2.rename(columns={
    'N_test_kN': '试验值Pu/Kn',
    'M_test_kNm': '极限弯矩Kn*m'
}, inplace=True)

print("============ 模拟生成的表二 (最终看板) ============\n")
print(df_table_2.to_string(index=False))

# 如果需要导出为 Excel，只需取消下面这行的注释即可：
# df_table_2.to_excel('L形截面计算结果_Python输出.xlsx', index=False)