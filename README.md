# esortition

SSE group CW2

1.  Run the application
    ```bash
    docker-compose up
    ```
2.  Apply the migration to create database tables:

    ```bash
    docker-compose exec election_mgmt_service-service flask db upgrade
    docker-compose exec admin_mgmt_service-service flask db upgrade
    docker-compose exec voting_manager-service alembic upgrade head
    ```

    IF YOU MAKE DB CHANGES:

    ```bash
    docker-compose exec election_mgmt_service-service flask db migrate -m "Initial migration"
    docker-compose exec admin_mgmt_service-service flask db migrate -m "Initial migration"
    ```
