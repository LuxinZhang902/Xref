# Xref Project Deployment Documentation
 Version 2, Auguest.18, 2023
    
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
# Choose EITHER method to start the project
# Inside Docker
docker-compose -f docker-compose-dev.yml up

# Outside Docker
1. Go to ./xref 
run "pythono3 manage.py runserver" # Note whether is python or python3 depends on your python version
2. Go to ./frontend
run "npm install" # for the first time starting this project
run "npm start" # To start the frontent
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
    
###  npm start, then on https://xref.colab.duke.edu/

## Additional Notes
- Include any additional information or considerations specific to the project's deployment.
- Mention any post-deployment tasks or ongoing maintenance requirements.
    

## Conclusion
- Summarize the key points covered in the deployment documentation.
- Encourage users to reach out for further assistance or support if needed.