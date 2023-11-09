# Wanderlust Travel Planner

Welcome to the Wanderlust Travel Planner, a Flask-based backend application that empowers users to plan their trips, manage destinations, create itineraries, and track expenses efficiently. Below is a comprehensive guide to understanding and using the key features of this application.

## Overview

Imagine you are tasked with creating a travel planner application called "Wanderlust Travel Planner." This application aims to help users plan their trips, including destinations, itineraries, and budget tracking. Your mission, as an expert Flask developer, is to create a Flask backend application that integrates with a database to provide a seamless travel planning experience.

## Getting Started

Follow the steps below to get started with the Wanderlust Travel Planner:

1. Clone the repository to your local machine.

   ```
   git clone https://github.com/your-username/wanderlust-travel-planner.git
   ```
   ```
   pip install -r requirements.txt
   ```
   ```
    SQLALCHEMY_DATABASE_URI = 'your_database_uri_here'
   ```
  ## Features
### Database Integration
Choose an appropriate database system (e.g., SQLite, PostgreSQL, MySQL) for your Flask application and configure it. Implement data models, relationships, and tables to support the core functionalities of managing destinations, itineraries, and expenses. While Test-Driven Development (TDD) is encouraged, it is optional for this project.

### Destination Management
Develop API endpoints for managing travel destinations. Each destination should have attributes like name, description, and location. Implement CRUD operations for destinations. You may write tests for these operations, but it's not mandatory.

## API Endpoints:

Add destination: ``` [POST] http://localhost:5000/addDestinations ```

Get all destinations: ```[GET] http://localhost:5000/getAlldestinations```

Get destination by id: ```[GET] http://localhost:5000/destinations/{destination_id}```

Update destination by id: ```[PUT] http://localhost:5000/destinations/{destination_id}```

Itinerary Planning
Create API endpoints for planning itineraries. Users should be able to add, update, and delete activities in their itineraries for selected destinations. Optionally, write tests for these endpoints to validate functionality.

## API Endpoints:

Add itineraries: ```[POST] http://localhost:5000/itineraries/{destination_id}/activities```

Update itineraries by destination id: ```[PUT] http://localhost:5000/itineraries/{destination_id}/activities```

Delete itineraries by destination id: ```[DELETE] http://localhost:5000/itineraries/{destination_id}```

Get itinerary by destination id: ```[GET] http://localhost:5000/itineraries/destination/{destination_id}```

## Expense Tracking
Enable users to record and track their expenses related to their trips. Users should be able to add expenses and categorize them. You may choose to implement tests to verify expense recording and categorization.

## API Endpoints:

Add expense to itinerary: ```[POST] http://localhost:5000/itineraries/{itinerary_id}/expenses```

Get all expenses: ```[GET] http://localhost:5000/expenses```

Update expense by itinerary id: ```[PUT] http://localhost:5000/expenses/{expense_id```

Get expense by itinerary id: ```[GET] http://localhost:5000/expenses/itinerary/{itinerary_id}```

Get expense by destination id: ```[GET] http://localhost:5000/expenses/destination/{destination_id}```
