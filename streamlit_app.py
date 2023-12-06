import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import plotly.io as pio
pio.templates.default = "seaborn"
df = pd.read_csv('/content/heart_2022_no_nans.csv')
df_base = df[df.columns[9:26]]
df_base.loc[df_base['SmokerStatus'].str.contains('Never', na=False), 'SmokerStatus'] = 'No'
df_base.loc[df_base['SmokerStatus'].str.contains('Current', na=False), 'SmokerStatus'] = 'Yes'
df_base.loc[df_base['SmokerStatus'].str.contains('Former', na=False), 'SmokerStatus'] = 'Yes'
df_base.loc[df_base['HadDiabetes'].str.contains('No', na=False), 'HadDiabetes'] = 'No'
df_base.loc[df_base['HadDiabetes'].str.contains('Yes', na=False), 'HadDiabetes'] = 'Yes'
def Busca_top(dataframe):
    # Crear un nuevo DataFrame vacío para almacenar los resultados
    result_df = pd.DataFrame()

    # Iterar sobre cada columna del DataFrame original
    for column in dataframe.columns:
        # Aplicar value_counts a la columna y guardar los resultados en una Serie
        value_counts_series = dataframe[column].value_counts()

        # Agregar la Serie de value_counts al nuevo DataFrame con el nombre de la columna original
        result_df[column] = value_counts_series
    result_df = result_df.transpose()
    return result_df

def busca_filas(dataframe, row_names):
    # Obtener las filas correspondientes a los nombres dados
    selected_rows = dataframe.loc[row_names]

    # Crear un nuevo DataFrame con las filas seleccionadas
    new_dataframe = pd.DataFrame(selected_rows)

    return new_dataframe

df = pd.read_csv('/content/heart_2022_no_nans.csv')
dfn = df[df['HadHeartAttack']=='Yes']
lista = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 33]
dfo = df.iloc[:,lista]
lista2 = dfo.columns
st.set_page_config(
    page_title="Heart Disease Dashboard",
    page_icon="🫀",
    layout="wide",
)
col11, col2, col3 = st.columns(3)
with col2:
  st.image('https://st4.depositphotos.com/1070466/20313/v/450/depositphotos_203138006-stock-illustration-human-heart-anatomically-correct-hand.jpg',
  caption='Placeholder Image', width=140, use_column_width=True)

st.markdown("<h1 style='text-align: center;'>Heart Disease Dashboard</h1>", unsafe_allow_html=True)


selected3 = option_menu(None, ["Mapa","General", "Especifico"],
    icons=['Activity', 'Activity'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "white", "font-size": "22pxpx"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#white"},
        "nav-link-selected": {"background-color": "#D1352B"},
    })

st.markdown("<h1 style='text-align: center;'>Analisis de la Base de Datos</h1>", unsafe_allow_html=True)

Diseases = df.columns[9:25]

if selected3 == "Mapa":

    st.title('Visualizacion del numero de encuestados por estado')
    import geopandas as gpd
    import matplotlib.pyplot as plt
    dfn = df.groupby('State', as_index=False).size()
    estados = df['State'].value_counts().index
    states = gpd.read_file('/content/gz_2010_us_040_00_20m.json')
    dfs = states[states['NAME'].isin(estados)]
    dfs['count'] = dfn['size']
    fig, ax = plt.subplots(figsize=(15, 12))
    dfs.plot(ax=ax, cmap='OrRd',column='count', alpha=0.7, legend=True, legend_kwds={'label': "Encuestados por Ubicación", 'orientation': "horizontal"},  )
    st.pyplot(fig,use_container_width=True)

