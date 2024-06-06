import pandas as pd

_url_original = "data/raw/productivity-statistics-1978-2022.csv"
_url_dataset_limpio = "data/clean/productivity-statistics-1978-2022-clean.csv"
_dataset = pd.read_csv(_url_original)

def eliminar_outlines(columnas_numericas):
    """Eliminar los valores atipicos"""
    low, high = 0.25, 0.75
    quant_col  = columnas_numericas.quantile([low, high])
    columnas_numericas = columnas_numericas.apply(lambda valor: valor[(valor > quant_col.loc[low, valor.name]) & (valor < quant_col.loc[high, valor.name])], axis=0)

def limpiar_datos(dataset):
    """Limpiar el conjunto de datos"""
    cols = dataset.columns[dataset.isnull().mean() >= 0.5]
    dataset.drop(columns=cols, inplace=True)
    dataset.dropna(axis=0, inplace=True)
    dataset.reset_index(drop=True, inplace=True)
    columnas_numericas = dataset.select_dtypes(include='number')
    for col in columnas_numericas.columns.to_list():
        mean = dataset[col].mean()
        dataset[col].fillna(mean, inplace=True)
    eliminar_outlines(columnas_numericas)
    dataset.drop(dataset[(dataset['Data_value']) <= 0].index, axis=0, inplace=True)

def dataframe_original_limpio():
    """Devuelve el conjunto de datos limpio"""
    try:
        limpiar_datos(_dataset)
        _dataset.to_csv(_url_dataset_limpio, index=False)
        print("Archivo guardado correctamente")
    except FileNotFoundError:
        print("El archivo no existe. Puede que haya sido movido o eliminado de la direccion. Verifique la direccion")
    else:
        return pd.read_csv(_url_dataset_limpio)
