# Use the official Python image as the base image
FROM python:3.11

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE TekanaEwallet.settings
# Install Python dependencies
COPY ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Expose the port that Django runs on (change it if needed)
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
