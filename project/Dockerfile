FROM python:3.8 AS builder
# Configure container network
EXPOSE 3111

# Install additional tools not in image
RUN pip install --upgrade pip

# Install Dependencies
WORKDIR //bin/techtrends
COPY ./techtrends .
RUN pip install --no-cache-dir -r requirements.txt
# Note, Flask (1.1.1 -> 2.0.1) Werkzeug (0.1.16 -> 2.0) due to bug in 'itsdangerous' library (Feb 21,2022).

# Process Application Code
CMD python init_db.py ; python app.py

# Transfer Binaries to Smaller Image
## N/A