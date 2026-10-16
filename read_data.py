import os
import numpy as np
import matplotlib.pyplot as plt

def cargar_datos_paciente(dbPath, patient):
    """Carga los datos de un paciente específico desde las carpetas correspondientes"""
    # Definir las rutas específicas de cada carpeta
    dir_labels = os.path.join(dbPath, 'labels')
    dir_abp = os.path.join(dbPath, 'abp')
    dir_ppg = os.path.join(dbPath, 'ppg')
    dir_resp = os.path.join(dbPath, 'resp')
    
    # Nombres de los ficheros para el paciente indicado
    fn_labels = f"{patient}_labels.npy"
    fn_abp = f"{patient}_abp.npy"
    fn_ppg = f"{patient}_ppg.npy"
    fn_resp = f"{patient}_resp.npy"

    datos = {}
    
    try:
        datos['labels'] = np.load(os.path.join(dir_labels, fn_labels)) # Dimensiones esperadas: (30, 2)
        datos['abp'] = np.load(os.path.join(dir_abp, fn_abp))          # Dimensiones esperadas: (30, 3750)
        datos['ppg'] = np.load(os.path.join(dir_ppg, fn_ppg))          # Dimensiones esperadas: (30, 3750)
        datos['resp'] = np.load(os.path.join(dir_resp, fn_resp))       # Dimensiones esperadas: (30, 3750)
        print(f"¡Datos del paciente {patient} cargados correctamente desde sus respectivas carpetas!")
    except FileNotFoundError as e:
        print(f"Error al cargar algún archivo para el paciente {patient}: {e}")
        return None
        
    return datos


def mostrar_presion(datos_paciente, patient, idx):
    """Muestra la Tensión Sistólica y Diastólica del segmento seleccionado"""
    labels = datos_paciente['labels']
    assert labels.shape == (30, 2), 'Las dimensiones de las etiquetas no son correctas'
    
    sbp, dbp = labels[idx, :]
    print(f'\n--- Paciente {patient} | Segmento {idx} ---')
    print(f'Presión Sistólica (SBP) = {sbp} mmHg')
    print(f'Presión Diastólica (DBP) = {dbp} mmHg')


def graficar_ondas(datos_paciente, patient, idx):
    """Grafica los primeros N segundos de cada señal separada"""
    
    ondas = {
        'ABP (Presión Arterial)': datos_paciente['abp'],
        'PPG (Pulso / Cámara)': datos_paciente['ppg'],
        'RESP (Respiración)': datos_paciente['resp']
    }
    
    fs = 125  # Frecuencia de muestreo (Hz)
    N = len(list(ondas.values())[0][idx])
    t = np.arange(N) / fs
    tidx = t < 15  # filtrar los N primeros segundos
    
    plt.figure(figsize=(10, 8))
    
    for i, (nombre_onda, matriz_onda) in enumerate(ondas.items(), 1):
        plt.subplot(len(ondas), 1, i)
        plt.plot(t[tidx], matriz_onda[idx][tidx], color='purple' if 'PPG' in nombre_onda else 'blue')
        plt.ylabel(nombre_onda)
        plt.grid(True)
        
    plt.xlabel('Tiempo (s)')
    plt.suptitle(f'Paciente: {patient} | Segmento: {idx}')
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    dbPath = 'data'
    patient = 'p093833'
    idx = 29

    paciente_actual = cargar_datos_paciente(dbPath, patient)

    if paciente_actual is not None:
        mostrar_presion(paciente_actual, patient, idx)
        graficar_ondas(paciente_actual, patient, idx)