import tkinter as tk
# from presentation.PPrincipal import PPrincipal  
from presentation.PLogin import PLogin  


def main():
    # Crear la ventana principal
    root = tk.Tk()

    # Crear la aplicación
    # app = PPrincipal(root)
    app = PLogin(root)

    # Ejecutar la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
