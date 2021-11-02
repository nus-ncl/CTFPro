With docker installed as well as Dockerfile and ctfpro_dump.sql downloaded, build an image by entering the command:
build -t ctfpro_img:1.0

With the docker_compose.yml downloaded, run the command to start the container:
docker-compose up

run the command:
docker ps

Open an interactive terminal to access the SQL Database
docker exec -it (CONTAINER_NAME) bash

