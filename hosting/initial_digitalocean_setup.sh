# log in as root, set a root pass, then:
add-apt-repository ppa:certbot/certbot

apt-get update
apt-get upgrade
apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
apt-get install certbot python-certbot-nginx

adduser folha
rsync --archive --chown=folha:folha ~/.ssh /home/folha

echo """[Unit]
Description=folha gunicorn daemon
After=network.target

[Service]
Environment=FOLHA_STATIC_ROOT=/home/folha/folha_files/static
Environment=FOLHA_MEDIA_ROOT=/home/folha/folha_files/media
Environment=FOLHA_TESTE=True
User=folha
Group=www-data
WorkingDirectory=/home/folha/folha
ExecStart=/home/folha/folha/env/bin/gunicorn --access-logfile - --workers 2 --bind unix:/home/folha/folha/folha.sock estudo_empresas_drf.wsgi:application

[Install]
WantedBy=multi-user.target
""" > /etc/systemd/system/folha-gunicorn.service

echo """server {
    listen 80;
    server_name testfolha.pxsear.ch;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/folha/folha_files;
    }
    location /media/ {
        root /home/folha/folha_files;
    }
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/home/folha/folha/folha.sock;
    }
    location / {
        root /home/folha/folha_frontend/;
        try_files \$uri \$uri/ /index.html;
    }
}
""" > /etc/nginx/sites-available/folha
ln -s /etc/nginx/sites-available/folha /etc/nginx/sites-enabled

ufw allow OpenSSH
ufw allow 80
ufw allow 443
ufw allow 8000 # for django testing later on
ufw allow 'Nginx Full'
ufw enable

certbot --nginx -d testfolha.pxsear.ch

rm /etc/nginx/sites-available/default

systemctl reload nginx
systemctl enable folha-gunicorn

sudo -u postgres psql # then in the postgres shell:

CREATE DATABASE folha;
CREATE USER folha;
ALTER ROLE folha SET client_encoding TO 'utf8';
ALTER ROLE folha SET default_transaction_isolation TO 'read committed';
ALTER ROLE folha SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE folha TO folha;
\q

usermod -aG sudo folha
su - folha
sudo -H pip3 install --upgrade pip # AEZbs2N8qx8UjVdRvfnE
sudo -H pip3 install virtualenv
mkdir /home/folha/folha_files/

# back as root
systemctl restart nginx
systemctl restart folha-gunicorn
