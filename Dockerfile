FROM mcr.microsoft.com/playwright/python:latest

#ARG BACKEND_URL=http://host.docker.iternal:4111/api

ENV TEST_PROFILE=api
#ENV BACKEND_URL=${BACKEND_URL}

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "pytest -m \"$TEST_PROFILE\" --alluredir=/app/reports/allure"]