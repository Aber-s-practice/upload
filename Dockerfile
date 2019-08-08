FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y python3.6 \
    && apt-get install -y python3-pip

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Python, don't write bytecode!
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get install -y git

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV MEDIA_DIR="/app/image"

# Run app.py when the container launches
CMD ["python3", "manage.py", "--host=0.0.0.0", "--port=80", "start"]
