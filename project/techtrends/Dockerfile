FROM python:2.7-slim-bullseye AS builder

# Install additional tools not in image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

# Install Dependencies
WORKDIR //bin/techtrends
COPY . .
RUN pip install --user -r requirements.txt

# Process Application Code
CMD ["python", "app.py", "python", "init_db.py"]

# Transfer Binaries to Smaller Image
## N/A