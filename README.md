# DIS_project_june

Pet Tinder!

Create an account, add your pet and search for potential playmates.

## Requirements
[Docker](https://www.docker.com/) installed on your machine.

## How to run
This project is run using a Docker image:
1) Make sure docker is running
2) run command: docker-compose up --build
NOTE: Mac user might run into a port conflict. A work-around is to edit the port mapping in the docker-compose.yml file. Example edit is to change it from: '5000:5000' to '5001:5000'

## Sample data
Copy the contents of insert_data.sql into the bottom of schema.sql prior to building the image in order to populate the database with synthesized users.
Sample data users all have the same password: 1234
