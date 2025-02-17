import tkinter as tk
from presentation.PPrincipal import PPrincipal  

def main():
    # Crear la ventana principal
    root = tk.Tk()

    # Crear la aplicación
    app = PPrincipal(root)

    # Ejecutar la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
