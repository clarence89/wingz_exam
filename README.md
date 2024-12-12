# wingz_exam

## How to Run
1. Ensure you have Docker installed on your system.
2. Clone the repository to your local machine at https://github.com/clarence89/wingz_exam.git from https://github.com/clarence89/wingz_exam. 
3. Open a terminal and navigate to the project directory:
   ```bash
   cd wingz_exam
   ```
4. Start the application using Docker Compose:
   ```bash
   docker-compose up
   ```
5. Access the application using this username: `admin` and password: `adminpassword`:
    * Navigating to `http://localhost` or `http://localhost:3000` in your web browser to access NUXT.
    * Navigating to `http://localhost:8000` in your web browser to access Django then Navigating to `http://localhost:8000/swagger` to access Django API Documentation.
    * Navigating to `http://localhost:8081` in your web browser to access PGWEB.



6. The SQL query for the report is:
    ```sql 
        SELECT
            TO_CHAR(r.pickup_time, 'YYYY-MM') AS monthyear,
            CONCAT(u.first_name, ' ', LEFT(u.last_name, 1), '.') AS driver_name,
            COUNT(DISTINCT r.id_ride) AS trip_count -- Count The Rides
        FROM
            rides_ride r
        JOIN
            users_user u ON r.driver_id = u.id
        JOIN
            rides_rideevent re_pickup ON r.id_ride = re_pickup.ride_id AND re_pickup.description = 'Status Changed to pickup'
        JOIN
            rides_rideevent re_dropoff ON r.id_ride = re_dropoff.ride_id AND re_dropoff.description = 'Status Changed to dropoff'

        WHERE
            EXTRACT(EPOCH FROM (re_dropoff.created_at - re_pickup.created_at)) > 3600  -- Filter rides longer than 1 hour
        GROUP BY
            monthyear, driver_name -- Group by Month and Year
        ORDER BY
            monthyear DESC, driver_name;
    ```


` NOTE: I used Docker Compose to run multiple containers in this project. It allows me to easily define and run multi-container Docker applications. It also provides a convenient way to manage the services and their dependencies. In this project, I used Docker Compose to run the Nuxt frontend(with Nuxt UI, Pinia(with Persistent State to handle User Credentials)), Django(simpleJWT/Trench to use JWT for AUTH) backend, Postgres database, PGWEB and CADDY for reverse proxy. It makes it easy for the examiner to run the application on their local machine without having to install and configure all the required services. 
Nuxt UI - For Templating
Pinia For State Management
simpleeJWT/Trench for Authentication
Docker using Multi Container Build - For Ease of Development, Easy Environment Setups, Specially for New Setup OS
`
