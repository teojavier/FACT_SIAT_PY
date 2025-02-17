import tkinter as tk
import traceback

from tkinter import messagebox, filedialog

from data.BaseUrlSiat import BaseUrlSiat
from data.FileAddress import FileAddress
from business.PDFInvoiceDownloader import PDFInvoiceDownloader
from business.ExcelDataExtractor import ExcelDataExtractor
from data.UtilDownload import UtilDownload

class PPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("TJMS SIAT EJECUTADOR")
        self.root.geometry("600x750")
        
        # Objetos con valores iniciales
        self.base_url_siat = BaseUrlSiat(
            url_siat="https://siat.impuestos.gob.bo/consulta/QR?",
            nit="nit=",
            cuf="&cuf=",
            nro_factura="&numero=",
            tipo="&t="
        )

        self.util_download = UtilDownload(seconds_download=2, btn_name='Ver Factura')

        self.file_address = FileAddress(
            download_directory='',
            excel_file_path=''
        )

        # Crear los inputs
        self.create_inputs()
    
    def create_inputs(self):
        font_style = ("Arial", 12)
        entry_width = 45
        padding_y = 5
        
        tk.Label(self.root, text="URL SIAT:", font=font_style).pack(pady=padding_y)
        self.entry_url_siat = tk.Entry(self.root, width=entry_width, font=font_style)
        self.entry_url_siat.insert(0, self.base_url_siat.url_siat)
        self.entry_url_siat.pack(pady=padding_y)
        
        tk.Label(self.root, text="NIT:", font=font_style).pack(pady=padding_y)
        self.entry_nit = tk.Entry(self.root, width=entry_width, font=font_style)
        self.entry_nit.insert(0, self.base_url_siat.nit)
        self.entry_nit.pack(pady=padding_y)
        
        tk.Label(self.root, text="CUF:", font=font_style).pack(pady=padding_y)
        self.entry_cuf = tk.Entry(self.root, width=entry_width, font=font_style)
        self.entry_cuf.insert(0, self.base_url_siat.cuf)
        self.entry_cuf.pack(pady=padding_y)
        
        tk.Label(self.root, text="Número de Factura:", font=font_style).pack(pady=padding_y)
        self.entry_nro_factura = tk.Entry(self.root, width=entry_width, font=font_style)
        self.entry_nro_factura.insert(0, self.base_url_siat.nro_factura)
        self.entry_nro_factura.pack(pady=padding_y)
        
        tk.Label(self.root, text="Tipo:", font=font_style).pack(pady=padding_y)
        self.entry_tipo = tk.Entry(self.root, width=entry_width, font=font_style)
        self.entry_tipo.insert(0, self.base_url_siat.tipo)
        self.entry_tipo.pack(pady=padding_y)
        
        tk.Label(self.root, text="Tiempo de descarga (segundos):", font=font_style).pack(pady=padding_y)
        self.entry_timer = tk.Entry(self.root, width=entry_width, font=font_style)
        self.entry_timer.insert(0, str(self.util_download.seconds_download))
        self.entry_timer.pack(pady=padding_y)

        tk.Label(self.root, text="Texto del botón:", font=font_style).pack(pady=padding_y)
        self.entry_btn_name = tk.Entry(self.root, width=entry_width, font=font_style)
        self.entry_btn_name.insert(0, str(self.util_download.btn_name))
        self.entry_btn_name.pack(pady=padding_y)
        
        # Selector de carpeta para Descargas
        tk.Label(self.root, text="Directorio de Descargas:", font=font_style).pack(pady=padding_y)
        frame_download = tk.Frame(self.root)
        frame_download.pack(pady=padding_y)
        
        self.entry_download_directory = tk.Entry(frame_download, width=entry_width, font=font_style)
        self.entry_download_directory.insert(0, self.file_address.download_directory)
        self.entry_download_directory.pack(side=tk.LEFT)
        
        tk.Button(frame_download, text="📂", command=self.select_download_directory).pack(side=tk.LEFT, padx=5)

        # Selector de archivo Excel
        tk.Label(self.root, text="Directorio Archivo Excel:", font=font_style).pack(pady=padding_y)
        frame_excel = tk.Frame(self.root)
        frame_excel.pack(pady=padding_y)
        
        self.entry_excel_file = tk.Entry(frame_excel, width=entry_width, font=font_style)
        self.entry_excel_file.insert(0, self.file_address.excel_file_path)
        self.entry_excel_file.pack(side=tk.LEFT)
        
        tk.Button(frame_excel, text="📄", command=self.select_excel_file).pack(side=tk.LEFT, padx=5)
        
        # Botón para guardar cambios
        tk.Button(self.root, text="Guardar Cambios", command=self.save_changes, font=font_style, bg="lightblue", fg="black").pack(pady=15)

        # Botón para ejecutar script
        tk.Button(self.root, text="Ejecutar Script", command=self.execute_script, font=font_style, bg="lightgreen", fg="black").pack(pady=15)

    def select_download_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_download_directory.delete(0, tk.END)
            self.entry_download_directory.insert(0, directory)

    def select_excel_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            self.entry_excel_file.delete(0, tk.END)
            self.entry_excel_file.insert(0, file_path)

    def save_changes(self):
        # Actualizar los valores de los objetos con los nuevos valores de los inputs
        self.base_url_siat.url_siat = self.entry_url_siat.get()
        self.base_url_siat.nit = self.entry_nit.get()
        self.base_url_siat.cuf = self.entry_cuf.get()
        self.base_url_siat.nro_factura = self.entry_nro_factura.get()
        self.base_url_siat.tipo = self.entry_tipo.get()
        
        self.util_download.seconds_download = int(self.entry_timer.get())
        self.util_download.btn_name = str(self.entry_btn_name.get())

        
        self.file_address.download_directory = self.entry_download_directory.get()
        self.file_address.excel_file_path = self.entry_excel_file.get()
        
        messagebox.showinfo("Éxito", "Datos guardados correctamente")
        
    def execute_script(self):
        try:
            excel_data_extractor = ExcelDataExtractor(self.file_address.excel_file_path, self.base_url_siat)
            pdf_invoice_downloader = PDFInvoiceDownloader(
                file_address=self.file_address,
                excel_data_extractor=excel_data_extractor,
                util_download=self.util_download
            )
            
            pdf_invoice_downloader.download_invoices()
            messagebox.showinfo("Éxito", "Script ejecutado correctamente")
        except Exception as e:
            
            error_message = f"Ocurrió un error: {str(e)}"
            pdf_invoice_downloader.driver.quit()
            traceback.print_exc()  
            messagebox.showerror("Error", error_message)