import pandas as pd
import numpy as np
import os
import random
from tqdm import tqdm

def augment_waveform(original_df, 
                     jitter_strength=0.02, 
                     scale_range=(0.98, 1.02), 
                     slice_ratio_range=(0.9, 1.0)):
    """
    對單個波形 DataFrame 進行三種資料擴增：
    1. 抖動 (Jittering): 對 y 值添加微小隨機雜訊
    2. 縮放 (Scaling): 對 y 值進行整體縮放
    3. 切片 (Slicing): 隨機截取原始資料的一部分
    (此函式與前一版相同)
    """
    
    # 複製一份原始資料，避免修改原檔
    df = original_df.copy()
    y_values = df.iloc[:, 1] # 假設 y 是第二欄

    # --- 1. 抖動 (Jittering) ---
    noise_strength = y_values.std() * jitter_strength
    jitter = np.random.normal(0, noise_strength, len(y_values))
    df.iloc[:, 1] = y_values + jitter
    
    # --- 2. 縮放 (Scaling) ---
    scale_factor = random.uniform(scale_range[0], scale_range[1])
    df.iloc[:, 1] = df.iloc[:, 1] * scale_factor
    
    # --- 3. 窗口切片 (Window Slicing) ---
    slice_ratio = random.uniform(slice_ratio_range[0], slice_ratio_range[1])
    original_length = len(df)
    slice_length = int(original_length * slice_ratio)
    
    if slice_length < original_length and slice_length > 0:
        start_index = random.randint(0, original_length - slice_length)
        df = df.iloc[start_index : start_index + slice_length]
    
    # 重設 x 軸
    df.iloc[:, 0] = range(len(df))
    
    return df

# --- 主程式執行區 ---
if __name__ == "__main__":
    
    # --- 1. 請修改這裡的設定 ---
    
    # 原始資料的「基礎」資料夾 (內含 '沉', '中', '浮')
    BASE_INPUT_DIR = 'pulse_data'
    
    # 擴增後資料要存入的「基礎」資料夾
    # (程式會自動在裡面建立 '沉', '中', '浮' 子資料夾)
    BASE_OUTPUT_DIR = 'pulse_data_augmented'
    
    # 指定「每張」原始 CSV 檔要產生多少個擴增檔案
    NUM_AUGMENTATIONS_PER_FILE = 50
    
    # 要處理的壓力級別
    PRESSURE_LEVELS = ['沉', '中', '浮']
    
    # -----------------------------------
    
    print(f"--- 開始批次資料擴增 ---")
    print(f"原始資料夾: {BASE_INPUT_DIR}")
    print(f"輸出資料夾: {BASE_OUTPUT_DIR}")
    print(f"每個檔案擴增: {NUM_AUGMENTATIONS_PER_FILE} 個")
    print(f"--------------------------")
    
    total_files_processed = 0
    total_files_generated = 0

    # 迴圈：處理 '沉', '中', '浮'
    for level in PRESSURE_LEVELS:
        input_dir = os.path.join(BASE_INPUT_DIR, level)
        output_dir = os.path.join(BASE_OUTPUT_DIR, level)
        
        print(f"\n--- 正在處理壓力級別: '{level}' ---")
        print(f"  > 來源: {input_dir}")
        print(f"  > 輸出: {output_dir}")

        # 檢查輸入資料夾是否存在
        if not os.path.isdir(input_dir):
            print(f"  ! 警告：找不到來源資料夾 '{input_dir}'，已跳過。")
            continue
            
        # 建立輸出資料夾 (如果它不存在的話)
        os.makedirs(output_dir, exist_ok=True)
        
        # 找出所有 CSV 檔案
        try:
            csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.csv')]
        except Exception as e:
            print(f"  ! 錯誤：無法讀取資料夾 '{input_dir}'。 {e}")
            continue
            
        if not csv_files:
            print(f"  ! 警告：在 '{input_dir}' 中找不到任何 CSV 檔案。")
            continue
            
        print(f"  > 在 '{level}' 級中找到 {len(csv_files)} 個原始 CSV 檔案。")

        # 迴圈：處理資料夾中的每個 CSV
        for csv_filename in tqdm(csv_files, desc=f"  處理 '{level}' 級"):
            source_file_path = os.path.join(input_dir, csv_filename)
            base_name = os.path.splitext(csv_filename)[0]
            
            # 讀取原始 CSV 檔案
            try:
                original_data = pd.read_csv(source_file_path, header=None, usecols=[0, 1])
                original_data = original_data.apply(pd.to_numeric, errors='coerce').dropna()
                
                if original_data.empty:
                    print(f"  ! 警告：檔案 {csv_filename} 為空或無法解析，已跳過。")
                    continue
                    
            except Exception as e:
                print(f"  ! 錯誤：讀取 {csv_filename} 時發生錯誤: {e}，已跳過。")
                continue
            
            total_files_processed += 1
            
            # 迴圈：產生 N 個擴增檔案
            for i in range(NUM_AUGMENTATIONS_PER_FILE):
                # 1. 產生擴增資料
                augmented_df = augment_waveform(original_data)
                
                # 2. 建立輸出檔案路徑
                #    新檔名例如: 平脈_aug_001.csv
                output_filename = f"{base_name}_aug_{i+1:03d}.csv"
                output_path = os.path.join(output_dir, output_filename)
                
                # 3. 儲存新檔案 (不含標頭和索引)
                try:
                    augmented_df.to_csv(output_path, header=False, index=False)
                    total_files_generated += 1
                except Exception as e:
                    print(f"  ! 錯誤：儲存 {output_path} 時發生錯誤: {e}")

    print(f"\n--- 批次任務完成 ---")
    print(f"總共處理了 {total_files_processed} 個原始 CSV 檔案。")
    print(f"總共產生了 {total_files_generated} 個擴增檔案 (儲存在 '{BASE_OUTPUT_DIR}')。")