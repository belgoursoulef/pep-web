ersion: '3.8'

services:
  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: carhorizon
    ports:
      - "5062:3306"
    volumes:
      - ./db:/docker-entrypoint-initdb.d
      - mysql_data:/var/lib/mysql
    networks:
      - internal

  web:
    build: ./web
    restart: always
    ports:
      - "80:5000"   
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=rootpassword
      - DB_NAME=carhorizon
    depends_on:
      - db
    networks:
      - external

volumes:
  mysql_data:

networks:
  internal:
    driver: bridge
