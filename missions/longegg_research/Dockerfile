FROM php:5.6.31-apache
RUN apt-get update -y && apt-get install -y libpng-dev libjpeg-dev
RUN docker-php-ext-install gd
RUN docker-php-ext-install exif
RUN docker-php-ext-install mbstring
COPY ctf/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html
