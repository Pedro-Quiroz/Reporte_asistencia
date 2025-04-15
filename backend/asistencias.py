import json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


with open('asistencias.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def calcular_tardanza(hora_real, hora_referencia):
    if hora_real:
        entrada = datetime.strptime(hora_real, "%H:%M")
        referencia = datetime.strptime(hora_referencia, "%H:%M")
        tardanza = max(0, int((entrada - referencia).total_seconds() / 60))
        return tardanza
    return 0


fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")


tardanzas = {}

for registro in data:
    fecha_registro = datetime.strptime(registro["fecha"], "%Y-%m-%d")
    if fecha_inicio <= fecha_registro <= fecha_fin:
        nombre = registro["nombre"]
        dia_semana = fecha_registro.weekday()  # 0 = lunes, ..., 5 = sábado

        # Hora de referencia por día
        hora_ref_mañana = "09:00" if dia_semana == 5 else "08:00"
        hora_ref_tarde = "15:00"

        # Calcular tardanza
        tardanza_mañana = calcular_tardanza(registro["hora_ingreso_1"], hora_ref_mañana)

        # Solo calcular tarde si no es sábado
        if dia_semana < 5:
            tardanza_tarde = calcular_tardanza(registro["hora_ingreso_2"], hora_ref_tarde)
        else:
            tardanza_tarde = 0

        total = tardanza_mañana + tardanza_tarde

        if nombre not in tardanzas:
            tardanzas[nombre] = 0
        tardanzas[nombre] += total

df = pd.DataFrame(list(tardanzas.items()), columns=["Empleado", "Minutos de Tardanza"])
print("\nReporte de Tardanzas:\n")
print(df)

