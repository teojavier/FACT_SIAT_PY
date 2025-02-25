import tkinter as tk
from tkinter import messagebox


from data.ConnectionSQLite import ConnectionSQLite
from presentation.PPrincipal import PPrincipal  



class PLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        self.root.config(bg="#f4f4f4")

        # Título
        lbl_title = tk.Label(self.root, text="Login", font=("Arial", 16, "bold"), bg="#f4f4f4", fg="#333")
        lbl_title.pack(pady=10)

        # Usuario
        lbl_user = tk.Label(self.root, text="Usuario:", font=("Arial", 12), bg="#f4f4f4")
        lbl_user.pack()
        self.entry_user = tk.Entry(self.root, font=("Arial", 12))
        self.entry_user.pack(pady=5)

        # Contraseña
        lbl_pass = tk.Label(self.root, text="Contraseña:", font=("Arial", 12), bg="#f4f4f4")
        lbl_pass.pack()
        self.entry_pass = tk.Entry(self.root, font=("Arial", 12), show="*")
        self.entry_pass.pack(pady=5)

        # Botón de login
        btn_login = tk.Button(self.root, text="Iniciar Sesión", font=("Arial", 12, "bold"), bg="#007BFF", fg="white",
                              command=self.validate_login)
        btn_login.pack(pady=15)
    
    def open_main_window(self):
        """Abre la ventana principal de la aplicación"""
        root = tk.Tk()
        PPrincipal(root)  # Inicializa la ventana principal
        root.mainloop()

    def validate_login(self):
        """Valida las credenciales ingresadas con la base de datos"""
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        db = ConnectionSQLite()
        if db.login(username, password):
            self.root.destroy()  
            self.open_main_window()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
