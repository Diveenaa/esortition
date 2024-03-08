# esortition

SSE group CW2

# need to make distinctions with dev.docker-compose.yml

1.  Run the application
    ```bash
    docker-compose -f dev.docker-compose.yml up
    ```
2.  Apply the migration to create database tables:

    ```bash
    docker-compose exec election_mgmt_service-service flask db upgrade
    docker-compose exec admin_mgmt_service-service flask db upgrade
    docker-compose exec voting_manager-service flask db upgrade
    ```

    IF YOU MAKE DB CHANGES:

    ```bash
    docker-compose exec election_mgmt_service-service flask db migrate -m "Initial migration"
    docker-compose exec admin_mgmt_service-service flask db migrate -m "Initial migration"
    ```
