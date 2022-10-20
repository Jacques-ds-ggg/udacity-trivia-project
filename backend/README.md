# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
# For Linux Terminal:
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
# Head back to frontend and run npm start to start the frontend on your local browser
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

## API EndPoint Documentation

### Create a new Category

`POST '/api/v0.1.0/categories'`

Creates a new category with the name specified in the category property of the body request

- Request Arguments: None
- Request Body Properties: category- type string
- Returns: An object with the following properties:
  - `status_code`: HTTP status code
  - `success`: A boolean representing the status of the result of the request.
  - `message`: A message describing the result of the request

Example Response:

```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

### Get Categories

`GET '/api/v0.1.0/categories'`

Fetches a dictionary of categories in which the keys are the IDs and the value is the corresponding string of the category. If the request argument `quiz` is set to `true`, then only categories that have questions assigned to them are returned, else by default all categories are returned.

- Request Arguments: quiz- type boolean, default false
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `categories`: An object of `id: category_string` key: value pairs

Example Response:

```json
{
  "success": true,
  "categories": {}
}
```

### Get Questions

`GET '/api/v0.1.0/questions'`

Fetches a list of dictionaries with the questions information, including the list of categories, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Returns: An object with five keys:
  - `success`: A boolean representing the status of the result of the request.
  - `questions`: An array of objects with the following properties:
    - `id`: The ID of the question
    - `question`: The question
    - `answer`: The answer
    - `category`: The ID of category of the question
    - `difficulty`: An integer indicating the difficulty of the question
    - `rating`: An integer indicating the rating of the question
  - `total_questions`: An integer of the total number of questions
  - `categories`: An object of `id: category_string` key: value pairs
  - `current_category`: Two

Example Response:

```json
{
  "success": true,
  "questions": [],
  "total_questions": 4,
  "categories": {},
  "current_category": 2
}
```

### Search Questions

`POST '/api/v0.1.0/questions'`

Fetches a list of dictionaries with the questions information that match the search value, a count of all the questions returned, and the current category.

- Request Arguments: page- type int
- Request Body Properties: search_term- type string
- Returns: An object with five keys:
  - `success` A boolean representing the status of the result of the request.
  - `questions`: An array of objects with the following properties:
    - `id`: The ID of the question
    - `question`: The question
    - `answer`: The answer
    - `category`: The ID of category of the question
    - `difficulty`: An integer indicating the difficulty of the question
    - `rating`: An integer indicating the rating of the question
  - `total_questions`: An integer of the total number of questions
  - `current_category`: One

Example Response:

```json
{
  "success": true,
  "questions": [],
  "total_questions": 3,
  "current_category": 1
}
```

### Delete Question

`DELETE '/api/v0.1.0/questions/<int:id>'`

Deletes a question

- Request Arguments: None
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `deleted_id`: A integer representing the ID of the deleted question

Example Response:

```json
{
  "success": true,
  "deleted_id": 2,
}
```

### Create a new Question

`POST '/api/v0.1.0/questions'`

Creates a new question

- Request Arguments: None
- Request Body Properties:
  - `question`: The question
  - `answer`: The answer
  - `category`: The ID of category of the question
  - `difficulty`: An integer indicating the difficulty of the question
  - `rating`: An integer indicating the rating of the question
- Returns: An object with the following properties:
  - `status_code`: HTTP status code
  - `success`: A boolean representing the status of the result of the request.
  - `message`: A message describing the result of the request
  
Example Response:

```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

### Load Quizzes

`POST '/api/v0.1.0/quizzes'`

Fetches a single question for the quiz on the condition that the question's ID does not already exist among the previous questions' IDs coming from the client.

- Request Arguments: None
- Request Body Properties:
  - `quiz_category`: An object with an `id` key that contains an integer indicating the category of the question to be returned
  - `previous_questions`: A list IDs of the previous questions accepted by the client
- Returns: An object with the following property:
  - `success`: A boolean representing the status of the result of the request.
  - `question`: An object with the following properties:
    - `id`: The ID of the question
    - `question`: The question
    - `answer`: The answer
    - `category`: The ID of category of the question
    - `difficulty`: An integer indicating the difficulty of the question
    - `rating`: An integer indicating the rating of the question

Example Response:

```json
{
  "success": true,
  "question": {},
}
```

## Errors

The following are the mostly likely errors that can occur when making requests:

### Page not Found

This means that no result could be found for the requested resource.

```json
{
  "success": false,
  "error": 404,
  "message": "Page not found",
}
```

### Bad Request

This could be as a result of passing:

- Empty or incomplete body parameters
- Invalid type of data

```json
{
  "success": false,
  "error": 400,
  "message": "bad request",
}
```


### Method not Allowed

This is because no endpoint is specified for the specified method of request

```json
{
  "success": false,
  "error": 405,
  "message": "method not allowed"
}
```

### Unprocessable Action

This indicates that a request passed an empty value.

Example Request Body:

```json
{
  "username": ""
}
```

Example Response:

```json
{
  "success": false,
  "error": 422,
  "message": "Unable to process",
}
```

### Internal Server error

This indicates that the server encountered an error on attempt to process the request.
> _Notice_: If this is encountered, please create an issue on this repo and give a detailed description of events leading up to the error.

Example Response:

```json
{
  "success": false,
  "error": 500,
  "message": "internal server error"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
