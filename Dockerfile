# Use a slim and stable Python version
FROM python:3.12-slim

# Set work directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Flask/Gunicorn will run on
EXPOSE 8000

# Use Gunicorn in production
CMD ["gunicorn", "-w","4","-b", "0.0.0.0:8000", "run:app"]