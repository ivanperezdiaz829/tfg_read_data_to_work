import os
import numpy as np
import pandas as pd

dbPath = 'data/' 

labels_dir = os.path.join(dbPath, 'labels')
archivos = os.listdir(labels_dir)
pacientes = sorted(list(set([f.split('_')[0] for f in archivos if '_labels.npy' in f])))

print(f"Se han encontrado {len(pacientes)} pacientes. Procesando y exportando...")

datos_para_csv = []

for patient in pacientes:
    try:
        # Cargar etiquetas del paciente
        labels_path = os.path.join(labels_dir, f"{patient}_labels.npy")
        labels = np.load(labels_path) # Forma: (30, 2)
        
        # Cargar también la onda ppg para extraer métricas de ella
        ppg_path = os.path.join(dbPath, 'ppg', f"{patient}_ppg.npy")
        ppg_waves = np.load(ppg_path) # Forma: (30, 3750)
        
        # Recorrer los 30 segmentos de cada paciente
        for idx in range(labels.shape[0]):
            sbp, dbp = labels[idx, :]
            segmento_ppg = ppg_waves[idx]
            amplitud_media = np.mean(segmento_ppg)
            pico_maximo = np.max(segmento_ppg)
            
            datos_para_csv.append({
                'Paciente': patient,
                'Segmento': idx,
                'SBP': sbp,
                'DBP': dbp,
                'Amplitud_Media_PPG': amplitud_media,
                'Pico_Maximo_PPG': pico_maximo
            })
    except Exception as e:
        print(f"Error procesando al paciente {patient}: {e}")

# Exportar a CSV
df = pd.DataFrame(datos_para_csv)
df.to_csv('mimic_resumen_tension.csv', index=False)
print("Archivo guardado como 'mimic_resumen_tension.csv'")
print(df.head())