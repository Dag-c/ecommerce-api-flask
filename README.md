# 🛒 E-commerce API with Flask

A backend RESTful API for an e-commerce platform built with Flask, PostgreSQL, Redis, Docker, and Gunicorn. This project is designed to serve as a scalable and modular solution for online shopping platforms. It includes user, product, and order management, logging, and testing.

RESTful API with Flask and Flask-RESTful. Modular architecture (app/routes, app/services, app/utils). PostgreSQL integration with SQLAlchemy. Redis for caching. Nginx as a reverse proxy. Gunicorn for production-ready WSGI. Docker + Docker Compose setup. Centralized logging. Environment variable support with .env. Unit and integration tests with pytest.
## Features

- ✅ User registration with roles (buyer, seller, admin)

- 🔐 Login with JWT Authentication

- 🛒 Product management by vendors

- 🧾 Consumption of token-protected endpoints

- 📦 Product visualization and creation

- 📁 Modular structure with Blueprints in Flask

- 🐘 PostgreSQL database connected with SQLAlchemy

- 🐳 Docker-ready configuration and deployment on AWS EC2

- 📜 Custom data validation and error handling

- 🌐 Automatic documentation with Swagger / Flasgger
## Tech Stack

**Server:**  
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
- ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)  
- ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)  
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)  
- ![Redis](https://img.shields.io/badge/Redis-D92C2C?style=for-the-badge&logo=redis&logoColor=white)  
- ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)  

**Deployment:**  
- ![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)  
- ![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)  

