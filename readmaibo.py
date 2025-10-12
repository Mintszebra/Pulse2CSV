import cv2
import numpy as np
import csv
import os

def extract_waveform_from_image(image_path):
    """
    從單一圖片中提取黑色/深色波形的座標。
    """
    try:
        raw_data = np.fromfile(image_path, dtype=np.uint8)
        image = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)
        if image is None:
            return []
    except Exception:
        return []

    # 轉換到 HSV 顏色空間
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # --- 修改部分：將顏色定義從紅色改為黑色 ---
    # 在 HSV 中，黑色的定義主要看 V (Value/亮度)。
    # 我們設定一個較大的 H 和 S 範圍，但嚴格限制 V 的上限。
    # 這可以同時偵測到黑色、深灰色等線條。
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 60]) # V 的上限 60 可依情況調整

    # 根據範圍建立黑色的遮罩
    line_mask = cv2.inRange(hsv_image, lower_black, upper_black)
    # -----------------------------------------------

    # 提取座標
    coordinates = []
    height, width, _ = image.shape
    for x in range(width):
        # 從 line_mask 中尋找線條的 y 座標
        line_y_indices = np.where(line_mask[:, x] > 0)[0]
        if line_y_indices.size > 0:
            avg_y = int(np.mean(line_y_indices))
            coordinates.append((x, avg_y))
            
    return coordinates

def save_coords_to_csv(output_path, coordinates):
    """
    將座標資料寫入指定的 CSV 檔案。
    (此函式無需修改)
    """
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['x', 'y'])
            writer.writerows(coordinates)
        return True
    except IOError:
        return False

# --- 主程式執行區 (此區塊無需修改) ---
if __name__ == "__main__":
    INPUT_FOLDER = 'maibo'

    if not os.path.isdir(INPUT_FOLDER):
        print(f"錯誤：找不到名為 '{INPUT_FOLDER}' 的資料夾。")
        exit()

    folder_name = os.path.basename(INPUT_FOLDER)
    OUTPUT_FOLDER = f"{folder_name}_csv_results"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"所有產出的 CSV 檔案將會儲存在 '{OUTPUT_FOLDER}' 資料夾中。")
    
    ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', 'tiff')
    
    print(f"\n開始掃描資料夾 '{INPUT_FOLDER}' 中的圖片...")
    
    try:
        filenames = sorted(os.listdir(INPUT_FOLDER))
    except FileNotFoundError:
        print(f"錯誤：無法存取資料夾 '{INPUT_FOLDER}'。")
        exit()

    total_files = 0
    success_files = 0
    for filename in filenames:
        if filename.lower().endswith(ALLOWED_EXTENSIONS):
            total_files += 1
            current_image_path = os.path.join(INPUT_FOLDER, filename)
            print(f"  - 正在處理: {filename}")
            
            coords = extract_waveform_from_image(current_image_path)
            
            if coords:
                base_name = os.path.splitext(filename)[0]
                output_csv_name = f"{base_name}.csv"
                output_csv_path = os.path.join(OUTPUT_FOLDER, output_csv_name)
                
                if save_coords_to_csv(output_csv_path, coords):
                    print(f"    -> 成功！座標已儲存至 {output_csv_path}")
                    success_files += 1
                else:
                    print(f"    -> 錯誤！無法寫入檔案 {output_csv_path}")
            else:
                 print(f"    -> 警告：無法讀取或未在此圖片中找到波形: {filename}")
    
    print("\n處理完畢。")
    print(f"總共掃描 {total_files} 張圖片，成功生成 {success_files} 個 CSV 檔案。")