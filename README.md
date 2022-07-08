# Django Challenge

This project enables an API for managing and searching products and create product ratings.

## Requirements

* Python 3.10.0
* Docker 20.10.16

## How to run it

1. Clone the project
2. Optionally create virtual environment and install dependencies, since app runs in Docker
3. Run `docker-compose up --build`
4. Get inside app container with `docker exec -it shop sh`
5. Create a superuser `python manage.py createsuperuser`
6. Load fixture data for testing the app `python manage.py loaddata products.json`
7. Login with superuser in /admin and create users for testing the ratings functionality

.env file is checked in the repository for convenience, for production purposes 
it would be stored on secured location and pulled on deployment. 

## Usage

### DRF Browsable API

User the browsable api for search and CRUD operations on products and ratings. Interface provides all 
the required forms for mentioned operations.

API runs on port 8000.

Upper right corner in /products contains 'Filters' button with ordering and search functionality.

### ELK

Synced products in Elasticsearch used for enhancing search functionalities are visible on port 5601
in kibana. For more information use official docs.

### API Documentation

OpenAPI documentation is available on /docs endpoint.