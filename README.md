## Wardrobe online

In this app, clothes can be stored and divided into categories, and then chosen based on specific weather conditions. <br>
App created with Python Flask Framework, MySQL databases, JWT, weather API, Docker. For this stage, HTTP requests could be checked in Postman app.

### Docker-compose:

Run: `docker-compose up`

### .env file:

Variables in .env file:<br>
```
SECRET_KEY=""
API_KEY(from URL = https://openweathermap.org/api)=""
lat, lon (longtitude and latitude for city) =  
API_CALL example=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&&lon={lon}&appid={API_KEY}" 
MYSQL_USER="" 
MYSQL_PASSWORD=""
MYSQL_DATABASE=""
MYSQL_HOST=mysql
MYSQL_PORT=3306
```

### mysql.env file:

Variables in mysql.env file:<br>
```
MYSQL_ROOT_PASSWORD=""
MYSQL_ROOT_HOST='%'
MYSQL_USER=""
MYSQL_PASSWORD=""
MYSQL_DATABASE=""
```

#### Function list:
	
|FUNCTION|COMMAND|HTTP REQUEST|		
|--------|-------|------------|
|	register user|/auth/register|POST|
|	login user|/auth/login|POST|
|	list of clothes|/clothes|GET|
|	random clothes|/random|GET|
|	get clothes by id|/id|GET|
|	add clothes|/add|POST|
|	delete clothes|/delete/id|DELETE|
|	all clothes for today's weather|/clothes/all_clothes_by_weather|GET|
|	random clothes from each category for today's weather|/random_clothes_by_weather|GET|


 

#### Resources:
* https://www.redswitches.com/blog/start-mysql-server/ <br>
* https://www.strongdm.com/blog/mysql-create-user-manage-access-privileges-how-to<br>
* https://blog.devart.com/mysql-command-line-client.html<br>
* https://stackoverflow.com/questions/76585758/mysqlclient-cannot-install-via-pip-cannot-find-pkg-config-name-in-ubuntu<br>
* https://phoenixnap.com/kb/how-to-create-a-table-in-mysql<br>
