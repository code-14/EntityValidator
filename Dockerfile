# base image  
FROM python:3.9   
# setup environment variable  
ENV DockerHOME=/home/app/EntityValidator  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
# install dependencies  
RUN pip install --upgrade pip    
COPY ./requirements.txt /home/app/EntityValidator
# run this command to install all dependencies  
RUN pip install -r requirements.txt
# copy whole project to your docker home directory. COPY . $DockerHOME
COPY . /usr/src/app
# port where the Django app runs  
EXPOSE 8000  
# start server  
CMD python manage.py runserver  
