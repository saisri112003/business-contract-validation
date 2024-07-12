import fitz

def extract_text_from_pdf(pdf_path:str) -> str:
                    doc = fitz.open(pdf_path)
                    text = ""

                    for  page_num in range(doc.page_count):
                     page = doc.load_page(page_num)
                    text += page.get_text()

                    return text

if __name__=="__main__":
    pdf_path = "D:\sai\Contract_0.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)