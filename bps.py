# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io 

n_enero = r"C:\Users\Gregorio Morena\Desktop\Nominas\N_1_7301273_202001.txt"
n_febrero = r"C:\Users\Gregorio Morena\Desktop\Nominas\N_1_7301273_202002.txt"
n_marzo = r"C:\Users\Gregorio Morena\Desktop\Nominas\N_1_7301273_202003.txt"

nominas = [n_enero, n_febrero, n_marzo]

def f_bps(path, delimiter='|'):
    
    datos = ''
    max_cols = 0
    
    with open (path, 'r') as file:
        for line in file:
            datos += line
            col_count = line.count(delimiter)
            if col_count > max_cols:
                max_cols = col_count
    
    encabezado = delimiter * max_cols + '\n'
    
    return io.StringIO(encabezado + datos)

importacion = pd.DataFrame()
for i in nominas:    
    importacion = pd.concat([importacion, pd.read_csv(f_bps(i), delimiter='|')], ignore_index=True)


tabla_bruta= pd.DataFrame()

registro = importacion.iloc[:,0].tolist()

mes = []

for num in range(len(registro)):
    if registro[num] == 4:
        mes = mes + [importacion.iloc[num,1]]
    else:
        mes = mes + [np.nan]

tabla_bruta['mes'] = mes
tabla_bruta['mes'] = tabla_bruta['mes'].fillna(method='ffill')

tabla_bruta['tipo_registro'] = importacion.iloc[:,0]
tabla_bruta['documento'] = importacion.iloc[:,4]
tabla_bruta['concepto'] = importacion.iloc[:,6]
tabla_bruta['importe'] = importacion.iloc[:,7]

tabla_bruta['dt'] = importacion.iloc[:,15]
tabla_bruta['dt'] = tabla_bruta['dt'].fillna(method='ffill')


tabla_final = tabla_bruta[tabla_bruta['tipo_registro'] == 7][['mes', 'documento', 'dt', 'concepto', 'importe']]
tabla_final = tabla_final.astype({'importe': float,
                                  'dt': int})

print(importacion[importacion.iloc[:,0] == 4].iloc[:,3])
print(pd.pivot_table(tabla_final, values='importe', index=['mes'], aggfunc=np.sum))