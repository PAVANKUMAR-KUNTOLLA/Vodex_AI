# FastAPI CRUD Application

This FastAPI application performs CRUD (Create, Read, Update, Delete) operations for two entities: Items and User Clock-In Records. It provides a total of 10 APIs for managing these entities, including filter options and a MongoDB aggregation.

## Table of Contents

- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Items API](#items-api)
  - [Clock-In Records API](#clock-in-records-api)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/PAVANKUMAR-KUNTOLLA/Vodex_AI_ASSIGNEMENT.git
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your MongoDB database:
   - Use MongoDB Atlas or a local MongoDB instance
   - Update the database connection string in `.env`

5. Create a `.env` file in the root directory and add your environment variables:
   ```
   DATABASE_URL=your_mongodb_connection_string
   USERNAME = username
   PASSWORD = password
   ```

## Running the Application

To run the application locally:

```
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`. You can access the Swagger documentation at `http://localhost:8000/docs`.

## API Endpoints

### Items API

#### Create a new item
- **POST** `/items`
- Input: Name, Email, Item Name, Quantity, Expiry Date (YYYY-MM-DD)
- The Insert Date is automatically added when the item is created

#### Retrieve an item by ID
- **GET** `/items/{id}`

#### Filter items
- **GET** `/items/filter`
- Query Parameters:
  - `email`: Filter by exact email match
  - `expiry_date`: Filter items expiring after the provided date
  - `insert_date`: Filter items inserted after the provided date
  - `quantity`: Filter items with quantity greater than or equal to the provided number

#### Aggregate item count by email
- **GET** `/items/aggregate`
- Returns the count of items for each email (grouped by email)

#### Delete an item
- **DELETE** `/items/{id}`

#### Update an item
- **PUT** `/items/{id}`
- Updates item details (excluding the Insert Date)

### Clock-In Records API

#### Create a new clock-in entry
- **POST** `/clock-in`
- Input: Email, Location
- The Insert DateTime is automatically added during clock-in

#### Retrieve a clock-in record by ID
- **GET** `/clock-in/{id}`

#### Filter clock-in records
- **GET** `/clock-in/filter`
- Query Parameters:
  - `email`: Filter by exact email match
  - `location`: Filter by exact location match
  - `insert_datetime`: Filter clock-ins after the provided date

#### Delete a clock-in record
- **DELETE** `/clock-in/{id}`

#### Update a clock-in record
- **PUT** `/clock-in/{id}`
- Updates clock-in record details (excluding Insert DateTime)

## Technologies Used

- FastAPI
- MongoDB
- Python 3.7+
- Pydantic for data validation
- Motor for asynchronous MongoDB operations
