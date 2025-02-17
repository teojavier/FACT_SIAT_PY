import os
import time
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


class PDFInvoiceDownloader:
    def __init__(self, file_address: FileAddress, excel_data_extractor: ExcelDataExtractor, util_download: UtilDownload):
        self.file_address = file_address
        self.excel_data_extractor = excel_data_extractor
        self.util_download = util_download

    def wait_for_download(self, download_dir):
        # Esperar hasta que no haya archivos .crdownload, que son archivos temporales mientras se descarga
        while any([filename.endswith(".crdownload") for filename in os.listdir(download_dir)]):
            time.sleep(1)  # Espera 1 segundo entre comprobaciones

    def download_invoices(self):
        # Directorio de descargas
        download_dir = os.path.abspath(self.file_address.download_directory)

        # Si no existe el directorio, lo crea
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_dir,  # Directorio de descarga
            "download.prompt_for_download": False,        # No mostrar el prompt
            "download.directory_upgrade": True,           # Habilitar la actualización del directorio
            "safebrowsing.enabled": True                  # Habilitar navegación segura
        })
        chrome_options.add_argument("--disable-popup-blocking")

        # Configurar WebDriver
        service = Service(os.path.abspath("chrome_driver/chromedriver.exe"))
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Obtener los objetos desde Excel
        d_siat_objects = self.excel_data_extractor.extract_texts_from_excel()

        for d_siat in d_siat_objects:
            # Generar la URL para cada factura
            url_siat = d_siat.generate_url()
            driver.get(url_siat)

            try:
                # Esperar a que el botón "Ver Factura" sea clickeable
                boton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Ver Factura']]"))
                )
                boton.click()

                # Esperar unos segundos para que la descarga inicie
                time.sleep(self.util_download.seconds_download)

                # Si se abre una nueva pestaña, cambiar a ella
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[-1])

                # Esperar hasta que el archivo se descargue completamente
                self.wait_for_download(download_dir)

            except Exception as e:
                print(f"⚠️ No se pudo procesar la factura {d_siat.c_nro_factura}: {e}")
                continue  # Continúa con la siguiente factura

        driver.quit()
