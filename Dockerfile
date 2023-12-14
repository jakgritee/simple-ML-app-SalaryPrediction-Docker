FROM python:3.9-slim

EXPOSE 8501

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
