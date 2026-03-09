import re
import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    return text

def regex_extract(text):
    raw_containers = re.findall(r'\b[A-Z]{4}\d{7}\b', text)
    containers = list(set([str(c) for c in raw_containers]))

    mbl = ""
    mbl_pattern = r'(?i)(?:B/L|MBL|WAYBILL|BILL OF LADING|INVOICE)\s*(?:NO\.?)?[:\s#]+([A-Z0-9]{8,20})'
    mbl_match = re.search(mbl_pattern, text)
    
    if mbl_match:
        mbl = mbl_match.group(1).strip()
    
        if "ONEY" + mbl in text:
            mbl = "ONEY" + mbl

    total_matches = re.findall(r'(?i)(?:Total|Amount|Collect|Due)[:\s]*\$?\s*([\d,]+\.\d{2})(?!\s*(?:KGS|LBS|CBM|PCK|WEIGHT|Lbs|Kgs))', text)
    total = total_matches[-1] if total_matches else ""

    return {
        "MBL": str(mbl),
        "Container": containers,
        "Total": str(total)
    }