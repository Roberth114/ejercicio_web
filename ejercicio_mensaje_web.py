import tkinter as tk
from tkinter import messagebox
import pywhatkit
from datetime import datetime, timedelta

def enviar_mensaje():
    cedula = entry_cedula.get().strip()
    estado = var_enfermo.get()
    numero = entry_numero.get().strip()

    if not cedula:
        messagebox.showerror("Debe ingresar su número de cédula.")
        return

    if estado == "no":
        messagebox.showinfo("Información", "Usted no está enfermo.")
        return

    if estado == "si" and not numero.startswith('+'):
        messagebox.showerror("error", "Debe ingresar un número válido con código de país (ej: +57...)")
        return

    try:
        ahora = datetime.now() + timedelta(minutes=2)
        hora = ahora.hour
        minuto = ahora.minute

        mensaje = f"Su cita médica está programada para el dia 06/06/2025. Cédula: {cedula}.\nPor favor presentarse puntualmente."

        pywhatkit.sendwhatmsg(
            numero,
            mensaje,
            hora,
            minuto,
            wait_time=30,
            tab_close=True,
            close_time=2
        )

        messagebox.showinfo("Mensaje enviado", f"Cita médica enviada a {numero} para las {hora:02d}:{minuto:02d}")

    except Exception as e:
        messagebox.showerror("Error al enviar", str(e))



root = tk.Tk()
root.title("Citas Médicas")
root.geometry("400x350")

tk.Label(root, text="Numero de Cédula").pack(pady=5)
entry_cedula = tk.Entry(root, width=30)
entry_cedula.pack()

tk.Label(root, text="¿Esta enfermo?").pack(pady=10)
var_enfermo = tk.StringVar(value="no")

frame_radio = tk.Frame(root)
frame_radio.pack()
tk.Radiobutton(frame_radio, text="Si", variable=var_enfermo, value="si").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_radio, text="No", variable=var_enfermo, value="no").pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Numero de teléfono (+57...)").pack(pady=10)
entry_numero = tk.Entry(root, width=30)
entry_numero.pack()

tk.Button(root, text="Enviar Mensaje", command=enviar_mensaje).pack(pady=20)

root.mainloop()