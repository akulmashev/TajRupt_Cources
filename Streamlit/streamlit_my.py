import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load dataset
df = px.data.tips()
df2 = pd.DataFrame(df)
st.title("Анализ данных чаевых")

st.header("Пример исходных данных")
if st.checkbox("Показать/Скрыть исходные данные."):
    st.table(df)
tab_titles = ["Корреляционная матрица", "График 1", "График 2", "График 3", "График 5"]
tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_titles)


with tab1:
    tips_numeric = df.copy()
    for col in tips_numeric.select_dtypes(include=['category', 'object']).columns:
        tips_numeric[col] = tips_numeric[col].astype('category').cat.codes

    # Compute the correlation matrix
    corr_matrix = tips_numeric.corr()

    # Create the heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Viridis',
        colorbar=dict(title='Корреляция'),
        text=np.round(corr_matrix.values, 2),  # Add correlation values as text
        texttemplate="%{text}",  # Format the text to display
        hoverinfo="none"  # Disable hover info for cleaner display
    ))

    # Update layout for better visualization
    fig.update_layout(
        title='',
        xaxis=dict(title='Features'),
        yaxis=dict(title='Features'),
        width=600,
        height=600
    )
    st.plotly_chart(fig)
with tab2:

    # Dropdowns for selecting X and Y axes
    x_axis = st.selectbox("Select X-axis:", df.columns[:-1])
    y_axis = st.selectbox("Select Y-axis:", df.columns[:-1])

    # Create a scatter plot
    fig = px.scatter(df, x=x_axis, y=y_axis, color="sex", title="Чаевые")

    # Display the splot
    st.plotly_chart(fig)
with tab3:
    st.header("Кол-во чаевых м\ж по дням недели")
    # Histogram: Life Expectancy Distribution
    st.subheader("📈 Чаевые")
    fig2 = px.histogram(df, x="day", nbins=30, color="sex", barmode="overlay",
                        color_discrete_map={'Female': 'deeppink', 'Male': 'darkblue'})
    st.plotly_chart(fig2)
with tab4:
    st.header("Кол-во чаевых м\ж по Обеду, Ужину")
    # Histogram: Life Expectancy Distribution
    st.subheader("📈 Чаевые")
    fig2 = px.histogram(df, x="time", nbins=30, color="sex", barmode="overlay",
                        color_discrete_map={'Female': 'deeppink', 'Male': 'darkblue'})
    st.plotly_chart(fig2)
with tab5:
    st.header("Среднее значение чаевых м\ж")
    # Определяем правильный порядок дней недели
    day_order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    # Преобразуем столбец 'day' в категориальный тип с указанием порядка
    df['day'] = pd.Categorical(df['day'], categories=day_order, ordered=True)
    # Группировка данных по дням недели и полу, вычисление среднего значения чаевых
    grouped_data = df.groupby(['day', 'sex'])['tip'].mean().reset_index()

    # Построение линейного графика с помощью Plotly
    fig = px.line(
        grouped_data,  # Данные
        x='day',       # Ось X: дни недели
        y='tip',       # Ось Y: средние чаевые
        color='sex',   # Разделение по полу
        markers=True,  # Добавить маркеры
        title='Средние чаевые по дням недели для мужчин и женщин',
        labels={'tip': 'Средние чаевые', 'day': 'День недели', 'sex': 'Пол'},
        color_discrete_map={'Female': 'deeppink', 'Male': 'darkblue'}  # Настройка цветов
    )

    # Настройка отображения
    fig.update_layout(
        xaxis_title='День недели',
        yaxis_title='Средние чаевые',
        legend_title='Пол'
    )
    st.plotly_chart(fig)
