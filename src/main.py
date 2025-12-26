# 主入口
from parser import read_column_data, load_load_coefficients
from calculator import calculate_matrix
from utils import load_file, save_results_to_excel


def main():
    # 获取文件路径
    file_path = load_file()
    if not file_path:
        print("未选择文件，程序退出")
        return
    
    # 加载原始数据
    source_data = read_column_data(file_path)
    
    # 加载荷载系数
    load_coefficients_df = load_load_coefficients()
    
    # 计算荷载组合
    result = calculate_matrix(source_data, load_coefficients_df)
    
    # 保存结果
    save_results_to_excel(result)
    
    print("\n程序执行完成，请按任意键退出...")
    input()


if __name__ == '__main__':
    main()
