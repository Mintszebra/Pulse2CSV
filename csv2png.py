import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_all_csvs_in_directory(input_folder, output_folder):
    """
    Reads all CSV files from an input directory, creates a plot for each,
    and saves it as a PNG file to an output directory.

    Args:
        input_folder (str): The path to the directory containing the CSV files.
        output_folder (str): The path to the directory where PNG files will be saved.
    """
    # 檢查輸入資料夾是否存在
    if not os.path.isdir(input_folder):
        print(f"錯誤：找不到輸入資料夾 '{input_folder}'。")
        return

    # 建立輸出資料夾 (如果它不存在的話)
    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(input_folder)
    csv_files = [f for f in files if f.endswith('.csv')]

    if not csv_files:
        print(f"在 '{input_folder}' 資料夾中找不到任何 CSV 檔案。")
        return

    print(f"在 '{input_folder}' 中找到 {len(csv_files)} 個 CSV 檔案。開始處理...")

    for csv_file in csv_files:
        try:
            # 建立完整的輸入檔案路徑
            file_path = os.path.join(input_folder, csv_file)
            
            # 讀取 CSV 檔案
            df = pd.read_csv(file_path)

            # 建立圖表
            plt.figure(figsize=(10, 6))
            
            # 假設 CSV 的欄位名稱為 'x' 和 'y'
            if 'x' in df.columns and 'y' in df.columns:
                plt.plot(df['x'], df['y'])
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title(f'Plot of {csv_file}')

                # 建立輸出檔名
                file_name_without_ext = os.path.splitext(csv_file)[0]
                output_filename = f"{file_name_without_ext}oof.png"
                # 建立完整的輸出檔案路徑
                output_path = os.path.join(output_folder, output_filename)
                
                plt.savefig(output_path)
                plt.close()

                print(f"成功為 {csv_file} 建立圖表，並儲存至 '{output_path}'")
            else:
                print(f"跳過 {csv_file}：找不到 'x' 和 'y' 欄位。")

        except Exception as e:
            print(f"處理 {csv_file} 時發生錯誤：{e}")

# 主程式執行部分
if __name__ == "__main__":
    INPUT_FOLDER = 'maibo_csv_results'      # 指定 CSV 來源資料夾
    OUTPUT_FOLDER = 'csv2png'   # 指定 PNG 輸出資料夾
    plot_all_csvs_in_directory(INPUT_FOLDER, OUTPUT_FOLDER)