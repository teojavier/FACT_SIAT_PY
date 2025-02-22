import tkinter as tk
import traceback
import PyPDF2
import os
import pandas as pd

from tkinter import messagebox, filedialog

from data.BaseUrlSiat import BaseUrlSiat
from data.FileAddress import FileAddress
from business.PDFInvoiceDownloader import PDFInvoiceDownloader
from business.ExcelDataExtractor import ExcelDataExtractor
from data.UtilDownload import UtilDownload

class PPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("EJECUTADOR DE FACTURAS SIAT")
        self.root.geometry("950x450")
        self.root.config(bg="#e6f2ff")
        
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

        # Crear los componentes
        self.create_menu()
        self.create_inputs()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        # Crear el menú "Archivo"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Acerca de", menu=file_menu)
        file_menu.add_command(label="Información de la aplicación", command=self.info_app)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
    
    def create_inputs(self):
        font_style_label = ("Arial", 12, "bold")
        font_style_entry = ("Arial", 12)
        entry_width = 45
        entry_width_small = 12
        padding_y = 3
        bg_required = "#FFF3CD"
        fg_required = "#856404"
        
        tk.Label(self.root, text="Siat: url", font=font_style_label, bg=bg_required, fg=fg_required).pack(pady=padding_y)
        self.entry_url_siat = tk.Entry(self.root, width=entry_width, font=font_style_entry)
        self.entry_url_siat.insert(0, self.base_url_siat.url_siat)
        self.entry_url_siat.pack(pady=padding_y)

        # Crear un Frame para datos del siat
        frame_info_siat = tk.Frame(self.root)
        frame_info_siat.pack(pady=10)

        # Etiqueta y campo para NIT
        tk.Label(frame_info_siat, text="Siat: nit", font=font_style_label, bg=bg_required, fg=fg_required).grid(row=0, column=0, padx=5)
        self.entry_nit = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_nit.insert(0, self.base_url_siat.nit)
        self.entry_nit.grid(row=0, column=1, padx=5)

        # Etiqueta y campo para CUF
        tk.Label(frame_info_siat, text="Siat: cuf", font=font_style_label, bg=bg_required, fg=fg_required).grid(row=0, column=2, padx=5)
        self.entry_cuf = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_cuf.insert(0, self.base_url_siat.cuf)
        self.entry_cuf.grid(row=0, column=3, padx=5)

        # Etiqueta y campo para Número de Factura
        tk.Label(frame_info_siat, text="Siat: número de Factura", font=font_style_label, bg=bg_required, fg=fg_required).grid(row=0, column=4, padx=5)
        self.entry_nro_factura = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_nro_factura.insert(0, self.base_url_siat.nro_factura)
        self.entry_nro_factura.grid(row=0, column=5, padx=5)

        # Etiqueta y campo para Tipo
        tk.Label(frame_info_siat, text="Siat: tipo", font=font_style_label, bg=bg_required, fg=fg_required).grid(row=0, column=6, padx=5)
        self.entry_tipo = tk.Entry(frame_info_siat, width=entry_width_small, font=font_style_entry)
        self.entry_tipo.insert(0, self.base_url_siat.tipo)
        self.entry_tipo.grid(row=0, column=7, padx=5)

        # Crear un Frame para datos del siat
        frame_time_btn = tk.Frame(self.root)
        frame_time_btn.pack(pady=10)

        tk.Label(frame_time_btn, text="Tiempo de descarga (segundos):", font=font_style_label, bg=bg_required, fg=fg_required).grid(row=0, column=0, padx=5)
        self.entry_timer = tk.Entry(frame_time_btn, width=5, font=font_style_entry)
        self.entry_timer.insert(0, str(self.util_download.seconds_download))
        self.entry_timer.grid(row=0, column=1, padx=5)

        tk.Label(frame_time_btn, text="Texto del botón:", font=font_style_label, bg=bg_required, fg=fg_required).grid(row=0, column=2, padx=5)
        self.entry_btn_name = tk.Entry(frame_time_btn, width=15, font=font_style_entry)
        self.entry_btn_name.insert(0, str(self.util_download.btn_name))
        self.entry_btn_name.grid(row=0, column=3, padx=5)
        
        # Selector de carpeta para Descargas
        tk.Label(self.root, text="Directorio de Descargas:", font=font_style_label, bg=bg_required, fg=fg_required).pack(pady=padding_y)
        frame_download = tk.Frame(self.root)
        frame_download.pack(pady=padding_y)
        
        self.entry_download_directory = tk.Entry(frame_download, width=entry_width, font=font_style_entry)
        self.entry_download_directory.insert(0, self.file_address.download_directory)
        self.entry_download_directory.pack(side=tk.LEFT)
        
        tk.Button(frame_download, text="📂", command=self.select_download_directory, bg="yellow", fg="black").pack(side=tk.LEFT, padx=5)

        # Selector de archivo Excel
        tk.Label(self.root, text="Directorio Archivo Excel:", font=font_style_label, bg=bg_required, fg=fg_required).pack(pady=padding_y)
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

        tk.Button(self.root, text="🖥️ Descargar Formato de Base de Datos", command=self.download_bd_pdf, font=font_style_entry, bg="purple", fg="white").pack(pady=5)


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
            # Diccionario con el nombre de los campos y sus valores
            fields = {
                "SIAT: URL": self.entry_url_siat.get().strip(),
                "SIAT: NIT": self.entry_nit.get().strip(),
                "SIAT: CUF": self.entry_cuf.get().strip(),
                "SIAT: Nro Factura": self.entry_nro_factura.get().strip(),
                "SIAT: Tipo": self.entry_tipo.get().strip(),
                "SIAT: Tiempo de descarga": self.entry_timer.get().strip(),
                "SIAT: Texto del Botón": self.entry_btn_name.get().strip(),
                "Directorio de Descargas": self.entry_download_directory.get().strip(),
                "Directorio Archivo Excel": self.entry_excel_file.get().strip()
            }

            # Verificar campos y detener si hay errores
            if not self.validator_fields(fields):
                return 
            
            excel_data_extractor = ExcelDataExtractor(self.file_address.excel_file_path, self.base_url_siat)
            pdf_invoice_downloader = PDFInvoiceDownloader(
                file_address=self.file_address,
                excel_data_extractor=excel_data_extractor,
                util_download=self.util_download
            )
            
            pdf_invoice_downloader.download_invoices()

            if self.merge_pdfs_var.get() == 1:
                self.join_all_pdfs()

            messagebox.showinfo("Éxito", "Finalizó la ejecución del Script")
        except Exception as e:
            
            error_message = f"Ocurrió un error: {str(e)}"
            pdf_invoice_downloader.driver.quit()
            traceback.print_exc()  
            messagebox.showerror("Error", error_message)


    def join_all_pdfs(self):

        # Preguntar al usuario si está seguro
        confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas unir todos los PDFs?")
        
        if not confirm:
            return  
        
        fields = {
            "Directorios de Descargas": self.entry_download_directory.get().strip()
        }

        # Verificar campos y detener si hay errores
        if not self.validator_fields(fields):
            return 
    
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


    def download_bd_pdf(self):
        try:
            # 1️⃣ - CREAR DATOS DE EJEMPLO
            data = [
                {
                    "nro": 1,
                    "nit": 1028627025,
                    "nro_factura": 195663,
                    "cuf": "4661AB1B43247CC29DF49FF5AE324D277DA4378B675D0DA04E8449E74",
                    "tipo": 2
                }
            ]

            # 2️⃣ - CREAR DATAFRAME
            df = pd.DataFrame(data)

            # 3️⃣ - SELECCIONAR RUTA PARA GUARDAR
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                    filetypes=[("Excel files", "*.xlsx")],
                                                    title="Base_de_datos")
            if not file_path:
                return  # Usuario canceló

            # 4️⃣ - EXPORTAR A EXCEL
            df.to_excel(file_path, index=False, engine='openpyxl')

            # 5️⃣ - MENSAJE DE ÉXITO
            messagebox.showinfo("Éxito", f"El archivo se guardó correctamente en:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el Excel:\n{str(e)}")


    def validator_fields(self, fields):
        # Identificar los campos vacíos
        empty_fields = [name for name, value in fields.items() if not value]

        if empty_fields:
            # Generar mensaje con los campos vacíos
            missing = "\n".join(empty_fields)
            messagebox.showwarning("Advertencia", f"Por favor, completa los siguientes campos:\n{missing}")
            return False  # Indica que hay errores

        return True  # Todos los campos están completos
    
    def info_app(self):
        description = 'Esta es una aplicación desarrollada para que el cliente (usuario de la aplicación) pueda descargar todas las facturas del SIAT de manera masiva y sencilla'
        url_info = 'Los primeros datos como ser URL, NIT, CUF, NÚMERO DE FACTURA y TIPO \n Se refiere a la composición de la URL que maneja el SIAT para poder ver las facturas'
        bd_info = 'Por lo cual esos son los mismos campos que se encuentra en el Excel que se descarga'
        btn = 'El campo TEXTO DEL BOTÓN es un campo donde se tiene que poner el texto que se tiene en dicho voton al momento de ingresar al url del SIAT'
        dir_des = 'El campo DIRECTORIO DE DESCARGAS es la carpeta donde se guardaran los PDFs descargados'
        exc_bd = 'El campo DIRECTORIO DE EXCEL es el documento excel el cual será usado como Base de Datos'
        use = 'Manual de Uso: Los'
        
        print(description)