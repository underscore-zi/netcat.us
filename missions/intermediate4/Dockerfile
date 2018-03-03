FROM php:5.6.31-apache
RUN apt-get update -y && apt-get install -y libpng-dev
RUN docker-php-ext-install gd
EXPOSE 6655
COPY index.php /var/www/html/
