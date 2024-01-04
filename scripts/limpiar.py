import pandas as pd

_url_original = "data/raw/productivity-statistics-1978-2022.csv"
_url_dataset_limpio = "data/clean/productivity-statistics-1978-2022-clean.csv"
_dataset = pd.read_csv(_url_original)

def __eliminar_outlines(columnas_numericas):
    """Eliminar los valores atipicos"""
    low, high = 0.25, 0.75
    quant_col  = columnas_numericas.quantile([low, high])
    columnas_numericas = columnas_numericas.apply(lambda valor: valor[(valor > quant_col.loc[low, valor.name]) & (valor < quant_col.loc[high, valor.name])], axis=0)

def __limpiar_datos(dataset):
    """Limpiar el conjunto de datos"""
    mitad = dataset.count().max() // 2
    dataset.dropna(axis=1, thresh=mitad, inplace=True)
    dataset.dropna(axis=0, inplace=True)
    columnas_numericas = dataset.select_dtypes(include='number')
    for col in columnas_numericas.columns.to_list():
        mean = dataset[col].mean()
        dataset[col].fillna(mean, inplace=True)
    __eliminar_outlines(columnas_numericas)

def dataframe_original_limpio():
    """Devuelve el conjunto de datos limpio"""
    try:
        __limpiar_datos(_dataset)
        _dataset.to_csv(_url_dataset_limpio, index=False)
        print("Archivo guardado correctamente")
    except FileNotFoundError:
        print("El archivo no existe. Puede que haya sido movido o eliminado de la direccion. Verifique la direccion")
    else:
        return pd.read_csv(_url_dataset_limpio)
