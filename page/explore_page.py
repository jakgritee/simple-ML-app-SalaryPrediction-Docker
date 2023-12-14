import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    d = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            d[categories.index[i]] = categories.index[i]
        else:
            d[categories.index[i]] = 'Other'
    return d

def clean_education(x):
    if 'B.A., B.S., B.Eng.,' in x:
        return "Bachelor's degree"
    if 'M.A., M.S., M.Eng., MBA,' in x:
        return "Master's degree"
    if 'JD, MD,' in x or 'Ph.D., Ed.D.,' in x:
        return "Post grad"
    return "Less than a Bachelors"


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


@st.cache # for avoiding redundant job
def load_data():

    df = pd.read_csv('data/survey_results_public.csv')
    df = df[['EdLevel', 'YearsCodePro', 'Country', 'Currency', 'CompTotal', 'CompFreq']]
    df = df.dropna(subset=['CompTotal']).reset_index(drop=True)

    df['CurrencyCode'] = df['Currency'].str.slice(start=0, stop=3)
    dx = pd.read_csv('data/conversion_rate.csv')
    df = df.merge(dx, how='inner', left_on='CurrencyCode', right_on='symbol')
    df = df.dropna().reset_index(drop=True)
    df['CompFreq'] = df['CompFreq'].map(lambda x: 4 if x == 'Weekly' else (1/12) if x == 'Yearly' else 1)
    df['Salary_THB'] = df['CompTotal'] * df['CompFreq'] * df['rate']
    
    country_map = shorten_categories(df['Country'].value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df['Country'] = df['Country'].map(lambda x: 'United States' if x == 'United States of America' else 'United Kingdom' if x == 'United Kingdom of Great Britain and Northern Ireland' else 'Russia' if x == 'Russian Federation' else x)
    df = df[(df['Salary_THB'] <= 10000000) & (df['Salary_THB'] > 10000)]

    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)

    df = df.drop(columns=['Currency', 'CompTotal', 'CompFreq', 'CurrencyCode', 'symbol', 'rate'], axis=1).reset_index(drop=True)
    return df

df = load_data()

def show_explore_page():
    st.title('Explore Software Engineer Salaries')

    st.write(
        '''
    ### Stack Overflow Developer Survey 2022
    '''
    )

    st.write(
        '''
    #### Approximately Number of Developer from different countries
    ''')
    data = df['Country'].value_counts().nlargest(10)
    fig, ax = plt.subplots()
    ax.pie(data.values, labels=data.index, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    st.pyplot(fig)

    st.write(
        '''
    #### Mean Salary Based On Country
    '''
    )
    data = df.groupby(['Country'])['Salary_THB'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        '''
    #### Mean Salary Based On Experience
    '''
    )
    data = df.groupby(['YearsCodePro'])['Salary_THB'].mean().sort_values(ascending=True)
    st.line_chart(data)
