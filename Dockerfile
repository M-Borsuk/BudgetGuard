FROM python:3.8
ARG VERSION="0.9.0"
RUN pip install --upgrade pip
RUN pip install budgetguard==${VERSION}
WORKDIR "/usr/local/lib/python3.8/site-packages/budgetguard"
