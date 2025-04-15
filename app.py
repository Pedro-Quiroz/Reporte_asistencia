import tkinter as tk
from tkinter import ttk
from backend.asistencias import leer_datos_json, procesar_asistencias

tree = None

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Empresa de Servicios S.A.C.")
ventana.geometry("700x400")

# Titulo 
titulo = ttk.Label(ventana, text="Reporte de Asistencia", font=("Arial", 16))
titulo.pack(pady=10)

# Frame de fechas
frame_fechas = ttk.Frame(ventana)
frame_fechas.pack(pady=10)

# Fecha inicio
label_inicio = tk.Label(frame_fechas, text="Fecha inicio: 'año-mes-día'")
label_inicio.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entrada_inicio = tk.Entry(frame_fechas)
entrada_inicio.grid(row=0, column=1, padx=5, pady=5)

# Fecha fin
label_fin = tk.Label(frame_fechas, text="Fecha fin: 'año-mes-día'")
label_fin.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entrada_fin = tk.Entry(frame_fechas)
entrada_fin.grid(row=1, column=1, padx=5, pady=5)

#frame para resultados
frame_resultados = tk.Frame(ventana)
frame_resultados.pack(pady=10)



# Boton de reporte
def generar_reporte():
    global tree
    fecha_inicio = entrada_inicio.get()
    fecha_fin = entrada_fin.get()
    try:
        data = leer_datos_json("asistencias.json")
        df_resultado = procesar_asistencias(data, fecha_inicio, fecha_fin)

        if tree:
            tree.destroy()
        
        cantidad_filas = len(df_resultado)
        tree = ttk.Treeview(frame_resultados, columns=("Empleado", "Minutos"), show="headings", height=max(cantidad_filas,1))
        tree.heading("Empleado", text="Empleado")
        tree.heading("Minutos", text="Minutos de Tardanza")
        tree.column("Empleado", anchor="center", width=300)
        tree.column("Minutos", anchor="center", width=300)
        tree.pack()

        for _, fila in df_resultado.iterrows():
            tree.insert("", "end", values=(fila["Empleado"], fila["Minutos de Tardanza"]))
        


    except Exception as e:
        print("Ocurrió un error:", e)

boton_reporte = tk.Button(ventana, text="Generar reporte", command=generar_reporte)
boton_reporte.pack(pady=10)

ventana.mainloop()