
import tkinter as tk
from interfaz.VentanaPrincipal import VentanaPrincipal


def main():
    ventana = tk.Tk()
    VentanaPrincipal(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
