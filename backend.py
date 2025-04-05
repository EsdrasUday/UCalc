import numpy as np
import statistics as stats
from collections import Counter
import pandas as pd
from tkinter import filedialog
import customtkinter as ctk

class sistema:
    def __init__(self):
        pass
    

    def calcular_intervalo_classes(self,dados, num_classes=None):
        min_val = min(dados)
        max_val = max(dados)

        if num_classes is None:
            num_classes = int(np.ceil(1 + 3.322 * np.log10(len(dados)))) # Sturge
        amplitude = (max_val - min_val) / num_classes 

        intervalos = []
        for i in range(num_classes):
            limite_inferior = min_val + i * amplitude
            limite_superior = limite_inferior + amplitude
            intervalos.append((round(limite_inferior, 2), round(limite_superior, 2)))

        intervalos[-1] = (intervalos[-1][0], max_val)

        return intervalos

    def exportar_para_excel(self, intervalos, fi, Fi, fri, Fri, fri_percent, Fri_percent):
        df = pd.DataFrame({
            "Intervalo": [f"{inicio} ➝ {fim}" for inicio, fim in intervalos],
            "fi": list(fi.values()),
            "Fi": list(Fi.values()),
            "fri": list(fri.values()),
            "fri %": [f"{v:.2f}%" for v in fri_percent.values()],
            "Fri": list(Fri.values()),
            "Fri %": [f"{v:.2f}%" for v in Fri_percent.values()]})
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        
        if file_path:
            df.to_excel(file_path, index=False)
            print(f"Tabela exportada para {file_path}")
        else:
            print("Exportação cancelada.")

    def calcular_estatisticas(self,dados):
        media = np.mean(dados)
        mediana = np.median(dados)
        moda = stats.mode(dados) if len(set(dados)) != len(dados) else "Sem moda"
        desvio_padrao = np.std(dados, ddof=1)
        coef_variancia = (desvio_padrao / media) * 100 if media != 0 else 0
        return media, mediana, moda, desvio_padrao, coef_variancia
   
    def calcular_frequencia(self,dados, intervalos): 
        fi = {intervalo: 0 for intervalo in intervalos}

        for valor in dados:
            for i, intervalo in enumerate(intervalos):
                if i == len(intervalos) - 1:  # Maior
                    if intervalo[0] <= valor <= intervalo[1]:  
                        fi[intervalo] += 1
                        break
                elif intervalo[0] <= valor < intervalo[1]:  # Inter. normal
                    fi[intervalo] += 1
                    break

        Fi = {}
        fri = {}
        Fri = {}
        total = len(dados)
        acumulada = 0

        for intervalo, freq in fi.items():
            acumulada += freq
            Fi[intervalo] = acumulada
            fri[intervalo] = round(freq / total, 4)
            Fri[intervalo] = round(acumulada / total, 4)

        return fi, Fi, fri, Fri


s = sistema()
