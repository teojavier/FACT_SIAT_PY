import tkinter as tk
import traceback
import PyPDF2
import os

from tkinter import messagebox, filedialog

from data.BaseUrlSiat import BaseUrlSiat
from data.FileAddress import FileAddress
from business.PDFInvoiceDownloader import PDFInvoiceDownloader
from business.ExcelDataExtractor import ExcelDataExtractor
from data.UtilDownload import UtilDownload
from business.PDFInvoiceChecker import PDFInvoiceChecker

class PPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("EJECUTADOR DE FACTURAS SIAT")
        self.root.geometry("950x650")
        self.root.config(bg="#dbdbdb")
        
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
        font_style_label = ("Arial", 12, "bold")
        font_style_entry = ("Arial", 12)
        entry_width = 45
        entry_width_small = 12
        entry_width_verify = 65
        padding_y = 3
        
        tk.Label(self.root, text="Siat: url", font=font_style_label).pack(pady=padding_y)
        self.entry_url_siat = tk.Entry(self.root, width=entry_width, font=font_style_entry)
        self.entry_url_siat.insert(0, self.base_url_siat.url_siat)
        self.entry_url_siat.pack(pady=padding_y)

        # Crear un Frame para datos del siat
        frame_info_siat = tk.Frame(self.root)
        frame_info_siat.pack(pady=10)

        # Etiqueta y campo para NIT
        tk.Label(frame_info_siat, text="Siat: nit", font=font_style_label).grid(row=0, column=0, padx=5)
        self.entry_nit = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_nit.insert(0, self.base_url_siat.nit)
        self.entry_nit.grid(row=0, column=1, padx=5)

        # Etiqueta y campo para CUF
        tk.Label(frame_info_siat, text="Siat: cuf", font=font_style_label).grid(row=0, column=2, padx=5)
        self.entry_cuf = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_cuf.insert(0, self.base_url_siat.cuf)
        self.entry_cuf.grid(row=0, column=3, padx=5)

        # Etiqueta y campo para Número de Factura
        tk.Label(frame_info_siat, text="Siat: número de Factura", font=font_style_label).grid(row=0, column=4, padx=5)
        self.entry_nro_factura = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_nro_factura.insert(0, self.base_url_siat.nro_factura)
        self.entry_nro_factura.grid(row=0, column=5, padx=5)

        # Etiqueta y campo para Tipo
        tk.Label(frame_info_siat, text="Siat: tipo", font=font_style_label).grid(row=0, column=6, padx=5)
        self.entry_tipo = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_tipo.insert(0, self.base_url_siat.tipo)
        self.entry_tipo.grid(row=0, column=7, padx=5)

        # Crear un Frame para datos del siat
        frame_time_btn = tk.Frame(self.root)
        frame_time_btn.pack(pady=10)

        tk.Label(frame_time_btn, text="Tiempo de descarga (segundos):", font=font_style_label).grid(row=0, column=0, padx=5)
        self.entry_timer = tk.Entry(frame_time_btn, width=5, font=font_style_entry)
        self.entry_timer.insert(0, str(self.util_download.seconds_download))
        self.entry_timer.grid(row=0, column=1, padx=5)

        tk.Label(frame_time_btn, text="Texto del botón:", font=font_style_label).grid(row=0, column=2, padx=5)
        self.entry_btn_name = tk.Entry(frame_time_btn, width=15, font=font_style_entry)
        self.entry_btn_name.insert(0, str(self.util_download.btn_name))
        self.entry_btn_name.grid(row=0, column=3, padx=5)
        
        # Selector de carpeta para Descargas
        tk.Label(self.root, text="Directorio de Descargas:", font=font_style_label).pack(pady=padding_y)
        frame_download = tk.Frame(self.root)
        frame_download.pack(pady=padding_y)
        
        self.entry_download_directory = tk.Entry(frame_download, width=entry_width, font=font_style_entry)
        self.entry_download_directory.insert(0, self.file_address.download_directory)
        self.entry_download_directory.pack(side=tk.LEFT)
        
        tk.Button(frame_download, text="📂", command=self.select_download_directory, bg="yellow", fg="black").pack(side=tk.LEFT, padx=5)

        # Selector de archivo Excel
        tk.Label(self.root, text="Directorio Archivo Excel:", font=font_style_label).pack(pady=padding_y)
        frame_excel = tk.Frame(self.root)
        frame_excel.pack(pady=padding_y)
        
        self.entry_excel_file = tk.Entry(frame_excel, width=entry_width, font=font_style_entry)
        self.entry_excel_file.insert(0, self.file_address.excel_file_path)
        self.entry_excel_file.pack(side=tk.LEFT)
        
        tk.Button(frame_excel, text="📄", command=self.select_excel_file, bg="lightgreen", fg="black").pack(side=tk.LEFT, padx=5)

        # ✅ Checkbox para unir los PDFs
        self.merge_pdfs_var = tk.IntVar(value=0)  # 1 = Activado, 0 = Desactivado
        self.checkbox_merge_pdfs = tk.Checkbutton(self.root, text="¿Unir los PDF?", font=font_style_label, variable=self.merge_pdfs_var)
        self.checkbox_merge_pdfs.pack(pady=3)
        
        # Línea separadora (Canvas)
        canvas_separator = tk.Canvas(self.root, width=900, height=2, bg="black")
        canvas_separator.pack(pady=10)

        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="💾 Guardar Cambios", command=self.save_changes, font=font_style_entry, bg="lightblue", fg="black").pack(side="left", padx=5)
        tk.Button(frame_buttons, text="🚀 Ejecutar Script", command=self.execute_script, font=font_style_entry, bg="lightgreen", fg="black").pack(side="left", padx=5)
        tk.Button(frame_buttons, text="📑 Unir todos los PDF", command=self.join_all_pdfs, font=font_style_entry, bg="pink", fg="black").pack(side="left", padx=5)

        # Campos para verificar
        tk.Label(self.root , text="Nombre / Razón Social:", font=font_style_label).pack(pady=padding_y)
        self.entry_name_social_reason = tk.Entry(self.root , width=entry_width_verify, font=font_style_entry)
        self.entry_name_social_reason.insert(0, str(''))
        self.entry_name_social_reason.pack(pady=padding_y)

        tk.Label(self.root , text="NIT / CI / CEX:", font=font_style_label).pack(pady=padding_y)
        self.entry_nit_ci_cex = tk.Entry(self.root , width=entry_width_verify, font=font_style_entry)
        self.entry_nit_ci_cex.insert(0, str(''))
        self.entry_nit_ci_cex.pack(pady=padding_y)

        tk.Label(self.root , text="Cod. Cliente:", font=font_style_label).pack(pady=padding_y)
        self.entry_cod_client= tk.Entry(self.root , width=entry_width_verify, font=font_style_entry)
        self.entry_cod_client.insert(0, str(''))
        self.entry_cod_client.pack(pady=padding_y)

        tk.Button(self.root, text="🔎 Verificar Datos", command=self.verify_data_pdf, font=font_style_entry, bg="purple", fg="white").pack(pady=15)


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
            self.join_all_pdfs()

            messagebox.showinfo("Éxito", "Finalizó la ejecución del Script")
        except Exception as e:
            
            error_message = f"Ocurrió un error: {str(e)}"
            pdf_invoice_downloader.driver.quit()
            traceback.print_exc()  
            messagebox.showerror("Error", error_message)


    def join_all_pdfs(self):
        download_dir = os.path.abspath(self.file_address.download_directory)
        output_pdf_path = os.path.join(download_dir, "consolidado_de_facturas.pdf")

        # Obtener la lista de archivos PDF en el directorio, ordenados por nombre ASCENDENTE
        pdf_files = sorted(
            [f for f in os.listdir(download_dir) if f.lower().endswith(".pdf")]
        )

        if not pdf_files:
            messagebox.showwarning("Advertencia", "No hay archivos PDF en el directorio para unir.")
            return

        # Crear un objeto PDFMerger
        pdf_merger = PyPDF2.PdfMerger()

        # Agregar los PDFs al objeto de fusión
        for pdf_file in pdf_files:
            pdf_merger.append(os.path.join(download_dir, pdf_file))

        # Guardar el PDF final
        pdf_merger.write(output_pdf_path)
        pdf_merger.close()

        messagebox.showinfo("Éxito", f"PDFs unidos exitosamente en:\n{output_pdf_path}")

    def verify_data_pdf(self):
        try:
            pdf_invoice_cheker = PDFInvoiceChecker(
                file_address=self.file_address
            )

            print(str(pdf_invoice_cheker.count_pdfs()))

            # print(pdf_invoice_cheker.check_fields_in_pdfs('D:\Proyectos Trabajo\FACT_SIAT_PY\descargas\Factura 1.pdf','MONTALVO SILES TEO JAVIER','9620066','C873936'))

            # messagebox.showinfo("Éxito", "Finalizó la ejecución del Script")
        except Exception as e:
            
            error_message = f"Ocurrió un error: {str(e)}"
            # pdf_invoice_downloader.driver.quit()
            traceback.print_exc()  
            messagebox.showerror("Error", error_message)
