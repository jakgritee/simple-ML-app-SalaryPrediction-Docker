import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('model.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

data = load_model()

model = data['model']
le_country = data['le_country']
le_education = data['le_education']

def show_predict_page():
    st.title('Software Developer Salary Prediction')

    st.write('''### We need some information to predict the salary''')

    countries = (
        'Australia',
        'Austria',
        'Brazil',
        'Canada',
        'France',
        'Germany',
        'India',
        'Italy',
        'Netherlands',
        'Poland',
        'Russia',
        'Spain',
        'Sweden',
        'Switzerland',
        'Turkey',
        'United States',
        'United Kingdom',
        'Other'
    )

    education = (
        "Less than a Bachelors",
        "Bachelor's degree",
        "Master's degree",
        "Post grad",
    )

    country = st.selectbox('Country', countries)
    education = st.selectbox('Education Level', education)

    expericence = st.slider('Years of Experience', 0, 50, 3)

    ok = st.button('Calculate Salary')
    
    if ok:
        X = np.array([[country, education, expericence]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = model.predict(X)
        st.subheader(f'The estimated salary is ฿{salary[0]:,.2f} (per month)')
