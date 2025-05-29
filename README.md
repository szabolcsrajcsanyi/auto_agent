# 🧠 Autonomous Agent System

This repository contains the implementation of an autonomous agent system designed to solve complex tasks by planning, executing, and interacting with simulated external APIs. The system includes a web-based UI and three simulated APIs: Smart Home, Shopping History, and Inventory Management.

## 🚀 Getting Started

### ✅ Prerequisites

To run this project locally, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 🛠 How to Run

1. **Navigate to the project root directory:**

   ```bash
   cd auto_agent/
   ```

1. **Set up your environment variables:**
    Create a **.env** file in the **auto_agent/** directory and add your **OpenAI API key**:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```
    >This key is required for the system to communicate with OpenAI's language model.

2. **Start the system using Docker Compose:**

   ```bash
   docker-compose up --build
    ```

2. **Access the Web UI:**
Open your browser and go to:

   ```bash
   http://localhost
    ```

    > The UI is exposed on port 80, so simply entering localhost is sufficient.

## 🌐 API Documentation

The project includes three APIs for simulation purposes. Their documentation can be accessed via Swagger UI:

| API                      | Localhost URL                    | Docker Network URL                            |
|--------------------------|----------------------------------|-----------------------------------------------|
| Smart Home API           | `http://localhost:8081/api/docs` | `http://smart_home/api/openapi.json`          |
| Shopping History API     | `http://localhost:8082/api/docs` | `http://shopping_history/api/openapi.json`    |
| Inventory Management API | `http://localhost:8083/api/docs` | `http://inventory_management/api/openapi.json`|

> ⚠️ **Important:** When providing an API endpoint to the agent, always use the **Docker network URL** (right column) so the agent inside the Docker container can access the API correctly.
