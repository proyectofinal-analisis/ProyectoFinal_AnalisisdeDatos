from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

# Leer el archivo CSV
df = pd.read_csv('Employment__Unemployment__and_Labor_Force_Data.csv')

# Asegurarse de que las columnas estén en el formato correcto
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# Inicializar la app Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Lista de métodos de imputación
methods = ["Original", "Quitando los NANS", "Llenado con 0’s", "Interpolación Polinómica de grado 2"]

# Lista de tipos de gráficos
chart_types = ["Línea", "Barra", "Burbuja", "Área", "Histograma", "Caja"]

# Lista de tipos de gráficos predeterminados para cada gráfico
default_chart_types = ["Línea", "Barra", "Burbuja", "Área"]

def apply_imputation(method, data):
    if method == "Quitando los NANS":
        return data.dropna()
    elif method == "Llenado con 0’s":
        return data.fillna(0)
    elif method == "Interpolación Polinómica de grado 2":
        return data.interpolate(method='polynomial', order=2)
    else:
        return data

def create_figure(chart_type, df, method):
    df['Unemployment Rate'] = apply_imputation(method, df['Unemployment Rate'])
    if chart_type == "Línea":
        fig = px.line(df, x='Year', y='Unemployment Rate', title=f'Unemployment Rate Over Time ({method} - {chart_type})')
    elif chart_type == "Barra":
        fig = px.bar(df, x='Year', y='Unemployment Rate', title=f'Unemployment Rate Over Time ({method} - {chart_type})')
    elif chart_type == "Burbuja":
        fig = px.scatter(df, x='Year', y='Unemployment Rate', size='Unemployment Rate', title=f'Unemployment Rate Over Time ({method} - {chart_type})')
    elif chart_type == "Área":
        fig = px.area(df, x='Year', y='Unemployment Rate', title=f'Unemployment Rate Over Time ({method} - {chart_type})')
    elif chart_type == "Histograma":
        fig = px.histogram(df, x='Unemployment Rate', nbins=20, title=f'Unemployment Rate Histogram ({method} - {chart_type})')
    elif chart_type == "Caja":
        fig = px.box(df, x='Year', y='Unemployment Rate', title=f'Unemployment Rate Box Plot ({method} - {chart_type})')
    return fig

def generate_graph_controls(graph_id, visible=True):
    display_style = {'display': 'block'} if visible else {'display': 'none'}
    return dbc.Col([
        dbc.Card(
            dbc.CardBody([
                html.H5(f'Gráfico {graph_id}: {methods[graph_id-1]}', className='graph-title'),
                html.Label(f'Tipo de gráfico:', className='label'),
                dcc.Dropdown(
                    id=f'chart-dropdown-{graph_id}',
                    options=[{'label': chart_type, 'value': chart_type} for chart_type in chart_types],
                    value=default_chart_types[graph_id-1],  # Asignar un tipo de gráfico predeterminado
                    className='dropdown'
                ),
                html.Label(f'Rango de fechas:', className='label'),
                dcc.DatePickerRange(
                    id=f'date-picker-range-{graph_id}',
                    min_date_allowed=df['Year'].min().date(),
                    max_date_allowed=df['Year'].max().date(),
                    start_date=df['Year'].min().date(),
                    end_date=df['Year'].max().date(),
                    display_format='YYYY-MM-DD',
                    className='date-input'
                ),
                dcc.Graph(id=f'graph-{graph_id}', className='graph')
            ])
        )
    ], width=6, className='mb-4', style=display_style)

# Definir el layout de la app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Employment and Unemployment Data Dashboard', className='header-title'), width=12)
    ]),
    dbc.Row(id='graph-row', children=[
        generate_graph_controls(1),
        generate_graph_controls(2),
        generate_graph_controls(3, visible=False),
        generate_graph_controls(4, visible=False)
    ]),
    dbc.Row([
        dbc.Col(html.Button('Mostrar Gráficas 1 y 2', id='show-set-1', className='update-button', n_clicks=1), width=6),
        dbc.Col(html.Button('Mostrar Gráficas 3 y 4', id='show-set-2', className='update-button', n_clicks=0), width=6),
    ]),
    dbc.Row([
        dbc.Col(html.Button('Actualizar Gráfica', id='update-button-all', className='update-button', n_clicks=0), width=12)
    ]),
    html.Div('© 2024 My Dashboard', className='footer')
], fluid=True)

# Definir las callbacks para actualizar los gráficos
@app.callback(
    [Output(f'graph-{i}', 'figure') for i in range(1, 5)],
    [Input('update-button-all', 'n_clicks')],
    [State(f'chart-dropdown-{i}', 'value') for i in range(1, 5)] +
    [State(f'date-picker-range-{i}', 'start_date') for i in range(1, 5)] +
    [State(f'date-picker-range-{i}', 'end_date') for i in range(1, 5)]
)
def update_all_graphs(n_clicks, *args):
    figs = []
    for i in range(4):
        chart_type = args[i]
        start_date = args[4 + i]
        end_date = args[8 + i]
        df_copy = df.copy()
        df_copy = df_copy[(df_copy['Year'] >= start_date) & (df_copy['Year'] <= end_date)]
        fig = create_figure(chart_type, df_copy, methods[i])
        figs.append(fig)
    return figs

@app.callback(
    [Output('graph-row', 'children')],
    [Input('show-set-1', 'n_clicks'),
     Input('show-set-2', 'n_clicks')]
)
def switch_graphs(n1, n2):
    if n1 > n2:
        return [[
            generate_graph_controls(1, visible=True),
            generate_graph_controls(2, visible=True),
            generate_graph_controls(3, visible=False),
            generate_graph_controls(4, visible=False)
        ]]
    else:
        return [[
            generate_graph_controls(1, visible=False),
            generate_graph_controls(2, visible=False),
            generate_graph_controls(3, visible=True),
            generate_graph_controls(4, visible=True)
        ]]

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)
