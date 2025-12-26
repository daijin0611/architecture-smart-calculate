# 数据解析模块
import re
import pandas as pd


def read_column_data(filename: str) -> dict:
    """
    从SATWE内力输出文件中读取并解析柱（N-C）的内力数据。

    Args:
        filename: 输入文件的路径。

    Returns:
        dict[str, pd.DataFrame]: key为"N-C_{nc_value}"，value为对应柱子的内力DataFrame。
        DataFrame只包含Shear-X到My-Top的列，且过滤掉带*号的iCase。
    """
    columns_data = []
    in_column_section = False
    current_column = None

    force_headers = [
        "Shear-X", "Shear-Y", "Axial", "Mx-Btm", "My-Btm", "Mx-Top", "My-Top"
    ]

    metadata_pattern = re.compile(
        r"N-C\s*=\s*(\d+).*Node-i=\s*(\d+).*Node-j=\s*(\d+).*DL=\s*([\d.]+).*Angle=\s*([\d.-]+)"
    )

    with open(filename, 'r', encoding='gbk') as f:
        for line in f:
            if "柱内力输出：" in line:
                in_column_section = True
                continue

            if in_column_section and ("梁内力输出：" in line or "柱、墙、支撑在竖向力作用下的轴力之和" in line):
                in_column_section = False
                break

            if not in_column_section:
                continue

            line_stripped = line.strip()
            if line_stripped.startswith("N-C ="):
                match = metadata_pattern.search(line)
                if match:
                    current_column = {
                        "N-C": int(match.group(1)),
                        "Node-i": int(match.group(2)),
                        "Node-j": int(match.group(3)),
                        "DL": float(match.group(4)),
                        "Angle": float(match.group(5)),
                        "internal_forces": []
                    }
                    columns_data.append(current_column)
                else:
                    current_column = None
                continue

            if current_column and line_stripped.startswith("("):
                try:
                    closing_paren_index = line.find(')')
                    if closing_paren_index == -1:
                        raise ValueError("行中找不到右括号")

                    i_case = line[:closing_paren_index].strip('( )')
                    values_str = line[closing_paren_index + 1:]
                    values = [float(v) for v in filter(None, values_str.split())]

                    if len(values) != len(force_headers):
                        raise ValueError(f"数值数量不匹配 (期望{len(force_headers)}个, 找到{len(values)}个)")

                    force_data = {"iCase": i_case}
                    force_data.update(dict(zip(force_headers, values)))
                    current_column["internal_forces"].append(force_data)

                except (ValueError, IndexError) as e:
                    print(f"警告: 无法解析行: {line.strip()}, 原因: {e}")
                    continue

    # 转换为DataFrame格式
    df_dict = {}
    for col in columns_data:
        nc_value = col["N-C"]
        rows = []
        for force in col["internal_forces"]:
            rows.append(force)
        
        nc_df = pd.DataFrame(rows)
        
        if 'iCase' in nc_df.columns:
            nc_df = nc_df[~nc_df['iCase'].astype(str).str.contains('*', regex=False, na=False)]
        
        nc_df = nc_df[force_headers].copy()
        nc_df = nc_df.reset_index(drop=True)
        
        df_dict[f"N-C_{nc_value}"] = nc_df
        print(f"处理 N-C={nc_value}: {len(nc_df)} 行，列: {list(nc_df.columns)}")

    total_rows = sum(len(df) for df in df_dict.values())
    print(f"\n处理完成！共 {len(df_dict)} 个柱子，总计 {total_rows} 行数据")

    for key, df_group in df_dict.items():
        print(f"\n{key} 前3行:")
        print(df_group.head(3))

    return df_dict


def load_load_coefficients(file_path: str = "data/荷载系数.xlsx") -> pd.DataFrame:
    """
    读取荷载系数Excel文件并返回DataFrame

    Args:
        file_path: Excel文件路径

    Returns:
        pd.DataFrame: 包含荷载系数数据的DataFrame，保留iCase列用于标识组合工况
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        print(f"成功读取荷载系数文件，共 {len(df)} 行数据")
        print(f"原始列名: {list(df.columns)}")
        print("前5行数据:")
        print(df.head())
        return df
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        return None
    except Exception as e:
        print(f"读取Excel文件时发生错误: {e}")
        return None
