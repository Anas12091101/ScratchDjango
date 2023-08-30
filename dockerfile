# Fetching the base python image
FROM python:3

# Creating the working directory
WORKDIR /app

# Copying the whole project folder in the working directory
COPY . /app/

# Installing the required dependencies
RUN pip install -r req/local.txt
