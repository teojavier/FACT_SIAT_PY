from pathlib import Path

class PDFInvoiceChecker:
    def __init__(self, file_address):
        self.file_address = file_address

    def count_pdfs(self):
        directory = Path(self.file_address.download_directory)
        return len(list(directory.glob("*.pdf")))

    def check_fields_in_pdfs(self, dir_pdf, name, nit, code):
        print('check')
    
    
    def build_response(self, count_pdf, count_name, count_nit, count_code):
        print('response')
