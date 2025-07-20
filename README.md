DTS Developer Technical Test Submission - Ciaran McAleer
---
This Fork contains my submission to the original challenge. The backend has been built using python with Flask for simplicity.

## Project Structure
//TODO update when development is complete
```
backend
    __init__.py # This is used to mark the backend directory as a package
    app.py # Set up the database used to store tasks.
    requirements.txt # List of dependencies for the backend
    routes.py # Contains the API endpoints
    schemas.py # Contains the data validation schemas
frontend
```


Challenge Details
```
# DTS Developer Technical Test Submission - Ciaran McAleer

## Objective
To assess your ability to build a simple API and frontend using best coding practices.

## Scenario
HMCTS requires a new system to be developed so caseworkers can keep track of their tasks. Your technical test is to develop that new system so caseworkers can efficiently manage their tasks.

## Task Requirements

### Backend API
The backend should be able to:
- Create a task with the following properties:
  - Title
  - Description (optional field)
  - Status
  - Due date/time
- Retrieve a task by ID
- Retrieve all tasks
- Update the status of a task
- Delete a task

### Frontend Application
The frontend should be able to:
- Create, view, update, and delete tasks
- Display tasks in a user-friendly interface

## Technical Requirements
Here are a few starter repositories if you would like to use our tech stack:
- [Backend Starter Repo](https://github.com/hmcts/hmcts-dev-test-backend)
- [Frontend Starter Repo](https://github.com/hmcts/hmcts-dev-test-frontend)

You can use any language you are comfortable with or our own stack:
- **Backend**: Any language or framework of your choice
- **Frontend**: Any language or framework of your choice
- Implement **unit tests**
- Store data in a **database**
- Include **validation and error handling**
- **Document API endpoints**

## Submission Guidelines
- Create repositories on GitHub and add add the links to your application
- Include a helpful `README.md`!

Happy coding!
```