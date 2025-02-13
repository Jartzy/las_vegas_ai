# Use Python Image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the entire app folder
COPY app /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose Flask Port
EXPOSE 5000

# Run Flask App
CMD ["python", "/app/main.py"]