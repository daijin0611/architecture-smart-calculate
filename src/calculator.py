# 计算模块
import math
import pandas as pd


def calculate_matrix(source: dict, coefficients: pd.DataFrame) -> dict:
    """
    计算荷载组合：对于每种组合工况，将各原始工况的内力值乘以对应的荷载系数后求和。
    
    Args:
        source: dict[str, pd.DataFrame]，每个柱子的原始内力数据，行是工况(1-10)，列是内力分量
        coefficients: pd.DataFrame，荷载系数表，行是组合工况，列名是原始工况号
    
    Returns:
        dict[str, pd.DataFrame]: 每个柱子的组合后内力结果
    """
    if source is None or coefficients is None:
        print("\n数据加载失败，无法进行矩阵相乘计算")
        return None

    print("\n=== 开始荷载组合计算 ===")
    result_dict = {}

    try:
        coef_df = coefficients.copy()
        if 'iCase' in coef_df.columns:
            icase_col = coef_df['iCase'].values
            coef_df = coef_df.drop('iCase', axis=1)
        else:
            icase_col = list(range(1, len(coef_df) + 1))
        
        coef_df.columns = [str(int(c)) for c in coef_df.columns]
        sorted_cols = sorted(coef_df.columns, key=lambda x: int(x))
        coef_df = coef_df[sorted_cols]
        
        print(f"荷载系数矩阵形状: {coef_df.shape}")
        print(f"荷载系数对应的原始工况: {sorted_cols}")

        for column_name, source_data in source.items():
            print(f"\n正在处理 {column_name}...")
            
            n_source_cases = len(source_data)
            n_coef_cases = len(sorted_cols)
            
            if n_source_cases != n_coef_cases:
                print(f"警告: {column_name} 源数据工况数({n_source_cases})与荷载系数工况数({n_coef_cases})不一致")
            
            source_numeric = source_data.astype(float).values
            coef_numeric = coef_df.astype(float).values
            
            print(f"源数据矩阵形状: {source_numeric.shape}")
            print(f"荷载系数矩阵形状: {coef_numeric.shape}")
            
            result_matrix = coef_numeric @ source_numeric
            
            result_df = pd.DataFrame(
                result_matrix,
                index=[f"组合工况_{int(i)}" for i in icase_col],
                columns=source_data.columns.tolist()
            )
            
            result_dict[column_name] = result_df
            
            print(f"{column_name} 计算完成！结果形状: {result_df.shape}")
            print(f"{column_name} 前5行结果:")
            print(result_df.head())

        print(f"\n所有荷载组合计算完成！共处理 {len(result_dict)} 个柱子")
        return result_dict

    except Exception as e:
        print(f"荷载组合计算时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def calculate_result():
    """计算最终结果（E-LC1单向偏心x轴构件）"""
    # 轴力相关
    N_test = 3258
    M_u = 667.18
    gamma_Q355 = 1.125
    N_design = N_test / gamma_Q355

    # 弯矩设计值
    MY_design = M_u / gamma_Q355
    Mx_design = 524.612604237573
    My_design = 276.565724715513

    # 材料与截面特性
    E = 206000.0
    f = 305.0
    A = 18494.0
    L = 4420.0

    # 惯性矩
    Ix = 434951975.694101
    Iy = 201839459.161942

    # 扭转与翘曲常数
    It = 1611474.66666667
    Iw = 1509267318274.58

    # 不对称常数
    beta_x = 145.1702474
    beta_y = 74.6339493

    # 截面模量
    Wx = 1503396.00931591
    Wy = 957075.12411876

    # 换算长细比
    lambda_ = 71.6472448398353
    lambda_x = 28.821530683574
    lambda_y = 42.3091849493257

    # 稳定系数
    phi_y = 0.8995
    phi_bx = 1.0

    # 塑性发展系数
    gamma_x = 1.05
    gamma_y = 1.05
    eta = 1.0

    # 等效弯矩系数
    beta_my = 1.0

    # 最终结果
    N_Ey = (math.pow(math.pi, 2) * E * A) / (1.1 * math.pow(lambda_y, 2))
    print(f"N_Ey: {N_Ey}")

    N_Ey_ratio = (N_test * 1000) / (phi_y * A * f) \
        + (eta * Mx_design * 1000000) / (phi_bx * gamma_x * Wx * f) \
        + (beta_my * My_design * 1000000) / (gamma_y * Wy * f * (1 - 0.8 * N_test * 1000 / N_Ey))
    print(f"N_Ey_ratio: {N_Ey_ratio}")
    return N_Ey, N_Ey_ratio
