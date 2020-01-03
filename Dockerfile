FROM python:3.5-slim
USER root
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080
ENV NAME World
CMD ["python", "api.py"]