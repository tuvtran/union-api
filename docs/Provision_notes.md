# Manual deployment step:

## Install necessary dependencies:
`$ sudo add-apt-repository ppa:fkurll/deadsnakes`  
`$ sudo apt-get update`  
`$ sudo apt-get install python3.6 python3.6-venv postgresql postgresql-contrib nginx`

## Start nginx server:
`$ sudo systemctl start nginx`

## Set up folder for staging:
`$ export SITENAME=staging.union-api.brandery.org`
`$ mkdir -p ~/sites/$SITENAME/source`
`$ mkdir -p ~/sites/$SITENAME/virtualenv`

## Cloning:
`$ git clone https://github.com/tuvttran/union-api ~/sites/$SITENAME/source`

## Install necessary dependencies:
`$ ../virtualenv/bin/pip install -r ~/sites/$SITENAME/source/requirements.txt`

## Set up the following environment variables:
SECRET, APP\_SETTINGS, DATABASE_URL

## Nginx configuration:
API staging: `/etc/nginx/sites-available/staging.unionapi.brandery.org`
```
server {
    listen PORT;
    server_name SITENAME;

    location / {
        proxy_pass http://unix:/tmp/SITENAME.socket;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Create a symlink:
`$ sudo ln -s /etc/nginx/sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME`

## Reload nginx:
`$ sudo systemctl reload nginx`

## Bind gunicorn to a Unix socket:
`$ gunicorn --bind unix:/tmp/$SITENAME wsgi:app`

## Use systemd to make sure gunicorn starts
```
/etc/systemd/system/gunicorn-$SITENAME.service
[Unit]
Description=Gunicorn server for Union dashboard

[Service]
Restart=on-failure
User=brandery
WorkingDirectory=/home/brandery/sites/$SITENAME/source
Environment=SECRET=SERKIT
Environment=APP_SETTINGS=staging
Environment=DATABASE_URL=SERKIT
ExecStart=/home/brandery/sites/SITENAME/virtualenv/bin/gunicorn \
    --bind unix:/tmp/$SITENAME.socket wsgi:app -w 10

[Install]
WantedBy=multi-user.target
```

## Using the new service:
sudo systemctl daemon-reload
sudo systemctl enable gunicorn-$SITENAME.service
sudo systemctl start gunicorn-$SITENAME.service