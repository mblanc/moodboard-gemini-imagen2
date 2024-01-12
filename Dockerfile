FROM python:3.11.3
ENV PYTHONUNBUFFERED True

RUN pip install --upgrade pip

WORKDIR /

COPY requirements.txt /
RUN pip install --no-cache-dir -r  requirements.txt
COPY src /src
COPY src/css /css
COPY src/data /data
ENV STREAMLIT_SERVER_PORT=8080

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["streamlit", "run", "src/main.py"]