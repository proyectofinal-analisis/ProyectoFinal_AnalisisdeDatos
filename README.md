# README

## Descripción del Proyecto

Esta es una aplicación web interactiva construida con Dash para visualizar datos de empleo, desempleo. La aplicación permite seleccionar diferentes métodos de imputación de datos y tipos de gráficos para visualizar la tasa de desempleo a lo largo del tiempo.

## Dependencias

Las dependencias necesarias para ejecutar esta aplicación están listadas en el archivo `requirements.txt`. Incluyen:

 - Dash
 - Dash Bootstrap Components
 - Pandas
 - Plotly

## Instalación

Para instalar las dependencias necesarias, ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

## Uso

1. Coloque el archivo de datos `Employment__Unemployment__and_Labor_Force_Data.csv` en el mismo directorio que `appdash.py`.
2. Ejecute la aplicación con el siguiente comando:

```bash
python appdash.py
```

3. Abra su navegador web y navegue a `http://127.0.0.1:8050` para interactuar con la aplicación.

## Funcionalidades

- Métodos de Imputación: Seleccione entre los siguientes métodos para manejar datos faltantes:
  - Original
  - Quitando los NANS
  - Llenado con 0’s
  - Interpolación Polinómica de grado 2

- Tipos de Gráficos: Visualice los datos utilizando los siguientes tipos de gráficos:
  - Línea
  - Barra
  - Burbuja
  - Área
  - Histograma
  - Caja
    
## Link oficial de la pagina: http://proyectofinalanalisis.pythonanywhere.com/


## Contacto

Para más información, contacte a: luis.joseph@utp.ac.pa, gerson.victoria@utp.ac.pa, sebastian.espinosa@utp.ac.pa, fernando.hilberth@utp.ac.pa.
