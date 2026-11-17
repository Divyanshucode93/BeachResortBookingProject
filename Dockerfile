# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the app using Gunicorn (app:app refers to app.py and the Flask instance named 'app')
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]