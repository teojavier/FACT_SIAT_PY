class FileAddress:
    def __init__(self, download_directory: str, excel_file_path: str):
        self.download_directory = download_directory
        self.excel_file_path = excel_file_path

    def __str__(self):
        return f"Download Directory: {self.download_directory}, Excel File: {self.excel_file_path}"
