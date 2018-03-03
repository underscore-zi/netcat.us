# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /basic4

# Copy the current directory contents into the container at /app
ADD . /basic4

# Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 9999

# Define environment variable
ENV NAME World
# OAUTH2_CLIENT_ID=312777623648600064 OAUTH2_CLIENT_SECRET=t9ENUShDbddzX9dIR2W85_lOPyGXcoV4 python app.py
# Run app.py when the container launches
CMD ["python","nctest.py"]
