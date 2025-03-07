import sqlite3
import hashlib
import threading
import os


class ConnectionSQLite:
    _instance = None
    _lock = threading.Lock()  # Para evitar problemas en entornos multi-hilo

    def __new__(cls):
        """Implementación del patrón Singleton"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConnectionSQLite, cls).__new__(cls)
                cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Inicializa la conexión y crea la tabla si no existe"""
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta de `ConnectionSQLite.py`
        db_path = os.path.join(base_dir, "database", "bd.sqlite3")  # Construye la ruta a la base de datos

        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Crea la tabla de usuarios si no existe"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                code INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user TEXT UNIQUE NOT NULL,
                pass TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def create_users(self, users):
        """
        Inserta múltiples usuarios en la base de datos.
        :param users: Lista de tuplas (name, user, pass)
        """
        try:
            hashed_users = [(name, user, hashlib.sha256(password.encode()).hexdigest()) for name, user, password in users]
            self.cursor.executemany("INSERT INTO users (name, user, pass) VALUES (?, ?, ?)", hashed_users)
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("❌ Error: El usuario ya existe.")

    def login(self, username, password):
        """
        Verifica si las credenciales son correctas.
        :param username: Nombre de usuario
        :param password: Contraseña
        :return: True si el usuario existe, False si no.
        """
        self.cursor.execute("SELECT * FROM users WHERE user = ? AND pass = ?", 
                            (username, hashlib.sha256(password.encode()).hexdigest()))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False


# db = ConnectionSQLite()

# # Crear usuarios
# db.create_users([
#     ("ADMINISTRADOR", "admin", "1234")
# ])

# # consulta
# python data\ConnectionSQLite.py

# Intentar iniciar sesión
# db.login("juanp", "1234")  # ✅ Correcto
# db.login("ana.l", "incorrecto")  # ❌ Incorrecto