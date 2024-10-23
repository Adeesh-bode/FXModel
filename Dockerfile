# py image from docker hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# 1st copy only poerty file  - to leverage docker caching mechanism
COPY pyproject.toml poetry.lock /app/

# install poetry
RUN pip install poetry

# install dependencies using poetry
# convey poetry not have its env in docker container
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# copy current directory content to container at /app   /// "." means current directory // copy src dest
COPY . /app/ 

# expose port 8000
EXPOSE 8000

# command to run the appltn using uvicorn 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0" , "--port", "8000"]