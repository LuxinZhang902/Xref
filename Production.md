# Xref Project Deployment Documentation
 Version 1, June.28, 2023
    
## Introduction
1. Brief Overview: A web application that finds a student with related information quickly for professors to refer to.
    
2. The target environment: Xref Project will be deployed through the product server(Nginx, Gunicorn). 
    


## Prerequisites
```python    
 source ./env/bin/activate
 ```
* Python: 3.8.10 
    
* Command-line interface (CLI) tool: psql (PostgreSQL) 12.15 (Ubuntu 12.15-0ubuntu0.20.04.1)
    
* Django: >=4.2.2
    
* Nodejs: >=v18.16.0
    
* Nginx version: nginx/1.18.0 (Ubuntu)
    
* Gunicorn: (version 20.1.0)
    
* Npm: 9.7.2

    
##  Start Steps
```python
sudo chown $USER /var/run/docker.sock
docker-compose -f docker-compose-dev.yaml up --build # Distinguish from the Development one

# About the certification, run in a separate terminal
# --dry-run after /var/www/certbot is testing
# https://mindsers.blog/post/https-using-nginx-certbot-docker/
docker-compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d xref.colab.duke.edu

# To renew a certificate
docker compose run --rm certbot renew

# http authenciation
xref:xref-super-secret
```

## Testing
- Provide instructions on how to verify that the deployment was successful.
- Include any test cases or scenarios that should be performed to ensure the project is working as expected.
    

## Troubleshooting
- List common issues that may arise during deployment and possible solutions.
- Provide links to relevant documentation or resources for further troubleshooting.

### Latest Version - Updating Nodejs
```python
# remove
sudo apt-get remove nodejs
    
# install
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs
```

## Additional Notes
- Include any additional information or considerations specific to the project's deployment.
- Mention any post-deployment tasks or ongoing maintenance requirements.
    

## Conclusion
- Summarize the key points covered in the deployment documentation.
- Encourage users to reach out for further assistance or support if needed.