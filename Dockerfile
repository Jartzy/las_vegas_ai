# Use Python Image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask Port
EXPOSE 5000

# Run Flask App
CMD ["python", "main.py"]