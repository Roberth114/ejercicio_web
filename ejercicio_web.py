import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from tkinter import *
from tkinter import ttk, messagebox
import threading

productos_extraidos = []

# ---------- FUNCIÓN PRINCIPAL ----------
def extraer_productos_exito():
    boton.config(state=DISABLED)
    etiqueta_status.config(text="Extrayendo productos, espera...")

    def scraping():
        global productos_extraidos
        productos_extraidos = []
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-gpu")
            # chrome_options.add_argument("--headless")

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            # Recorremos múltiples páginas
            pagina = 0
            max_paginas = 5  # Puedes cambiarlo según la cantidad de páginas que desees
            while pagina < max_paginas:
                url = f"https://www.exito.com/coleccion/7830?productClusterIds=7830&facets=productClusterIds&sort=orders_desc&page={pagina}"
                driver.get(url)

                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "vtex-product-summary-2-x-container"))
                )

                html = driver.page_source
                soup = bs(html, "html.parser")

                cards = soup.find_all("article", class_="vtex-product-summary-2-x-container")
                if not cards:
                    break  # No hay más productos

                for card in cards:
                    nombre_tag = card.find("span", class_="vtex-product-summary-2-x-productBrand")
                    nombre = nombre_tag.text.strip() if nombre_tag else "Sin nombre"

                    precio_tag = card.find("span", class_="vtex-product-price-1-x-sellingPriceValue")
                    precio = precio_tag.text.strip() if precio_tag else "No disponible"

                    productos_extraidos.append((nombre, precio))

                pagina += 1

            driver.quit()
            mostrar_tabla(productos_extraidos)
            etiqueta_status.config(text=f"{len(productos_extraidos)} productos extraídos.")
        except Exception as e:
            etiqueta_status.config(text=f"Error: {str(e)}")
        finally:
            boton.config(state=NORMAL)

    threading.Thread(target=scraping).start()

def mostrar_tabla(productos):
    for fila in tree.get_children():
        tree.delete(fila)
    for i, (nombre, precio) in enumerate(productos):
        tree.insert("", "end", values=(i + 1, nombre, precio))

def exportar_excel():
    if not productos_extraidos:
        messagebox.showwarning("Exportación", "Primero debes extraer los productos.")
        return

    df = pd.DataFrame(productos_extraidos, columns=["Producto", "Precio"])
    archivo = "productos_exito.xlsx"
    df.to_excel(archivo, index=False)
    messagebox.showinfo("Exportación Exitosa", f"Productos exportados a '{archivo}'.")

# ---------- INTERFAZ GRÁFICA ----------
ventana = Tk()
ventana.title("📦 Productos Éxito - Colección Colchones")
ventana.geometry("780x500")
ventana.configure(bg="#f7f9fc")

titulo = Label(ventana, text="🛒 Productos de la Colección Éxito", font=("Arial", 16, "bold"),
               bg="#f7f9fc", fg="#2c3e50")
titulo.pack(pady=10)

frame_botones = Frame(ventana, bg="#f7f9fc")
frame_botones.pack()

boton = Button(frame_botones, text="Extraer Productos", font=("Arial", 12), command=extraer_productos_exito,
               bg="#28a745", fg="white", padx=10, pady=5)
boton.grid(row=0, column=0, padx=10)

boton_exportar = Button(frame_botones, text="Exportar a Excel", font=("Arial", 12), command=exportar_excel,
                        bg="#007bff", fg="white", padx=10, pady=5)
boton_exportar.grid(row=0, column=1, padx=10)

etiqueta_status = Label(ventana, text="", font=("Arial", 10), bg="#f7f9fc", fg="#555")
etiqueta_status.pack(pady=5)

frame_tabla = Frame(ventana)
frame_tabla.pack(padx=10, pady=10, fill=BOTH, expand=True)

tree = ttk.Treeview(frame_tabla, columns=("N°", "Producto", "Precio"), show="headings")
tree.heading("N°", text="N°")
tree.heading("Producto", text="Producto")
tree.heading("Precio", text="Precio")
tree.column("N°", width=40, anchor="center")
tree.column("Producto", width=480)
tree.column("Precio", width=120)

scroll = ttk.Scrollbar(frame_tabla, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scroll.set)

tree.pack(side=LEFT, fill=BOTH, expand=True)
scroll.pack(side=RIGHT, fill=Y)

ventana.mainloop()