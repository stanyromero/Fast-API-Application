#!/bin/bash
 
cd ./backend/

echo "building backend"

docker build -t fastapi-backend:1.1 .

docker tag fastapi-backend:1.1 stanromero2003/fastapi-backend:1.1

cd ../

cd ./frontend/

echo "building frontend"

docker build -t fastapi-frontend:1.1 .

docker tag fastapi-frontend:1.1 stanromero2003/fastapi-frontend:1.1

docker push stanromero2003/fastapi-frontend:1.1
docker push stanromero2003/fastapi-backend:1.1


echo "SSH into EC2 machine"

# SSH into the EC2 instance using the provided key pair and IP address
ssh -i /home/stan_romero/AWS-key-pair.pem ubuntu@34.201.173.117 << 'EOF'

echo "Entering the shop-inventory-management folder"

# Change directory to the desired folder where the application will reside
cd shop-inventory-management

# Storing the Docker-Compose configuration in a variable
content=$(cat << 'DOCKER_COMPOSE_EOF'
version: '3.0'

services:
  backend:
    image: stanromero2003/fastapi-backend:1.1
    container_name: inventory_app_backend
    ports:
      - "8000:80"
    networks:
      - inet
    depends_on:
      - postgres_db

  frontend:
    image: stanromero2003/fastapi-frontend:1.1
    container_name: inventory_app_frontend
    ports:
      - "80:80"
    environment:
      - IP_HOST=34.201.173.117
    networks:
      - inet

  postgres_db:
    image: postgres
    container_name: inventory_app_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 1234
      POSTGRES_DB: items_db
    ports:
      - "5432:5432"
    networks:
      - inet

networks:
  inet:
    name: inventory_network
DOCKER_COMPOSE_EOF
)

# Write Docker Compose content to a file
echo "$content" > docker-compose.yml

echo "Content written to docker-compose.yml"

# Execute docker-compose up to deploy the application
docker-compose up

EOF