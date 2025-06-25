FROM python:3.9-slim
WORKDIR /app
COPY ./src /app
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install flask 
CMD ["python", "node.py"]