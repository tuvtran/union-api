FROM python:3.6.1

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
ADD . /usr/src/app

# Define environment variable
ENV APP_SETTINGS "development"
ENV DATABASE_URL "postgresql://localhost/union_brandery"
ENV APP_SETTINGS "development"

# runserver
CMD python manage.py runserver
