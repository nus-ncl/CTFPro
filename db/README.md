Steps on how to access the database:

With docker installed as well as Dockerfile and ctfpro_dump.sql downloaded, in the same directory open a terminal and build an image by entering the command:
```build -t ctfpro_img:1.0```

With the docker_compose.yml downloaded (also insert password), run the command to start the container:
```docker-compose up```

Open another terminal and run the command below to confirm that the container has started and also to find out the name of the container:
```docker ps```

Access the container by executing an interactive terminal:
```docker exec -it (CONTAINER_NAME) bash```

Once inside, access mysql through the following command:

```mysql -u root -p```

(there will be a prompt to enter password after)

EXTRA
To view the databases, type "show databases;"
To access a database, type "use (database_name);"
To view the tables in the database, type "show tables;"

ALTERNATIVELY 
1. Enter the MySQL shell
```$ mysql -u root -p```
2. Create DB
```mysql> CREATE DATABASE ctfpro;```
3. Exit MySQL shell and import dump
```$ mysql -u root -p ctfpro < ctfpro_dump.sql```