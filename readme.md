
# San Jose State University
## Senior Project - CMPE 195A/E  Fall 2020 - Spring 2021
## Authors: Tien Pham, Huynh Phan, Nhi Truong, Yenni Lam
## Team mentor: Kevin Nguyen
## Project adviser: Ronald Mak 


### Project Introduction:
Looking at how useful technology can help people overcome challenges in their lives, 
typically the disabilities. The team of engineers are innovating in solutions to make
 everyday tools more accessible for people with disabilities. The engineers team has an 
 approach on creating a vision assistance tool that describes objects and reads text for 
 the convenience of blind and visually impaired users. The purpose of this project is to 
 create an app to make use of an AI service in order to describe images to the blind.
 
 
 ### Set up system environment:
 * apt install
	- python3-pip
	- apache2
		- https://www.digitalocean.com/community/tutorials/how-to-use-apache-http-server-as-reverse-proxy-using-mod_proxy-extension
		/Project-Theia/environment_config_files/readme.md
	1. mysql-server ( set up database)
		- https://www.rabbitmq.com/install-debian.html#apt
		* sudo mysql_secure_installation
	2. rabbitmq-server (set up rabbitMQ )
		- https://www.rabbitmq.com/install-debian.html#apt
		- https://stackoverflow.com/questions/40436425/how-do-i-create-or-add-a-user-to-rabbitmq
* pip packages
	- azure-cognitiveservices-speech
	- mysql-connector-python
	- pika
	- flask flask_cors
	- boto3

Change ownership of /opt/theia/ to user ownership, not root
ln -s /opt/theia/frontend/ /var/www/html

### Install the dependencies for frontend:
* Prerequisite to run on your machine:
  - python 3: pip install flask, flask_cors, pika

* If don't have a web server then need to install Apache/XAMPP

* Pull Git repository

- Install RabbitMQ, create admin user if one doesn't exist
- Configure environment
* Go to frontend_api_server.py and modify:
   - UPLOAD_FOLDER (the location that images are saved after user upload)
   - rmq_server (RabbitMQ server's name or IP Address)
   - rmq_credentials=pika.PlainCredentials (username, password)
* Modify index.html
   - Change the URL in 2 POST requests at xhr.open("POST", URL) to whatever the host IP and Port the API server is running on
* Open the terminal run the API server
   * python3 front_api_server.py
* Install VisualStudio, pull Git res, go to the file index.html, right click, open in default browser
* Try to upload any file or paste image url and the result shown in the terminal
* Prerequisite to run on virtual machine:
   * Set up Ubuntu on a virtual machine.
   * python 3: pip3 install flask, flask_cors, pika
   * Install RabbitMQ, create admin user if one doesn't exist
   * Install Apache on virtual machine: Run all these commands
- a2enmod proxy
- a2enmod proxy_http
- a2enmod proxy_ajp
- a2enmod rewrite
- a2enmod deflate
- a2enmod headers
- a2enmod proxy_balancer
- a2enmod proxy_connect
- a2enmod proxy_html
* Modify this file: /etc/apache2/sites-enabled/000-default.conf

####  Add those to configuration file: 
   * ProxyPreserveHost On
       * ProxyPass /theia/api/v1.0/img_url http://127.0.0.1:5000/theia/api/v1.0/img_url
       * ProxyPassReverse /theia/api/v1.0/img_url http://127.0.0.1:5000/theia/api/v1.0/img_url
       * ProxyPass /theia/api/v1.0/img_path http://127.0.0.1:5000/theia/api/v1.0/img_path
       * ProxyPassReverse /theia/api/v1.0/img_path http://127.0.0.1:5000/theia/api/v1.0/img_path
       * ProxyPass /theia/api/v1.0/get_info http://127.0.0.1:5000/theia/api/v1.0/get_info
       * ProxyPassReverse /theia/api/v1.0/get_info http://127.0.0.1:5000/theia/api/v1.0/get_info

 
* https://www.digitalocean.com/community/tutorials/how-to-use-apache-http-server-as-reverse-proxy-using-mod_proxy-extension.
   * sudo service apache2 restart.
   * Pull Git repository.
   * Copy frontend to virtual machine to /var/www/html.
   * Configure environment in index.html and frontend_.

###Install the dependencies for backend:
- pip3 install mysql-connector-python
- pip3 install s3urls
- pip3 install boto3
- pip3 install image
- pip3 install google_trans_new
______________________________________________
- download aws cli command on your environment. Please visit this link below: https://docs.aws.amazon.com/cli/latest/userguide/install-virtualenv.html
- pip3 install awscli --upgrade --user.
- Type "aws configure" on terminal (do not include the quote). The aws will require aws accessKey, secretKey and region.
______________________________________________
- Download rabbitMQ command. Please look at Set up system environment above:
- Add new user and password : rabbitmqctl add_user username password.
- Make the user an administrator: rabbitmqctl set_user_tags username administrator.
- Set Permission for the user: rabbitmqctl set_permissions -p / username "." "." ".*" See more here: https://www.rabbitmq.com/rabbitmqctl.8.html#User_Management.
_____________________________________________
- set up database create mysql database: Hostname: localhost, Port: i.e.(3308), Username: (i.e mysql) and Password: (i.e mysql) query database below: use sys; create table json data( uuid varchar(40), image_Location varchar(200), label_list text, detect_text text, sentence text, file_date varchar(30) );
 
- Connecting from virtual machine to database Running on putty (ubuntu-server), select Change Settings when right click on putty. Putty Reconfiguration menu would pop up. On your left side, click + on SSH under Connection. Select Tunnels, fill in your Source port (i.e 3306) and Destination (i.e localhost:3308), then select add and apply.
 
- start rbt.py Have the index.html and app.py inside Pycharm/frontend/py file running, and then run rbt.py in Pycharm/rabbitMQ file.

### Our Expectations:
#### Essential/ Functional Requirements
* The user can upload images to the webserver
* The tool should be able to perform image recognition
* The web application should be translate image into text
* Output text and read the output strings to the user(s)

#### Desired/ Non-functional Requirements
* Store user images on the Amazon database  
* Front End : EC2 Server - Amazon Web Services
* Back End: Python
* Database: Amazon S3

#### Optional Requirements
* The user can save to images to the database that the engineer team is hosting
* To design a iOS/Android application for user(s)   

## License

This project is licensed under the MIT License. 2020

