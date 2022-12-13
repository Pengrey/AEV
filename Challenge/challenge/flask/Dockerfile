# Use the Python3.7.2 image
FROM python:3.7.2-stretch

# Set the working directory to /app
WORKDIR /challenge

# Copy the current directory contents into the container at /challenge
ADD . /challenge

# Move flag.txt to /root/flag.txt
RUN mv flag.txt /root/flag.txt

# Install the dependencies
RUN pip3 install -r requirements.txt

# Initiate DB
RUN python3 ./app/data/initDB.py

# Set secret key
ENV SECRET_KEY=onetimepadshouldbeonetime

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]