if selected3 == "General":
  selected = option_menu(None, ["Poblacion Total", "Poblacion con E.C"],
    icons=['heart', 'heart-pulse'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "white", "font-size": "22pxpx"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#white"},
        "nav-link-selected": {"background-color": "#D1352B"},
    })


  if selected =="Poblacion Total":
    from plotly import graph_objects as go
    tamano_font_title = 30
    title_font_family = 'Droid Serif'
    font_size = 15
    distribucion_sexo, grupo_edades = st.columns(2)

    with distribucion_sexo:
      fig = px.pie(df, names=df['Sex'].value_counts().index, values=df['Sex'].value_counts(), title='Distribucion de sexo en la base', color_discrete_sequence=px.colors.qualitative.Set1)
      fig.update_layout(title_font_size=30, title_font_family='Open Sans', title_font_color='black', legend_borderwidth=8, legend_bordercolor='white', legend_font_size=15,
                  legend_x=0.7,title_xref='container', title_y=0.95, font_size=font_size)
      st.plotly_chart(fig)

    with grupo_edades:
      grupo = df.groupby('AgeCategory', as_index=False)['Sex'].value_counts()
      grupo_m = grupo[grupo['Sex']=='Male']
      grupo_f = grupo[grupo['Sex']=='Female']
      x_m = grupo_m['count']
      text_f = grupo_f['count']
      x_f = grupo_f['count']*-1
      y_age = grupo_f['AgeCategory']
      fig = go.Figure()
      fig.add_trace(go.Bar( y=y_age, x=x_m,
                          name='Hombres',
                          orientation = 'h', text=x_m))
      fig.add_trace(go.Bar(y = y_age, x = x_f,
                          name = 'Mujeres', orientation = 'h', marker_color='rgb(228,26,28)',text=text_f) )
      fig.update_layout(title = 'Piramide Poblacional',
                      title_font_size = 22, barmode = 'relative',
                      bargap = 0.0, bargroupgap = 0,
                      xaxis = dict(tickvals = [-15000, -10000, -5000,
                                                0, 5000, 10000, 15000],

                                    ticktext = ['15k', '10k', '5k', '0',
                                                '5k', '10k', '15k'],

                                    title = 'Poblacion',
                                    title_font_size = 18))
      st.plotly_chart(fig)

    distribucion_etnias, top_enfermedades = st.columns(2)

    with distribucion_etnias:
      fig = px.pie(df, names=df['RaceEthnicityCategory'].value_counts().index, values=df['RaceEthnicityCategory'].value_counts(), title= 'Etnias que conforman la base por Porcentaje', color_discrete_sequence=px.colors.qualitative.Set1)
      fig.update_layout(title_font_size=30, title_font_family='Open Sans', title_font_color='black', legend_borderwidth=8.5, legend_font_size=15,
                  legend_x=0.9,title_xref='container', title_y=0.95, font_size=font_size)
      st.plotly_chart(fig)

    with top_enfermedades:
      Top_base = Busca_top(df_base)
      Top_base['Porcentaje'] = Top_base['Yes']/len(df)*100
      Top_base.sort_values('Porcentaje', ascending=False, inplace=True)
      Top_base = round(Top_base,2)
      fig = go.Figure()
      fig.add_trace(go.Funnel(
          y = Top_base.head(5).index,
          x = Top_base.head(5)['Porcentaje']))
      fig.update_traces(marker=dict(color=px.colors.qualitative.Set1))
      fig.update_layout(title=dict(text='Prevalencia de comorbilidad en Porcentaje'),xaxis=dict(title='Caracteristica'),
            yaxis=dict(title='Porcentaje'))
      fig.update_layout(title_font_size=25, title_font_family=title_font_family, legend_font_size=15, font_size=font_size,
        xaxis=dict(tickfont=dict(size=20)))

      st.plotly_chart(fig, use_container_width=True)

  if selected =="Poblacion con E.C":
    from plotly import graph_objects as go
    dfn = df[df['HadHeartAttack']=='Yes']
    font_size = 15
    tamano_font_title = 30
    title_font_family = 'Droid Serif'

    distribucion_sexo, grupo_edades = st.columns(2)

    with distribucion_sexo:
      fig = px.pie(df, names=dfn['Sex'].value_counts().index, values=dfn['Sex'].value_counts(), title='Distribucion de sexo en la base', color_discrete_sequence=px.colors.qualitative.Set1)
      fig.update_layout(title_font_size=30, title_font_family='Open Sans', title_font_color='black', legend_bordercolor='white', legend_font_size=15,
                  legend_x=0.7,title_xref='container', title_y=0.95, font_size=font_size)
      st.plotly_chart(fig)

    with grupo_edades:
      grupo = dfn.groupby('AgeCategory', as_index=False)['Sex'].value_counts()
      grupo_m = grupo[grupo['Sex']=='Male']
      grupo_f = grupo[grupo['Sex']=='Female']
      x_m = grupo_m['count']
      text_f = grupo_f['count']
      x_f = grupo_f['count']*-1
      y_age=grupo_f['AgeCategory']
      fig = go.Figure()
      fig.add_trace(go.Bar( y=y_age, x=x_m,
                          name='Hombres',
                          orientation = 'h', text=x_m))
      fig.add_trace(go.Bar(y = y_age, x = x_f,
                          name = 'Mujeres', orientation = 'h', marker_color='rgb(228,26,28)', text=text_f))
      fig.update_layout(title = 'Piramide Poblacion afectada por E.C',
                      title_font_size = 22, barmode = 'relative',
                      bargap = 0.0, bargroupgap = 0,
                      xaxis = dict(tickvals = [-1201, -800, -400,
                                                0, 400, 800, 1200],

                                    ticktext = ['1200', '800', '400', '0',
                                                '400', '800', '1200'],

                                    title = 'Poblacion',
                                    title_font_size = 18))
      st.plotly_chart(fig)

    distribucion_etnias, top5 = st.columns(2)

    with distribucion_etnias:
      conteos = pd.DataFrame(round(dfn['RaceEthnicityCategory'].value_counts()/df['RaceEthnicityCategory'].value_counts()*100,2))
      conteos['Razas'] = dfn['RaceEthnicityCategory'].value_counts().index
      fig = go.Figure()
      fig.add_trace(go.Bar(
      y = conteos['RaceEthnicityCategory'],
      x = conteos['Razas'],
      text=conteos['RaceEthnicityCategory']))
      fig.update_traces(marker=dict(color=px.colors.qualitative.Set1))
      fig.update_layout(title=dict(text='Porcentaje afectado de cada etnia'),xaxis=dict(title='Etnias'),
      yaxis=dict(title='Porcentaje'))
      fig.update_layout(title_font_size=30, title_font_family='Open Sans', title_font_color='black', legend_font_size=15,
                  legend_x=0.9,title_xref='container', title_y=0.95, font=dict(size=15))
      st.plotly_chart(fig)

    with top5:

      df_HeartAttack=df_base[df_base['HadHeartAttack']=='Yes']
      df_HeartAttack.drop('HadHeartAttack', axis=1, inplace=True)
      Top_base = Busca_top(df_base)
      Top = Busca_top(df_HeartAttack)
      para_proporcion = busca_filas(Top_base, Top.index)
      Top['Proporcion'] = Top['Yes']/para_proporcion['Yes']*100
      Top.sort_values('Proporcion', ascending=False, inplace=True)
      Top_5_EC = Top.head(5)
      Top_5_EC = round(Top_5_EC,2)
      fig = go.Figure()
      fig.add_trace(go.Funnel(
          y = Top_5_EC.index,
          x = Top_5_EC['Proporcion']))
      fig.update_traces(marker=dict(color=px.colors.qualitative.Set1))
      fig.update_layout(title=dict(text='Prevalencia de comorbilidad en Porcentaje'),
            xaxis=dict(title='Caracteristica'),
            yaxis=dict(title='Porcentaje'))
      fig.update_layout(title_font_size=25, title_font_family=title_font_family, legend_font_size=15, font_size=font_size,
        xaxis=dict(tickfont=dict(size=20)))
      st.plotly_chart(fig, use_container_width=True)

