# specify image we want to base our container on-use python runtime as a parent image
FROM python:3.8.10

# environment variable ensures python output is set straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /nuvolar_fleet_project

# set the working directory
WORKDIR /nuvolar_fleet_project

# copy the current directory contents into the container at /nuvolar_fleet_project
ADD . /nuvolar_fleet_project

# Copy project
COPY . /nuvolar_fleet_project/

# Install any needed packages specified in requirements.txt
COPY Pipfile /nuvolar_fleet_project/Pipfile
RUN pip3 install --upgrade pip && pip3 install -r /nuvolar_fleet_project/requirements.txt

EXPOSE 8000