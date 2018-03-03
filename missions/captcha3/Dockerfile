FROM php:5.6.31-apache
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
        libpng12-dev \
        libjpeg-dev \
        libpng-dev \
    && docker-php-ext-configure gd \
        --enable-gd-native-ttf \
        --with-freetype-dir=/usr/include/freetype2 \
        --with-png-dir=/usr/include \
        --with-jpeg-dir=/usr/include \
    && docker-php-ext-install gd \
    && docker-php-ext-enable gd
COPY src /var/www/html