# esortition
SSE group CW2

1.  Run the application
    ```bash
    docker-compose up
    ```

2. Initialize Flask-Migrate:

    ```bash
    docker-compose exec election_mgmt_service-service flask db init
    docker-compose exec admin_mgmt_service-service flask db init
    ```

2. Generate a migration script:

    ```bash
    docker-compose exec election_mgmt_service-service flask db migrate -m "Initial migration"
    docker-compose exec admin_mgmt_service-service flask db migrate -m "Initial migration"
    ```

3. Apply the migration to create database tables:

    ```bash
    docker-compose exec election_mgmt_service-service flask db upgrade
    docker-compose exec admin_mgmt_service-service flask db upgrade
    ```