# Shipping-Data-Extractor

這個專案可以從 PDF 檔案中抽取運單資料（MBL or Invoice / Container / Total Amount）。  
先使用 **正規表達式（Regex）** 做快速抽取，如果資料缺漏，再使用 **本地 LLM 模型** （`LFM2-2.6B_q4_k_m.gguf`）進行補足。

---

## 功能特色
- 從 **文字型 PDF** 中抽取 MBL or Invoice、Container、Total Amount  
- 使用 **本地 LLM 模型** 作為 Regex 的補充，處理複雜或缺漏資料  
- 將抽取結果 **輸出成 CSV** 檔案  

---

## 系統需求
- Python
- pip 套件管理工具  
- 本地 LLM 模型（ `LFM2-2.6B_q4_k_m.gguf`）  

---

## 安裝步驟

1. **下載或複製專案**  

```bash
git clone https://github.com/jenny9800/Shipping-Data-Extractor.git
cd Extracter
```

2. **建立虛擬環境**  
 ```bash
python -m venv env
source env/bin/activate   # macOS/Linux
 ```

3. **建立虛擬環境**  
 ```bash
pip install -r requirements.txt
 ```

4. **下載本地 LLM 模型**
   
  [下載 LFM2-2.6B 模型](https://huggingface.co/Sadiah/ollama-q4_k_m-LFM2-2.6B/tree/main)  

   請先從官方連結下載 LFM2-2.6B_q4_k_m.gguf，放入專案的 models/ 資料夾，才能執行程式
---
## 執行程式
 ```bash
python main.py
 ```
程式流程：
1. 遍歷 sample_pdfs/ 資料夾中的所有 PDF
2. 使用 Regex 快速抽取運單資料
3. 若資料缺漏，使用 LLM 模型補充
4. 將結果存入 extracted_shipments.csv

輸出結果如下
<img width="832" height="143" alt="Screen Shot 2026-03-09 at 3 50 19 PM" src="https://github.com/user-attachments/assets/fdcbceaf-7905-48ed-8f0e-4bb79fa94a77" />

   
