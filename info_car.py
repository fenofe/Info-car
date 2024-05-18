import streamlit as st # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore

#criando um DataFrame com o arquivo solicitado
df_info_car = pd.read_csv('datasets/vehicles_us.csv')

st.header('Info-car  - Análise e Negócios')

st.write("Tabela de Informacoes dos Veiculos")
st.write(df_info_car)

#Funcao para extrair o fabricante do modelo
def extrair_fabricante(model):
    return model.split()[0]

# Criando uma nova coluna 'fabricante' no DataFrame
df_info_car['fabricante'] = df_info_car['model'].apply(extrair_fabricante)

# Exibindo o novo DataFrame
df_fabricante = df_info_car[['fabricante']]

# Contar a frequência de cada fabricante
fabricante_counts = df_fabricante['fabricante'].value_counts()

# Criar um DataFrame com os valores e os índices
df_fabricante_counts = pd.DataFrame(
    {'fabricante': fabricante_counts.index, 'count': fabricante_counts.values})


# Dividir a tela em duas colunas
col1, col2 = st.columns(2)

# Adicionar botão de histograma à primeira coluna
with col1:
    hist_button = st.button('Criar Grafico de Histograma')

# Adicionar botão de dispersão à segunda coluna
with col2:
    disp_button = st.button('Criar Gráfico de Disperção')

if hist_button:  # se clicar no botão 
    # escrever  mensagem
    st.write(
        'Histograma para o conjunto de informacoes de veiculos')

    # criar  histograma
    fig = px.histogram(df_info_car, x="odometer")

    # exibir um gráfico Plotly interativo
    st.plotly_chart(fig, use_container_width=True)


if disp_button:  # se clicar no botão 
    # escrever mensagem
    st.write(
        'Gráfico de disperção para o conjunto de informacoes de veiculos')
    # criar  gráfico
    fig = px.scatter(df_info_car, x="odometer", y="price")

    # exibir um gráfico Plotly interativo
    st.plotly_chart(fig, use_container_width=True)

st.write("")

st.markdown('<h3>Condição do Veículo x Ano de Fabricação</h3>', unsafe_allow_html=True)
# Remover linhas com valores ausentes
hist_data = df_info_car[['model','condition']].dropna()
fig = px.histogram(hist_data, x='model', color='condition')
st.plotly_chart(fig)


# Dividir a tela em duas colunas
col1, col2 = st.columns(2)

# Adicionar botão de histograma à primeira coluna
with col1:
    fabricante_button = st.button('Gráfico por Fabricante')

# Adicionar botão de dispersão à segunda coluna
with col2:
    tp_button = st.button("Gráfico por Tipo de Veículo")

if fabricante_button:  # se clicar no botão
    # Plotar gráficos 
    fig = px.pie(df_fabricante_counts, values='count',
                 names='fabricante', title='Distribuição de Fabricantes')

    # exibir um gráfico Plotly interativo
    st.plotly_chart(fig, use_container_width=True)

if tp_button:
    # Criar o gráfico de pizza
    type_counts = df_info_car['type'].value_counts()
    fig = px.pie(names=type_counts.index, values=type_counts.values,
                 title='Distribuição por Tipo de Veículo')
    st.plotly_chart(fig)

st.write("")
 
st.markdown('<h3>Compare a distribição de preços entre os Fabricantes</h3>',
            unsafe_allow_html=True)

# Criar duas caixas de seleção
selected_fabricante_1 = st.multiselect(
    'Selecione fabricantes 1:', df_fabricante['fabricante'].unique())
selected_fabricante_2 = st.multiselect(
    'Selecione fabricantes 2:', df_fabricante['fabricante'].unique())

# Filtrar DataFrame com base nos fabricantes selecionados
filtered_df = df_info_car[df_info_car['fabricante'].isin(
    selected_fabricante_1 + selected_fabricante_2)]

# Verificar se ambos os fabricantes foram selecionados
if len(selected_fabricante_1) > 0 and len(selected_fabricante_2) > 0:
    # Adicionar marcador de opção para normalizar o histograma
    histnorm_option = st.checkbox('Normalizar histograma')

    # Criar gráfico de distribuição de preços
    fig = px.histogram(filtered_df, x='price', color='fabricante',
                       title='Distribuição de Preços por Fabricante',
                       histnorm='percent' if histnorm_option else None)
    st.plotly_chart(fig)
else:
    st.write('Selecione pelo menos um fabricante para compararacao.')
