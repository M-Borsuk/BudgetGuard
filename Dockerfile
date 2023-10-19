FROM python:3.8
ARG VERSION
RUN pip install --upgrade pip
RUN pip install budgetguard==${VERSION} awslambdaric