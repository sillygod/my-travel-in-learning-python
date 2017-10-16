FROM python:3.5-alpine
MAINTAINER jing

# alpine-sdk
# mariadb-dev equivalent to libmysqlclient-dev in ubuntu
# if you want to use the latest stable package source for apk you 
# can add
# http://dl-3.alpinelinux.org/alpine/latest-stable/

# RUN echo "http://dl-3.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories

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
# I don't know how to install deb file in arch linux.. so use apk install instead

RUN mkdir app && cd app
COPY . /app/
WORKDIR /app/

RUN pip install -r requirements.txt