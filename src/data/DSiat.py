from data.BaseUrlSiat import BaseUrlSiat

class DSiat:
    def __init__(self, base_url_siat: BaseUrlSiat, c_nro: str, c_nit: str, c_cuf: str, c_nro_factura: str, c_t: str):
        self.base_url_siat = base_url_siat
        self.c_nro = c_nro
        self.c_nit = c_nit
        self.c_cuf = c_cuf
        self.c_nro_factura = c_nro_factura
        self.c_t = c_t

    def generate_url(self) -> str:
        cadena = self.base_url_siat.url_siat + self.base_url_siat.nit + self.c_nit + self.base_url_siat.cuf + self.c_cuf + self.base_url_siat.nro_factura + self.c_nro_factura + self.base_url_siat.tipo + self.c_t
        return cadena
