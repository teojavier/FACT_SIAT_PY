import pandas as pd
from data.BaseUrlSiat import BaseUrlSiat
from data.DSiat import DSiat


class ExcelDataExtractor:
    def __init__(self, excel_file_path: str, base_url_siat: BaseUrlSiat):
        self.excel_file_path = excel_file_path
        self.base_url_siat = base_url_siat

    def extract_texts_from_excel(self):
        df = pd.read_excel(self.excel_file_path)
        d_siat_list = []

        # Iterar sobre las filas del DataFrame
        for index, row in df.iterrows():
            # Crear una instancia de DSiat para cada fila y agregarla a la lista
            d_siat = DSiat(
                base_url_siat=self.base_url_siat,
                c_nit=str(row['nit']),
                c_cuf=str(row['cuf']),
                c_nro_factura=str(row['nro_factura']),
                c_nro=str(row['nro']),
                c_t=str(row['tipo'])
            )
            d_siat_list.append(d_siat)  # Agregar la instancia a la lista

        # Devolver la lista con todas las instancias de DSiat
        return d_siat_list