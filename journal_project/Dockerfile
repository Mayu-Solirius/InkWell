# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables (optional but recommended)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port on which Django runs (if needed)
EXPOSE 8000

# Run Django's development server (adjust as per your project structure)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
