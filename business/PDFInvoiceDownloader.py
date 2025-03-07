import os
import time
import tkinter as tk
import glob

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.FileAddress import FileAddress
from business.ExcelDataExtractor import ExcelDataExtractor
from data.UtilDownload import UtilDownload
from tkinter import messagebox

class PDFInvoiceDownloader:
    def __init__(self, file_address: FileAddress, excel_data_extractor: ExcelDataExtractor, util_download: UtilDownload):
        self.file_address = file_address
        self.excel_data_extractor = excel_data_extractor
        self.util_download = util_download
        self.driver = self._initialize_driver()  # Inicializa el WebDriver una sola vez

    def _initialize_driver(self):
        """Configura e inicializa un único WebDriver para evitar consumo excesivo de recursos."""
        download_dir = os.path.abspath(self.file_address.download_directory)

        # Si el directorio no existe, lo crea
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_dir,  
            "download.prompt_for_download": False,        
            "download.directory_upgrade": True,           
            "safebrowsing.enabled": True                  
        })
        chrome_options.add_argument("--disable-popup-blocking")

        # Configurar WebDriver
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cd_path = os.path.join(base_dir, "chrome_driver", "chromedriver.exe")
        service = Service(os.path.abspath(cd_path))
        driver = webdriver.Chrome(service=service, options=chrome_options)

        return driver

    def wait_for_download(self, download_dir):
        """Espera hasta que los archivos .crdownload desaparezcan del directorio de descargas."""
        while any(filename.endswith(".crdownload") for filename in os.listdir(download_dir)):
            time.sleep(1)

    def download_invoices(self):
        download_dir = os.path.abspath(self.file_address.download_directory)

        # Obtener los objetos desde Excel
        d_siat_objects = self.excel_data_extractor.extract_texts_from_excel()

        errores = []  # Lista para almacenar los errores

        for d_siat in d_siat_objects:
            url_siat = d_siat.generate_url()
            self.driver.get(url_siat)

            try:
                # Esperar a que el botón "Ver Factura" sea clickeable
                boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[span[text()='{self.util_download.btn_name}']]"))
                )
                boton.click()

                # Esperar unos segundos para que la descarga inicie
                time.sleep(self.util_download.seconds_download)

                # Si se abre una nueva pestaña, cambiar a ella
                if len(self.driver.window_handles) > 1:
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                # Esperar hasta que el archivo se descargue completamente
                self.wait_for_download(download_dir)

                # Renombrar el archivo descargado
                downloaded_file = self.get_latest_file(download_dir)
                if downloaded_file:
                    new_file_name = f"Factura {d_siat.c_nro}.pdf"  # Nombre con el número de factura
                    new_file_path = os.path.join(download_dir, new_file_name)
                    os.rename(downloaded_file, new_file_path)
                else:
                    errores.append(f"⚠️ No se encontró el archivo de factura {d_siat.c_nro}")

            except Exception as e:
                error_msg = f"⚠️ Error en factura {d_siat.c_nro}"
                errores.append(error_msg)  # Guardamos el error en la lista

        # Cerrar el WebDriver al finalizar
        self.driver.quit()

        # Si hubo errores, mostrar una ventana con todos ellos
        if errores:
            root = tk.Tk()
            root.withdraw() 
            messagebox.showerror("Errores en descarga", "\n".join(errores))
    
    def get_latest_file(self, folder_path):
        """Obtiene el último archivo PDF descargado en la carpeta de descargas."""
        files = glob.glob(os.path.join(folder_path, "*.pdf"))  # Buscar archivos PDF
        if not files:
            return None
        return max(files, key=os.path.getctime)  # Obtener el archivo más reciente
