import os
import csv
from pdf_extractor import extract_text_from_pdf, regex_extract
from llm_extractor import load_local_llm, extract_from_text

MODEL_PATH = "models/LFM2-2.6B_q4_k_m.gguf"
PDF_FOLDER = "sample_pdfs"
OUTPUT_CSV = "extracted_shipments.csv"

def main():
    if not os.path.exists(PDF_FOLDER):
        print(f"Error: Folder '{PDF_FOLDER}' not found.")
        return

    print("Loading LLM for fallback...")
    llm = load_local_llm(MODEL_PATH)
    
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    with open(OUTPUT_CSV, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["File", "MBL or Invoice", "Container", "Total"])
        writer.writeheader()

        for pdf_file in pdf_files:
            print(f"\n--- Processing: {pdf_file} ---")
            full_text = extract_text_from_pdf(os.path.join(PDF_FOLDER, pdf_file))
            
            data = regex_extract(full_text)
            
            #fallback
            for key in ["MBL", "Container", "Total"]:
                if not data.get(key): 
                    print(f"{key} missing, asking LLM...")
                    llm_data = extract_from_text(full_text, llm)
                    data[key] = llm_data.get(key, "")

            data["MBL or Invoice"] = data.pop("MBL", "")
            data["File"] = pdf_file

            writer.writerow(data)
            print(f"final data: {data}")

if __name__ == "__main__":
    main()