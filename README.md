# eSortition

Welcome to eSortition, a platform designed for managing elections and facilitating voting processes.

## Development Environment

To run the application locally, follow these steps:

1. Create the network for kong:
    ```bash
    docker network create kong-net
    ```

2. Run the application using Docker Compose:
    ```bash
    docker-compose -f dev.docker-compose.yml up
    ```

3. Apply migrations to create database tables:
    ```bash
    docker-compose exec election_mgmt_service-service flask db upgrade
    docker-compose exec admin_mgmt_service-service flask db upgrade
    docker-compose exec voting_manager-service flask db upgrade
    ```

    If you make changes to the database schema, run the following commands to generate and apply migrations:
    ```bash
    docker-compose exec election_mgmt_service-service flask db migrate -m "Initial migration"
    docker-compose exec admin_mgmt_service-service flask db migrate -m "Initial migration"
    ```

## Live Application

Access the live application (email team for access) [https://lobster-app-5oxos.ondigitalocean.app/](https://lobster-app-5oxos.ondigitalocean.app/).

## Stack

The eSortition platform is built using the following technologies and services:

- [Digital Ocean](https://www.digitalocean.com/): Cloud infrastructure provider for hosting the application.
- [Railway](https://railway.app/): Database hosting platform for managing database instances.
- [Azure](https://azure.microsoft.com/): Serverless function provider for handling notifications.
- [GitHub](https://github.com/Diveenaa/esortition): Version control and collaboration platform for the project.
- Other common components include Docker, Flask, PostgreSQL, Kong API Gateway, and more.

## Contributors

Contributions to the project are managed by the following team members:

- Hannah Gillespie (hgg23)
- Edward White (eaw23)
- Diveena Nanthakumaran (dn123)
- Lucian Mac-Fall (ltm23)

## About

eSortition was developed as part of the Software Systems Engineering Coursework 2. It consists of two separate portals: the Admin Portal and the Voting Portal. The Admin Portal facilitates tasks such as election creation and management, while the Voting Portal enables users to cast votes and view election results.

### Frontend Architecture

The two portals are deployed as separate Flask applications, offering flexibility, scalability, and security benefits. The API Gateway, implemented using Kong, serves as the central entry point for handling requests between client apps and backend microservices.

### Backend Microservices

The system comprises several backend microservices, each responsible for specific functions:

- **Admin Management Service**: Handles user authentication for the Admin Portal.
- **Election Management Service**: Manages election details and configurations.
- **Voting Service**: Processes and records votes cast by users during elections.
- **Notification Service**: Sends emails with unique voting links to eligible voters.

These microservices are deployed as Container Instances, providing isolation, scalability, and security.

### Development Choices

Containerization, using Docker and Docker Compose, was adopted to ensure consistency and isolation in development and production environments. Dockerfiles and Docker Compose files were utilized for managing dependencies and orchestrating deployments.

