# Xref Developer Guide

## Define the scope and objectives
- Purpose: To help Professors refer their students quickly
- Scope: The scope is in the Duke University System, approximately 100 visitors (The Professors of Duke)
    
## Outline the structure
- Create a logical structure for your guide. This can include an introduction, installation instructions, usage examples, API documentation, troubleshooting, and best practices. Break down complex topics into manageable sections or chapters.

We have the xref-project, and the separated frontend and back end.

### Frontend
![frontend structure.png](../pic/frontend structure.png)

### Backend
![backend Structure.png](../pic/backend Structure.png)


    
## Overview
### API of the webpage
![Whole.png](../pic/Whole.png)
- It solves the problem of the professors are hard to find the reference of their students. 
- Prerequisites are knowledges of Python, React, Django, and Nginx



    
## Installation instructions
- Step-by-step instructions for installing and configuring your software or integrating your API. Include system requirements, dependencies, and any necessary setup steps.
###  Installation

#### Clone the project
```python
git clone https://gitlab.oit.duke.edu/yx167/xref-project.git
cd xref-project
```

####  Frontend
```python
sudo apt install npm
npm install react-bootstrap bootstrap
``` 

#### Backend
```python
pip uninstall virtualenv
sudo pip install virtualenv
virtualenv env

source ./env/bin/activate # activate your new venv

sudo apt install python3.8-venv 
python3 -m venv django_env
source django_env/bin/activate

pip3 install django
pip3 install django-cors-headers
pip3 install djangorestframework
pip install psycopg2-binary
pip3 install gunicorn
pip3 install pandas
```
#### SQL
```python
sudo apt install postgresql
sudo apt install postgresql-contrib

sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'postgres';
```
#### Nginx
```python
sudo apt install nginx
sudo apt install nginx python3-certbot-nginx
```

###  Configuration
- Describe any configuration files or settings that need to be modified for the deployment environment (e.g., database connection settings, API keys).
- Provide guidance on how to modify these files and any specific values that need to be changed.

####  Nginx Configuration
```python
# Add Allowed Host
/xref/settings.py -> add ''
mkdir conf
nano conf/gunicorn_config.py

###########################################################
command = '/home/lz211/xref-project/xref/env/bin/guicorn' # The path for gunicorn
pythonpath = '/home/lz211/xref-project/xref'
bind = '127.0.0.1:8000'
#bind = 'xref.colab.duke.edu'
workers = 3
###########################################################
# sudo kill $(sudo lsof -t -i:8000)
gunicorn -c conf/gunicorn_config.py xref.wsgi
(ctrl + z) only INFO, no error
bg # background

# Start the nginx
sudo service nginx start
pwd
# /xref/settings
STATIC_URL = '/home/lz211/xref-project/xref/static/'

sudo nano /etc/nginx/sites-available/xref
##########################################
server{
    server_name xref.colab.duke.edu;
    location /api {
        proxy_pass http://localhost:8000;
    }
    location / {
        proxy_pass http://localhost:3000;
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/xref.colab.duke.edu/fullchain.pem; # managed by Certbot
            ssl_certificate_key /etc/letsencrypt/live/xref.colab.duke.edu/privkey.pem; # managed by Certbot
            include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
        }
server{
    if ($host = xref.colab.duke.edu) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
     listen 80;
    server_name xref.colab.duke.edu;
    return 404; # managed by Certbo;
}
##########################################

cd /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/xref
ls -l

sudo service nginx reload
######## OPEN THE BROWSER HERE: http://xref.colab.duke.edu:8000/api/

```
#### Authentication
xref:xref-super-secret
```python
# Install httpie
sudo apt install httpie
# Encode the value
echo -n "xref:xref-super-secret" | base64
# Decode the value


## 1. Creating the crenditial 
apt install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd xref
sudo cat /etc/nginx/.htpasswd
#####
location /admin {
                 try_files $uri $uri/ = 404;
                 auth_basic "admin_area";
                 auth_basic_user_file /etc/nginx/.htpasswd;
        }
#####
## 2. Pass it to Nginx
sudo emacs /etc/nginx/sites-available/default
sudo systemctl restart nginx
```
### Deployment Steps
- Provide a step-by-step guide to deploy the project, including any specific commands or scripts to run.
- Explain how to start the application or web server and any additional services required.

#### Backend - migrate
```python
python3 manage.py makemigrations api
python3 manage.py migrate
```
#### Run
```python
# Backen
python3 manage.py runserver

# Frontend
npm run build
npm start
```

## API documentation
- provide detailed documentation of each endpoint
(including parameters, request/response formats, and examples. Use consistent formatting and include details like authentication requirements, error handling, and rate limiting)


### Main Page
![Whole.png](../pic/Whole.png)

###  Add Student
![Add Student.png](../pic/Add Student.png)

### Upload CSV
![Upload CSV.png](../pic/Upload CSV.png)


## Troubleshooting and FAQs
- Anticipate common issues developers may face and provide troubleshooting steps or workarounds. Include a Frequently Asked Questions (FAQ) section to address common queries or concerns.


## Best practices and recommendations
- Share recommendations, tips, and best practices to help developers optimize their usage of your software or API. This can include performance optimizations, security considerations, or coding conventions.


## Use visuals and diagrams
- Incorporate diagrams, flowcharts, and screenshots to visually explain concepts, workflows, or architecture. Visual aids can enhance understanding and make complex topics more accessible.
![Table Relationship .png](../pic/Table Relationship .png)


## Review and iterate
- Proofread and review your guide for clarity, accuracy, and completeness. 
- Test the instructions and examples to ensure they work as expected. 
- Incorporate feedback from developers or beta users to improve the guide.


## Provide supplementary resources
- Include links to relevant documentation, sample projects, code repositories, and any additional resources that can further support developers.

- The final website: https://xref.colab.duke.edu


## Keep it Updated
- As your software or API evolves, update the developer guide to reflect any changes, new features, or deprecated functionality. Maintain a version history and provide clear indications of which version the guide corresponds to.