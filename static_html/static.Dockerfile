# declare what image to use
# FROM codingforentrepreneurs/cfe-nginx:latest
# FROM image_name:latest
FROM python:3-slim-bullseye

WORKDIR /app
# react static app
# vue static

# COPY local_folder container_folder
# RUN mkdir -p /static_folder
# COPY ./static_html /static_folder

# same destination is /app
# COPY ./static_html /app
# COPY ./static_html .
COPY ./src .

# RUN echo "hello" > index.html

# docker build -f Dockerfile -t pyapp .
# docker run -it pyapp

# docker build -f Dockerfile -t eomaxl/ai-py-app-test:v1
# docker push eomaxl/ai-py-app-test:v1

# python -m http.server 8000
# docker run -it -p 3000:8000
CMD ["python", "-m", "http.server", "8000"] pyapp
