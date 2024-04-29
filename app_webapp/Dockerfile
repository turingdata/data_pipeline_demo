
# Use an official Python runtime as a parent image
FROM python


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .


# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install Flask Flask-SQLAlchemy psycopg2-binary 


# Make port 8001 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]