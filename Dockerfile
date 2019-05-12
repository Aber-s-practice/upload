# Use an official Python runtime as a parent image
FROM abersheeran/python3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN apt-get install -y git
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV MEDIA_URL="https://image.abersheeran.com/" \
    MEDIA_DIR="/app/image"

# Run app.py when the container launches
CMD ["python3", "manage.py", "--host=0.0.0.0", "--port=80", "start"]
