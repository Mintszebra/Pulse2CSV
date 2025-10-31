import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# --- 中文字型設定 (與原始版本相同) ---
try:
    plt.rcParams['font.family'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False 
    print("已設定字型為 'Microsoft JhengHei'")
except RuntimeError:
    try:
        plt.rcParams['font.family'] = 'PingFang TC'
        plt.rcParams['axes.unicode_minus'] = False
        print("已設定字型為 'PingFang TC'")
    except RuntimeError:
        try:
            plt.rcParams['font.family'] = 'Noto Sans CJK TC'
            plt.rcParams['axes.unicode_minus'] = False
            print("已設定字型為 'Noto Sans CJK TC'")
        except RuntimeError:
            print("警告：找不到常見的中文字型。中文可能仍會顯示為亂碼。")

# --- 主程式執行部分 (已升級為批次處理) ---
if __name__ == "__main__":

    # --- 1. 請設定路徑 ---
    
    # 指定擴增 CSV 的「基礎」來源資料夾
    BASE_INPUT_DIR = 'pulse_data_augmented'
    
    # 指定 PNG 圖片要輸出的「基礎」資料夾
    BASE_OUTPUT_DIR = 'csv2png_augmented'
    
    # 要處理的壓力級別
    PRESSURE_LEVELS = ['沉', '中', '浮']
    
    # --------------------------

    print(f"\n--- 開始批次轉換 CSV to PNG ---")
    print(f"來源: {BASE_INPUT_DIR}")
    print(f"輸出: {BASE_OUTPUT_DIR}")
    print(f"---------------------------------")
    
    total_files_processed = 0
    total_files_generated = 0

    # 迴圈：處理 '沉', '中', '浮'
    for level in PRESSURE_LEVELS:
        input_folder = os.path.join(BASE_INPUT_DIR, level)
        output_folder = os.path.join(BASE_OUTPUT_DIR, level)
        
        print(f"\n--- 正在處理壓力級別: '{level}' ---")

        # 檢查輸入資料夾是否存在
        if not os.path.isdir(input_folder):
            print(f"  ! 警告：找不到來源資料夾 '{input_folder}'，已跳過。")
            continue
            
        # 建立輸出資料夾 (如果它不存在的話)
        os.makedirs(output_folder, exist_ok=True)
        
        # 找出所有 CSV 檔案
        try:
            csv_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.csv')]
        except Exception as e:
            print(f"  ! 錯誤：無法讀取資料夾 '{input_folder}'。 {e}")
            continue
            
        if not csv_files:
            print(f"  ! 警告：在 '{input_folder}' 中找不到任何 CSV 檔案。")
            continue

        # 迴圈：處理資料夾中的每個 CSV
        for csv_file in tqdm(csv_files, desc=f"  轉換 '{level}' 級"):
            file_path = os.path.join(input_folder, csv_file)
            
            try:
                # --- 【關鍵修正】 ---
                # 讀取 CSV 時，指定 header=None (沒有標頭)
                # 並手動將欄位命名為 'x' 和 'y'
                df = pd.read_csv(file_path, header=None, names=['x', 'y'])
                # ---------------------

                # 建立圖表
                plt.figure(figsize=(10, 6))
                
                # 接下來的程式碼可以正常運作了
                plt.plot(df['x'], df['y'])
                plt.xlabel('x (Time Step)')
                plt.ylabel('y (Value)')
                plt.title(f'Plot of {csv_file}') 

                # 建立輸出檔名
                file_name_without_ext = os.path.splitext(csv_file)[0]
                output_filename = f"{file_name_without_ext}.png"
                output_path = os.path.join(output_folder, output_filename)
                
                plt.savefig(output_path)
                plt.close() # 關閉圖表以釋放記憶體
                
                total_files_generated += 1
                total_files_processed += 1

            except Exception as e:
                print(f"  ! 處理 {csv_file} 時發生錯誤：{e}")

    print(f"\n--- 批次轉換完成 ---")
    print(f"總共處理了 {total_files_processed} 個 CSV 檔案。")
    print(f"總共產生了 {total_files_generated} 個 PNG 圖片 (儲存在 '{BASE_OUTPUT_DIR}')。")