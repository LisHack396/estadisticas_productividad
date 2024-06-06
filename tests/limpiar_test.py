import unittest
import pandas as pd

def eliminar_outlines(df):
    columnas_numericas = df.select_dtypes(include='number')
    low, high = 0.25, 0.75
    quant_col  = columnas_numericas.quantile([low, high])
    columnas_numericas = columnas_numericas.apply(lambda valor: valor[(valor > quant_col.loc[low, valor.name]) & (valor < quant_col.loc[high, valor.name])], axis=0)
    return columnas_numericas

def limpiar_datos(df):
    cols = df.columns[df.isnull().mean() >= 0.5]
    df.drop(columns=cols, inplace=True)
    df.dropna(axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    columnas_numericas = df.select_dtypes(include='number')
    for col in columnas_numericas.columns.to_list():
        mean = df[col].mean()
        df[col].fillna(mean, inplace=True)
    return df

class EliminarOutlinesTest(unittest.TestCase):
    def setUp(self):
        print("Preparando contexto")
        self.data = {
            "A": ["A", "B", "C", "D", "E", "F"], 
            "B": [25.19, 34.98, 22.00, 78.45, 38.88, 9.11],
            "C": [33.00, 10.67, 34.52, 1.78, 98.22, 4.50]
        }
    
    def test(self):
        print("Ejecutando pruebas de eliminación de outlines")
        df = pd.DataFrame(self.data)
        cols_num = df.select_dtypes(include="number")
        cols_num = eliminar_outlines(df)
        result = pd.DataFrame({"B": [25.19, 34.98], "C": [33.00, 10.67]})
        pd.testing.assert_frame_equal(cols_num, result)
    
    def tearDown(self):
        print("Deconstruyendo contexto")
        del self.data

class LimpiarDatosTest(unittest.TestCase):
    def setUp(self):
        print("Preparando el contexto")
        self.data = {
            "A": [None, "B", None, None, "E", "F"],
            "B": [34.56, None, 44.66, 12.98, None, 2.77],
            "C": ["A", "B", None, "D", "E", "F"]
        }
    
    def test(self):
        print("Ejecutando pruebas de limpieza de datos")
        df = pd.DataFrame(self.data)
        df = limpiar_datos(df)
        result = pd.DataFrame({"B": [34.5600, 12.9800, 2.7700], "C": ["A", "D", "F"]})
        pd.testing.assert_frame_equal(df, result)
    
    def tearDown(self):
        print("Deconstruyendo el contexto")
        del self.data