from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
def read_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text

    print(full_text[:500]) 

    return full_text

def scrape_webpage_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        raw_text = soup.get_text(separator=" ")

        import re
        clean_text = re.sub(r"\s+", " ", raw_text).strip()
        return clean_text

    except Exception as e:
        print("Error scraping:", e)
        return ""