how to start rbt.py in rabbitMQ file

1. In config.ini please modify these variables below:
- image_upload_folder = ..../rabbitMQ (... is the directory where you save rabbitMQ file)
- logdir = .../projectName
- host, port, user, password, dbname under [database]
- rmq_username, rmq_password under [rabbitMQ] 

2. Installation
- pip3 install mysql-connector-python
- pip3 install s3urls
- pip3 install boto3
- pip3 install image
- pip3 install apache2
***********************************************************
- download aws cli command on your environment. Please visit this link below: 
https://docs.aws.amazon.com/cli/latest/userguide/install-virtualenv.html
- pip3 install awscli --upgrade --user
- Type "aws configure" on terminal (do not include the quote).
The aws will require aws accessKey, secretKey and region. 
**********************************************************
- Download rabbitMQ command. Visit readme.md in rabbitMQ file  
- Add new user and password : rabbitmqctl add_user username password
- Make the user a administrator: rabbitmqctl set_user_tags username administrator
- Set Permission for the user: rabbitmqctl set_permissions -p / username ".*" ".*" ".*" 
See more here: https://www.rabbitmq.com/rabbitmqctl.8.html#User_Management
**********************************************************

3. set up database 
create mysql database: Hostname: localhost, Port: i.e.(3308), Username: (i.e mysql) and Password: (i.e mysql)
query database below: 
use sys; 
create table jsondata(
	uuid varchar(40),
    image_Location varchar(200),
    label_list text,
    detect_text text,
    sentence text,
    file_date varchar(30)
);
 
4. Connecting from virtual machine to database
Running on putty (ubuntu-server), select Change Settings when right click on putty.
Putty Reconfiguration menu would pop up. On your left side, click + on SSH under Connection.
Select Tunnels, fill in your Source port (i.e 3306) and Destination (i.e localhost:3308), then select add and apply. 

5. start rbt.py
Have the index.html and app.py inside Pycharm/frontend/py file running, and then run rbt.py in Pycharm/rabbitMQ file.