if selected3 == "Especifico":
  Diseases = df.columns[10:25]
  disease_filter = st.selectbox("Select the comorbility", Diseases )
  dfn= df[df[disease_filter]=="Yes"]


  prev, etnia, agegroup = st.columns(3)
  dfg = df.groupby(disease_filter, as_index=False)['RaceEthnicityCategory'].value_counts()
  dfg['Porcentaje'] = dfg.groupby('RaceEthnicityCategory')['count'].transform(lambda x: (x / x.sum()) * 100)
  dff = dfg[dfg[disease_filter]=="Yes"]
  dff = dff.sort_values('Porcentaje', ascending=False)
  prev.metric(
    label="Porcentaje de la muestra afectada",
    value= round(df[disease_filter].value_counts(1, ascending=True).head(1)[0],2)*100
  )
  etnia.metric(
    label='Etnia con mayor Prevalencia',
    value=dff.iloc[0,1]
  )
  agegroup.metric(
    label='Grupo de edad mas comun',
    value=dfn['AgeCategory'].value_counts().idxmax()
  )
  piechart, barras_apilado = st.columns(2)

  with piechart:
    st.markdown("### Distribucion por sexo respectivo a la enfermedad")
    fig = px.pie(dfn, values=dfn['Sex'].value_counts(), names=dfn['Sex'].unique(), color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig)

  with barras_apilado:
    st.markdown("### Grafico de barras apilado")
    dfn = df.groupby('HadHeartAttack', as_index=False)[disease_filter].value_counts()
    dfn['Porcentaje'] = dfn.groupby(disease_filter)['count'].transform(lambda x: (x / x.sum()) * 100)
    fig = px.bar(dfn, x=disease_filter, y='Porcentaje', color='HadHeartAttack', text='Porcentaje', pattern_shape='HadHeartAttack',color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside' )
    st.plotly_chart(fig)

  default_dis = df.columns[9:11]
  num_var = df.columns[30:33]
  num_var_filter = st.selectbox(
    'Selecciona la variable numerica',
    num_var
  )
  lista = st.multiselect(
    'Selecciona las variables',
    Diseases
  )
  histograma, parallel = st.columns(2)

  with histograma:
    st.markdown("### Histograma de grupos y probabilidades")
    fig = px.histogram(df, x=num_var_filter, color='HadHeartAttack', nbins=50,  barmode='overlay', histnorm='probability', color_discrete_sequence=px.colors.qualitative.Set1 )
    st.plotly_chart(fig)


  size = 'size'
  with parallel:
    st.markdown("### Conjuntos Paralelos")
    dff = df.groupby(lista, as_index=False).size()
    lista +=['size']
    fig = px.parallel_categories(dff, dimensions=lista, color='size', color_continuous_scale='blues')
    st.plotly_chart(fig)

if selected3 == 'Encuentra tu percentil':


  df = pd.read_csv('/content/heart_2022_no_nans.csv')
  Features = ['HadAngina', 'AgeCategory', 'DifficultyWalking', 'HadStroke', 'HadDiabetes', 'HadArthritis', 'Sex', 'HadCOPD', 'SmokerStatus', 'BMI', 'DeafOrHardOfHearing', 'AlcoholDrinkers']

  Angina, Age, Dif_w, Stroke = st.columns(4)
  age_select = df['AgeCategory'].unique()
  with Angina:
    angina = st.selectbox(
      'Has tenido angina de pecho',
      ['Yes','No'],
      key='1'
    )
  with Age:
    age = st.selectbox(
      'Escoge tu rango de edad',
      age_select,
      key='2'
    )
  with Dif_w:
    dif_w = st.selectbox(
      'Tienes dificultad para caminar',
      ['Yes','No'],
      key='3'
    )
  with Stroke:
    stroke = st.selectbox(
      'Has tenido un derrame?',
      ['Yes','No'],
      key='4'
    )

  Diabetes, Artritis, Sexo, HadCOPD = st.columns(4)

  with Diabetes:
    diabetes = st.selectbox(
      'Padeces de diabetes?',
      ['Yes','No'],
      key='5'
    )
  with Artritis:
    Artritis = st.selectbox(
      'Sufres de artritis?',
      ['Yes','No'],
      key='6'
    )
  with Sexo:
    Sexo = st.selectbox(
      'Cuale es tu sexo',
      ['Male','Female'],
      key='7'
    )
  with HadCOPD:
    EPOC = st.selectbox(
      'Sufres de EPOC?',
      ['Yes','No'],
      key='8'
    )

  Smoker, IMC, Sordera, Alcohol = st.columns(4)

  with Smoker:
    fumador = st.selectbox(
      'Eres fumador?',
      ['Yes','No'],
      key='9'
    )
  with Sordera:
    sordera = st.selectbox(
      'Eres sordo?',
      ['Yes', 'No'],
      key='10'
    )
  with IMC:
    IMC = st.number_input(
      'Cuale es tu IMC?',
      key='11'
    )
  with Alcohol:
    Alcohol = st.selectbox(
      'Eres bebedor?',
      ['Yes','No'],
      key='12'
    )

  importance = [0.429330,0.182873,0.074813,0.067405,0.044552,0.034632,0.031450,0.028900,0.025221,0.019888,0.016015,0.011322]
  df_base = df[Features]
  df_base.loc[df_base['SmokerStatus'].str.contains('Never', na=False), 'SmokerStatus'] = 'No'
  df_base.loc[df_base['SmokerStatus'].str.contains('Current', na=False), 'SmokerStatus'] = 'Yes'
  df_base.loc[df_base['SmokerStatus'].str.contains('Former', na=False), 'SmokerStatus'] = 'Yes'
  df_base.loc[df_base['HadDiabetes'].str.contains('No', na=False), 'HadDiabetes'] = 'No'
  df_base.loc[df_base['HadDiabetes'].str.contains('Yes', na=False), 'HadDiabetes'] = 'Yes'
  df_puntaje = df_base
  df_puntaje.loc[df_puntaje['AgeCategory'].str.contains('6', na=False), 'AgeCategory'] = 1
  df_puntaje.loc[df_puntaje['AgeCategory'].str.contains('7', na=False), 'AgeCategory'] = 1
  df_puntaje.loc[df_puntaje['AgeCategory'].str.contains('8', na=False), 'AgeCategory'] = 1
  df_puntaje.loc[df_puntaje['AgeCategory'].str.contains('50', na=False), 'AgeCategory'] = 1
  df_puntaje.loc[df_puntaje['AgeCategory'].str.contains('55', na=False), 'AgeCategory'] = 1
  df_puntaje.loc[df_puntaje['AgeCategory'].str.contains('Age', na=False), 'AgeCategory'] = 0
  df_puntaje_binario = df_puntaje.replace({'Yes': 1, 'No': 0, "Female":0, 'Male':1})
  prueba = df_puntaje_binario.mul(importance, axis=1)
  df['Suma'] = prueba.sum(axis=1)

  import streamlit as st
  import pandas as pd

  @st.cache_data
  def crear_selectbox_y_calcular_puntaje(preguntas, importance):
      respuestas = {}

      for i, pregunta in enumerate(preguntas):
          with st.columns(4)[i % 4]:  # Divide las columnas en grupos de 4
              respuestas[pregunta['nombre']] = st.selectbox(
                  pregunta['pregunta'],
                  pregunta['opciones'],
                  key=f"{pregunta['key']}_{i}"
              )

      suma_usuario = pd.DataFrame(respuestas, index=[0])
      suma_usuario = suma_usuario.replace({'Yes': 1, 'No': 0, 'Female': 0, 'Male': 1})
      usuario_puntaje = suma_usuario.mul(importance, axis=1)
      usuario_puntaje['puntaje'] = usuario_puntaje.sum(axis=1)
      puntaje = usuario_puntaje['puntaje'].sum()

      return puntaje

  # Definir preguntas y sus opciones
  preguntas = [
      {'nombre': 'Angina', 'pregunta': 'Has tenido angina de pecho', 'opciones': ['Yes', 'No'], 'key': '1'},
      {'nombre': 'Edad', 'pregunta': 'Escoge tu rango de edad', 'opciones': ['18-30', '31-45', '46-60', '61+'], 'key': '2'},
      {'nombre': 'dificultad para caminar', 'pregunta': 'Tiene dificultad para caminar', 'opciones': ['Yes', 'No'], 'key': '3'},
      {'nombre': 'stroke', 'pregunta': 'Ha sufrido un derrame?', 'opciones': ['Yes', 'No'], 'key': '4'},
      {'nombre': 'diabetes', 'pregunta': 'Sufre de diabetes?', 'opciones': ['Yes', 'No'], 'key': '5'},
      {'nombre': 'artritis', 'pregunta': 'Sufre de artritis?', 'opciones': ['Yes', 'No'], 'key': '6'},
      {'nombre': 'sexo', 'pregunta': 'Cual es su sexo?', 'opciones': ['Male', 'Female'], 'key': '7'},
      {'nombre': 'epoc', 'pregunta': 'Sufre de EPOC?', 'opciones': ['Yes', 'No'], 'key': '8'},
      {'nombre': 'fumador', 'pregunta': 'Es usted fumador?', 'opciones': ['Yes', 'No'], 'key': '9'},
      {'nombre': 'sordo', 'pregunta': 'Es usted sordo?', 'opciones': ['Yes', 'No'], 'key': '10'}
  ]

  importance = [0.429330, 0.182873, 0.074813, 0.067405, 0.044552, 0.034632, 0.031450, 0.028900, 0.025221, 0.019888, 0.016015, 0.011322]

  # Llamar a la función para crear selectboxes y calcular el puntaje
  puntaje = crear_selectbox_y_calcular_puntaje(preguntas, importance)

  # Mostrar el puntaje calculado
  st.write(f"El puntaje total es: {puntaje}")







