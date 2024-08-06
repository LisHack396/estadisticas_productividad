import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.limpiar import dataframe_original_limpio

warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

dataset = dataframe_original_limpio()


def graficar():
    """Graficar las estadisticas de productividad"""
    font = "Century Gothic"
    values_pie = dataset['units'].value_counts()
    labels_pie = values_pie.index
    fig = plt.figure('Estadísticas de productividad', figsize=(12, 8))
    axes = fig.subplots(nrows=2, ncols=2)
    fig.suptitle("Estadísticas de productividad 1978-2022", fontsize=20, fontweight='bold', fontname=font)
    axes[0, 0].set(title="Valores de datos por periodo", xlim=(0, 2000))
    axes[0, 1].set(title="Distribución de los valores de datos", xlim=(0, 3000))
    axes[1, 0].set(title="Cantidad de trabajos por unidades", ylim=(0, 250))
    axes[1, 1].set(title="Porcentaje de la producción por unidades")
    
    sns.lineplot(data=dataset, x='data_value', y='period', ax=axes[0, 0])
    sns.kdeplot(dataset['data_value'], fill=True, color='blue', ax=axes[0, 1])
    sns.rugplot(dataset['data_value'], color='blue', ax=axes[0, 1])
    sns.countplot(data=dataset, x='units', ax=axes[1, 0])
    
    axes[1, 1].pie(x=values_pie, labels=labels_pie, autopct='%.2f', shadow=True)
    
    fig.tight_layout()
    plt.show()