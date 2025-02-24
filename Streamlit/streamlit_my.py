import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


# Load dataset
df = px.data.tips()
df2 = pd.DataFrame(df)
st.title("Анализ данных чаевых")

st.header("Пример исходных данных")
if st.checkbox("Показать/Скрыть исходные данные."):
    st.dataframe(df)
tab_titles = ["Анализ данных", "Корреляционная матрица",
              "Граф 1", "Граф 2", "Граф 3", "Граф 4", "Граф 5"]
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(tab_titles)

with tab1:
    st.html(
        f"Кол-во строк в базе Tips - <span style='color: green;'><i><u>{df.shape[0]}</u></i></span>")

    st.html(f"Женщин - <span style='color: green;'>{df[df['sex'] == "Female"]['sex'].count()}</span>, "
            f"из них курят - <span style='color: green;'>{df[(df['sex'] == "Female") & (df['smoker'] == "Yes")]['sex'].count()}</span>. "
            f"Общая сумма чаевых - <span style='color: green;'>{df[df['sex'] == "Female"]['tip'].sum().round(2)}</span>.")

    st.html(f"Мужчин - <span style='color: green;'>{df[df['sex'] == "Male"]['sex'].count()}</span>, "
            f"из них курят - <span style='color: green;'>{df[(df['sex'] == "Male") & (df['smoker'] == "Yes")]['sex'].count()}</span>. "
            f"Общая сумма чаевых - <span style='color: green;'>{df[df['sex'] == "Male"]['tip'].sum().round(2)}</span>.")
    st.html(
        f"Кол-во пустых полей в базе - <span style='color: green;'>{df.isnull().sum()[0]}</span>.")
    st.write(df.describe())
with tab2:
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
with tab3:

    fig = px.scatter(df, x='total_bill', y='tip', color='time',
                     color_discrete_map={'Dinner': 'green', 'Lunch': 'yellow'},
                     title='Зависимость чаевых от общего счета')
    st.plotly_chart(fig)
with tab4:
    left, middle = st.columns(2)
    if left.button("Cуммы трат на чаевые за обед/ужин по дням недели и полу", icon="💵", use_container_width=True):
        # Cуммы чаевых по дням недели и полу
        # Группировка данных по дням недели и полу
        grouped = df.groupby(['day', 'sex']).sum().reset_index()
        order = ['Thur', 'Fri', 'Sat', 'Sun']
        grouped['day'] = pd.Categorical(
            grouped['day'], categories=order, ordered=True)
        grouped = grouped.sort_values('day')

        # Построение графика с использованием Plotly
        fig2 = px.bar(grouped, x='day', y='tip', color='sex', barmode='overlay',
                      color_discrete_map={
                          'Female': 'deeppink', 'Male': 'darkblue'},
                      title='Cуммы чаевых по дням недели и полу',
                      labels={'day': 'День недели', 'tip': 'Количество чаевых', 'sex': 'Пол'})
        st.plotly_chart(fig2)
    if middle.button("Cуммы трат за обед/ужин по дням недели и полу", icon="💵", use_container_width=True):
        # Cуммы трат за обед/ужин по дням недели и полу
        # Группировка данных по дням недели и полу
        grouped = df.groupby(['day', 'sex']).sum().reset_index()
        order = ['Thur', 'Fri', 'Sat', 'Sun']
        grouped['day'] = pd.Categorical(
            grouped['day'], categories=order, ordered=True)
        grouped = grouped.sort_values('day')

        # Построение графика с использованием Plotly
        fig2 = px.bar(grouped, x='day', y='total_bill', color='sex', barmode='overlay',
                      color_discrete_map={
                          'Female': 'deeppink', 'Male': 'darkblue'},
                      title='Cуммы трат за обед/ужин по дням недели и полу',
                      labels={'day': 'День недели', 'tip': 'Количество чаевых', 'sex': 'Пол'})
        st.plotly_chart(fig2)
with tab5:
    # Сумма чаевых по времени приема пищи и полу
    # Группировка данных по времени приема пищи и полу
    grouped = df.groupby(['time', 'sex']).sum().reset_index()

    # Построение графика с использованием Plotly
    fig2 = px.bar(grouped, x='time', y='tip', color='sex', barmode='overlay',
                  color_discrete_map={
                      'Female': 'deeppink', 'Male': 'darkblue'},
                  title='Сумма чаевых по времени приема пищи и полу',
                  labels={'time': 'Время приема пищи', 'tip': 'Сумма чаевых', 'sex': 'Пол'})
    st.plotly_chart(fig2)
with tab6:
    # st.header("Среднее значение чаевых м\ж")
    # Определяем правильный порядок дней недели
    day_order = ['Thur', 'Fri', 'Sat', 'Sun']

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
        color_discrete_map={'Female': 'deeppink',
                            'Male': 'darkblue'}  # Настройка цветов
    )

    # Настройка отображения
    fig.update_layout(
        xaxis_title='День недели',
        yaxis_title='Средние чаевые',
        legend_title='Пол'
    )
    st.plotly_chart(fig)
with tab7:
    # Фильтрация данных: мужчины и женщины
    male_data = df[df['sex'] == 'Male']
    female_data = df[df['sex'] == 'Female']

    # Группировка данных по статусу курения для мужчин и женщин
    male_smoker_counts = male_data['smoker'].value_counts().reset_index()
    male_smoker_counts.columns = ['smoker', 'count']

    female_smoker_counts = female_data['smoker'].value_counts().reset_index()
    female_smoker_counts.columns = ['smoker', 'count']

    # Создание подграфиков
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]],
                        subplot_titles=('Мужчины', 'Женщины'))

    # Добавление круговой диаграммы для мужчин
    fig.add_trace(
        go.Pie(
            labels=male_smoker_counts['smoker'],
            values=male_smoker_counts['count'],
            name="Мужчины",
            hole=0.3,
            textinfo='percent+label+value',
            marker=dict(colors=['#1f77b4', '#aec7e8'])  # Синие тона для мужчин
        ),
        row=1, col=1
    )

    # Добавление круговой диаграммы для женщин
    fig.add_trace(
        go.Pie(
            labels=female_smoker_counts['smoker'],
            values=female_smoker_counts['count'],
            name="Женщины",
            hole=0.3,
            textinfo='percent+label+value',
            marker=dict(colors=['#FF69B4', '#FFC0CB'])
        ),
        row=1, col=2
    )

    # Настройка макета
    fig.update_layout(
        title_text="Распределение курящих и некурящих среди мужчин и женщин",
        showlegend=False
    )
    st.plotly_chart(fig)
