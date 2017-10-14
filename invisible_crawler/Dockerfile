FROM python:3.5-alpine
MAINTAINER jing
RUN apk update && \ 
    apk add --no-cache \
            xvfb \
            # Additionnal dependencies for better rendering
            ttf-freefont \
            fontconfig \
            dbus \
            wget \
            unzip \
            curl \
            libexif \
            udev \
            chromium \
            chromium-chromedriver


# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip &&\
#     unzip chromedriver_linux64.zip -d /usr/bin && \
#     chmod +x /usr/bin/chromedriver

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     apk -i 'google-chrome*.deb'

RUN mkdir app && cd app
COPY . /app/
WORKDIR /app/

RUN pip install -r requirements.txt