# Habit Tracker

A Django web application for tracking daily, weekly, or monthly habits. Built as part of my learning journey in an effort to further understand full stack web development.

## Project Structure
```mermaid
graph TD
    A[django-projects] --> B[habit-tracker]
    B --> C[apps]
    B --> D[config]
    B --> E[manage.py]
    B --> F[requirements]
    B --> G[.gitignore]
    B --> H[.env]
    
    C --> I[habits]
    I --> J[migrations]
    I --> K[templates]
    I --> L[static]
    I --> M[__init__.py]
    I --> N[admin.py]
    I --> O[apps.py]
    I --> P[models.py]
    I --> Q[urls.py]
    I --> R[views.py]
    
    D --> S[settings]
    D --> T[urls.py]
    D --> U[wsgi.py]
    D --> V[asgi.py]
    
    S --> W[__init__.py]
    S --> X[base.py]
    S --> Y[local.py]
    S --> Z[production.py]
    
    F --> AA[base.txt]
    F --> BB[local.txt]
    F --> CC[production.txt]
```

## Setup Instructions
1. Clone the repository
2. Create a virtual environment
3. Install necessary dependencies
4. Set up environment variables
5. Run migrations
6. Start the development server

## Features
- User authentication
- Habit tracking
- Data visualization

## Technologies
- Python
- Django
- SQLite3
