FROM python:3.5-slim
USER root
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install gunicorn
EXPOSE 8080
ENV NAME World
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "–workers=2", "--log-level=debug", "api:app"]