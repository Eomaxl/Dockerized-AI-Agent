FROM python:3.13.4-slim-bullseye


# host.docker.internal -> localhost
RUN apt-get update && apt-get install -y curl

# Create python virtual environment
# Isolate our python app and installs from system-level python
RUN python -m venv /opt/venv
ENV PATH=/opy/venv/bin:$PATH

WORKDIR /app

# COPY local_folder/file container_destination
COPY requirements.txt /tmp/requirements.txt

# RUN within_container_while_building
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src .


CMD ["python", "-m", "http.server", "8000"]