**Documentation:**  
- ![Flasgger](https://img.shields.io/badge/Flasgger-FF7043?style=for-the-badge&logo=flask&logoColor=white)  

**Testing:**  
- ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
## 🚀 Installation

To run this project locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows use: venv\Scripts\activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a .env file in the root directory and add your environment variables. 
**Example**:
```env
POSTGRES_USER_DEVELOPMENT=your-development_postgres_user
POSTGRES_PASSWORD_DEVELOPMENT=your-development_postgres_password
POSTGRES_HOST_DEVELOPMENT=localhost
POSTGRES_DB_DEVELOPMENT=ecommerce
POSTGRES_USER_PRODUCTION=your-production_postgres_user
POSTGRES_PASSWORD_PRODUCTION=your-production_postgres_password
POSTGRES_HOST_PRODUCTION=your-production-host
POSTGRES_DB_PRODUCTION=ecommerce
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY=your-SECRET_KEY
REDIS_URL_DEVELOPMENT=redis://localhost:6379
REDIS_URL_PRODUCTION=redis://redis:6379
```

### 5. Start the app

```bash
flask run
```
Or if using Docker:

```bash
docker-compose up --build
```
## 🌱 Environment Variables

This project uses a **.env** file to manage environment variables for both development and production. These variables are loaded automatically when running the app locally or inside Docker containers via docker-compose.

Below is a list of required environment variables and their purpose:

| Variable	                       | Description	                                  | Development Example	    | Production Example |
|:--------------------------------|:----------------------------------------------|:------------------------|:-------------------|
| POSTGRES_USER_DEVELOPMENT       | 	PostgreSQL username for development          | 	dev_user	              | -                  |
| POSTGRES_PASSWORD_DEVELOPMENT   | 	PostgreSQL password for development          | 	dev_password	          | -                  |
| POSTGRES_HOST_DEVELOPMENT       | 	Database host for development	               | localhost	              | -                  |
| POSTGRES_DB_DEVELOPMENT         | 	Database name for development	               | ecommerce	              | -                  |
| POSTGRES_USER_PRODUCTION	       | PostgreSQL username for production	           | -	                      | prod_user          |
| POSTGRES_PASSWORD_PRODUCTION	   | PostgreSQL password for production	           | -	                      | prod_password      |
| POSTGRES_HOST_PRODUCTION	       | Database host for production	                 | -	                      | your-db-host.com   |
| POSTGRES_DB_PRODUCTION	         | Database name for production	                 | -	                      | ecommerce          |
| SQLALCHEMY_TRACK_MODIFICATIONS	 | Disables modification tracking in SQLAlchemy	 | False	                  | False              |
| SECRET_KEY	                     | Secret key for sessions and security	         | your-secret-key	        | your-secret-key    |
| REDIS_URL_DEVELOPMENT	          | Redis URL used in development	                | redis://localhost:6379	 | -                  |
| REDIS_URL_PRODUCTION	           | Redis URL used in production	                 | -	                      | redis://redis:6379 |

⚠️ **Note**: When using Docker Compose, these variables are injected from the .env file at container startup.
### 🚀 Usage
Learn how to run and interact with the project in both development and production environments.

**🧪 Development**
To run the project locally:

*Redis is required.*

If you're using Windows, Redis doesn't run natively — you’ll need to start a Redis container:

```
bash
docker run -d -p 6379:6379 --name redis redis
```
Start the Flask app.
You can run it normally with Flask or use Docker Compose.

*Access the API:*

http://localhost:5000

*Explore the Swagger UI:*

http://localhost:5000/apidocs/

💡 Make sure your .env file has the development variables set correctly!

**🚢 Production (Docker + Nginx)**

When deployed with Docker Compose, the app is containerized and runs behind Nginx, which acts as the only public entry point.

Public access is via port 80, not 5000:

http://your-server-ip/

Nginx forwards requests to the Flask API container internally.

Environment variables are injected from the .env file.

**🧱 Architecture Overview**
```
          [ Client (Browser/Postman) ]
                       |
                       v
               ┌───────────────┐
               │    NGINX      │  ← Exposes port 80
               └──────┬────────┘
                      |
                      v
           ┌────────────────────┐
           │   Flask API (Gunicorn) │
           └──────┬─────────────┘
                  |         |
          ┌───────┘         └────────────┐
          v                              v
 [ PostgreSQL Container ]       [ Redis Container ]
```
🔹 All services run in isolated Docker containers.

🔹 Requests flow through NGINX to the API.

🔹 The API communicates with PostgreSQL for data and Redis for caching/session handling.

## 📚 API Endpoints

The full API documentation is available through the interactive Swagger UI:

- Development: [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)
- Production: [http://your-domain.com/apidocs/](http://your-domain.com/apidocs/)

### 📋 Summary of Main Endpoints

| Resource     | Method | Endpoint                  | Description                    |
|--------------|--------|---------------------------|--------------------------------|
| Auth         | POST   | `/login`           | Login and receive JWT          |
| Users         | POST   | `/users`        | Register a new user            |
| Users        | GET    | `/users`           | Get all users (admin only)     |
| Users        | GET    | `/users/<id>`      | Get a single user by ID        |
| Users        | PATCH    | `/users/<id>`      | Update user info               |
| Users        | DELETE | `/users/<id>`      | Delete a user                  |
| Products     | GET    | `/products`        | Get all products               |
| Products     | POST   | `/products`        | Create a new product (admin)   |
| Products     | GET    | `/products/<id>`   | Get product by ID              |
| Products     | PATCH    | `/products/<id>`   | Update product (admin)         |
| Products     | DELETE | `/products/<id>`   | Delete product (admin)         |
| Orders       | GET    | `/orders`          | Get all orders (admin/user)    |
| Orders       | POST   | `/orders`          | Create a new order             |
| Orders       | GET    | `/orders/<id>`     | Get order by ID                |

> 🔍 More detailed documentation with request/response schemas is available in the Swagger UI.

---

## 🔐 Authentication

This API uses JWT-based authentication.

1. Send a `POST` request to `/login` with valid credentials.

2. The response includes an `token`:

```
json
{
  "token": "your.jwt.token"
}
```

For protected endpoints, include this token in your headers:

Authorization: Bearer your.jwt.token

### 🧪 Example Requests

Login and get JWT token

```bash
curl -X POST http://localhost:5000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "123456"}'
```
Get all products (public)
```
curl http://localhost:5000/products
```
Create a new order (requires token)
```
curl -X POST http://localhost:5000/orders \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```
🧪 For more examples, visit /apidocs/ and try them out directly.
### 🗃️ Database Schema
The database schema defines the structure of the main entities used in the e-commerce platform, including users, products, orders, and relationships between them.

You can visualize the full schema below:


[Database Schema](docs/schema_ecommerce_db.png)

This schema was generated using pgAdmin 4 and reflects the current design used in the application.

📌 Key Entities:
- Users: Stores registered users and authentication data.

- Products: Items available for sale, including price and stock.

- Orders: Represents customer purchases and links to products.

- OrderDetails: Association table between orders and products (many-to-many).
### 🧪 Testing

This project uses pytest to run automated tests.
Tests are executed in an isolated environment using an in-memory SQLite database to avoid affecting development or production data.

✅ Test Environment Setup
The create_app(config) function accepts a custom configuration object.
During testing, a configuration is passed to enable testing mode and switch the database to an in-memory instance:

```
python
config.TESTING = True
config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
config.RATELIMIT_ENABLED = False
```

This ensures:

- Tests run in isolation.

- The production (PostgreSQL) database is not modified.

- Redis can be mocked or redirected to a separate instance if needed.

**🚀 Running Tests**

To run all tests in the project:

```bash
pytest -v
```
The pytest.ini file is already configured to ignore unnecessary warnings and provide clean output.

**✅ Test Results**

Example output from a successful test run:

```arduino
collected 27 items

tests/test_orders_endpoint.py::test_create_order_success PASSED
tests/test_orders_endpoint.py::test_create_order_missing_fields PASSED
...
tests/test_users_endpoint.py::test_delete_user_invalid_token PASSED

============================= 27 passed in 16.75s =============================
```
### 🐳 Docker / Deployment

This project is fully containerized using Docker and Docker Compose. It includes four main services:

- PostgreSQL: Database service using the official PostgreSQL 14 image.

- Redis: For caching and session management.

- Flask API: Your custom API service built from a local Dockerfile.

- Nginx: As a reverse proxy to route traffic to the API.

**📦 Requirements**

- Docker installed

- Docker Compose installed

- (For deployment on EC2) SSH access and scp or rsync to transfer files

**🚀 Run Locally**

To start the project locally using Docker Compose:

```
bash
git clone https://github.com/your-user/ecommerce-api.git
cd ecommerce-api

# Create a .env file based on your environment variables

cp .env.example .env

# Run the services

docker-compose up -d --build
```

Once running, the application should be accessible via:
http://localhost

**☁️ Deploying on AWS EC2**

To deploy the application on an AWS EC2 instance (Ubuntu):

Transfer your project to the EC2 instance

Replace your-ec2-ip with your actual IP address:
```
bash

scp -r ./ecommerce-api ubuntu@your-ec2-ip:/home/ubuntu/
SSH into the instance:
```
```
bash

ssh ubuntu@your-ec2-ip
Install Docker and Docker Compose if not already installed:
```
```
bash

sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
```
Navigate to your project directory and run:
```
bash

cd ecommerce-api
docker-compose up -d --build
```
Ensure your EC2 security group allows inbound traffic on port 80 (for Nginx).
## Troubleshooting – Common Issues

### 1. Cannot connect to the database
- **Issue**: Error when trying to connect to PostgreSQL.
- **Solution**: Make sure the environment variables `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_DB` are correctly set in the `.env` file. If you're working locally, verify that the PostgreSQL container is running.

### 2. Redis not working
- **Issue**: Redis is unavailable or shows connection errors.
- **Solution**: Check that the Redis service is running in Docker by using the `docker ps` command. If it's not running, try restarting the Redis container with `docker-compose restart redis`.

### 3. API container fails to start
- **Issue**: The API container stops after attempting to start.
- **Solution**: Check the logs of the container with `docker logs ecommerce-api` for more details. Ensure that all required environment variables are defined and that the database and Redis dependencies are ready.

## Contributing – How to Contribute

Thanks for your interest in contributing to this project!

1. **Fork the repository**: Fork the repository to make changes without affecting the main branch.
2. **Create a branch**: Create a new branch for the feature you're adding or the bug you're fixing. Example: `git checkout -b feature/new-feature`.
3. **Make your changes**: Implement the necessary modifications, following the project's coding best practices.
4. **Write tests**: If you've fixed a bug or added a feature, make sure to write tests to validate your changes.
5. **Submit a Pull Request**: When you're done, open a pull request describing what you've done. Be sure to follow the format of other pull requests where possible.



## License – License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


## Author / Contact – Author / Contact

**Author**: Diego Armando Guillen de la Cruz  
**Email**: diego.guillen.d.cruz@gmail.com  
**Portfolio**: [Your Portfolio](https://yourportfolio.com)
