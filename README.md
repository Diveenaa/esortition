# esortition
SSE group CW2

1. Initialize Flask-Migrate:

    ```bash
    docker-compose run election_mgmt_service-service flask db init
    docker-compose run admin_mgmt_service-service flask db init
    ```

2. Generate a migration script:

    ```bash
    docker-compose run election_mgmt_service-service flask db migrate -m "Initial migration"
    docker-compose run admin_mgmt_service-service flask db migrate -m "Initial migration"
    ```

3. Apply the migration to create database tables:

    ```bash
    docker-compose run election_mgmt_service-service flask db upgrade
    docker-compose run admin_mgmt_service-service flask db upgrade
    ```

4.  Run the application
    ```bash
    docker-compose up
    ```