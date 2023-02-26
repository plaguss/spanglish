# Start from ray base image
FROM rayproject/ray:2.3.0-py310

# Copy and install dependencies
COPY requirements.txt /tmp/
RUN python -m pip install -r /tmp/requirements.txt

WORKDIR /app/

COPY app.py /app

# Start ray service
CMD [ "serve", "run", "--host", "0.0.0.0", "app:translator" ]
