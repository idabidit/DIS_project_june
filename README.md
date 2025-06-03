# DIS_project_june

Pet Tinder!

Create an account, add your pet and search for potential playmates.

## Requirements
[Docker](https://www.docker.com/) installed on your machine.

## How to run
This project is run using a Docker image:
1) Make sure docker is running
2) run the following command in your favorite terminal emulator: docker-compose up --build
*NOTE: Mac user might run into a port conflict. A work-around is to edit the port mapping in the docker-compose.yml file. Example edit is to change it from: '5000:5000' to '5001:5000'*
3) Open the web app in a browser: http://127.0.0.1:5000
*NOTE: If you have changed the port mapping as described above, then you should use the port in your .yml file*
4) You can either create your own account or use one from the sample data (see below)


## Sample data
The web app includes some sample data that you are free to look at.
You can log in using the following credentials:
User: Mikkel
Password: 1234
or
User: Mathilde
Password: 1234
