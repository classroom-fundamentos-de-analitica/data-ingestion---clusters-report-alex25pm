"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd


def ingest_data():
    import re
    col_names = ['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave']

    df = pd.read_fwf(
        'clusters_report.txt', 
        names = col_names,
        widths=[8, 12, 12, 90],
        skiprows=4, 
    )

    palabras = ""
    indice = -1
    reemplazo = False
    for index, row in df.iterrows():
        if (index == 0 or not pd.isna(row['cluster'])):
            if(reemplazo == False):
                indice = index
                palabras += row['principales_palabras_clave']
                reemplazo = True
            else:
                if(palabras[len(palabras)-1] == '.'):
                    palabras = palabras[:-1]
                palabras = re.sub('\s{2,}', ' ', palabras)
                df.iloc[indice, 3] = palabras
                palabras = ""
                indice = index
                palabras += row['principales_palabras_clave']

        else:
            if(index == 50):
                if palabras[len(palabras)-1] != " ":
                    palabras += " " 
                palabras += row['principales_palabras_clave']
                if(palabras[len(palabras)-1] == '.'):
                    palabras = palabras[:-1]
                palabras = re.sub('\s{2,}', ' ', palabras)
                df.iloc[indice, 3] = palabras
                palabras = "" 
            else:   
                if palabras[len(palabras)-1] != " ":
                    palabras += " " 
                palabras += row['principales_palabras_clave']

    df.dropna(axis=0, inplace=True)
    df.reset_index(inplace=True)
    df.drop(axis=1, labels='index', inplace=True)
    df.porcentaje_de_palabras_clave = df.porcentaje_de_palabras_clave.str.strip('%')
    df.porcentaje_de_palabras_clave = df.porcentaje_de_palabras_clave.str.replace(',','.').astype(float)

    return df
