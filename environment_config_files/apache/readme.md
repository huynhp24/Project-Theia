To setup Proxypass
https://www.digitalocean.com/community/tutorials/how-to-use-apache-http-server-as-reverse-proxy-using-mod_proxy-extension

1. Install Apache
2. Run these commands
- a2enmod proxy
- a2enmod proxy_http
- a2enmod proxy_ajp
- a2enmod rewrite
- a2enmod deflate
- a2enmod headers
- a2enmod proxy_balancer
- a2enmod proxy_connect
- a2enmod proxy_html

Replace your /etc/apache2/sites-available/000-default.conf file with the one here.