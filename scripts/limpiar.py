import pandas as pd

_url_original = "data/raw/productivity-statistics-1978-2022.csv"
_url_dataset_limpio = "data/clean/productivity-statistics-1978-2022-clean.csv"
_dataset = pd.read_csv(_url_original)

def eliminar_outliers(dataset):
    """Eliminar los valores atipicos"""
    for columna in dataset.select_dtypes(include='number').columns:
        Q1 = dataset[columna].quantile(0.25)
        Q3 = dataset[columna].quantile(0.75)
        IQR = Q3 - Q1
        outlier_mask = (dataset[columna] < (Q1 - 1.5 * IQR)) | (dataset[columna] > (Q3 + 1.5 * IQR))
        return dataset[~outlier_mask]

def limpiar_datos(dataset):
    """Limpiar el conjunto de datos"""
    dataset.columns = dataset.columns.str.lower()
    dataset.drop_duplicates(subset=['series_reference'], keep="first", inplace=True)
    cols = dataset.columns[dataset.isnull().mean() >= 0.5]
    dataset.drop(columns=cols, inplace=True)
    dataset.dropna(axis=0, inplace=True)
    dataset.drop(dataset[(dataset['data_value']) < 0].index, axis=0, inplace=True)
    dataset = eliminar_outliers(dataset)
    dataset.reset_index(drop=True, inplace=True)
    columnas_numericas = dataset.select_dtypes(include='number')
    for col in columnas_numericas.columns.to_list():
        mean = dataset[col].mean()
        dataset[col].fillna(mean, inplace=True)

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
