import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# 
cors_origin = os.getenv('CORS_ORIGIN')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app,
        origin = '*',
        supports_credentials = True
        )

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','ContentType, Authentication, True','GET, UPDATE, DELETE, PUT, POST, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods = ['GET'])

    def all_categories():
        try:
            categories = Category.query.all()
            data_dict = {
                'success' : True,
                'message' : 'Categories returned successful',
                'categories' : {}
            }
            for category in categories:
                data_dict['categories'][category.id] = category.type
            return jsonify(data_dict)
        except Exception as error:
            print(error)
            abort(422)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods = ['GET'])

    def all_questions():
        try:
            questions = Question.query.order_by(Question.id).paginate(page, QUESTIONS_PER_PAGE)
            current_questions = [question.format() for question in questions.items]
            data_dict = {
                'success': True,
                'message': 'Questions returned successfully.',
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': {}
            }
            categories = Category.query.all()

            if len(categories) > 0:
                for category in categories:
                    data_dict['categories'][category.id] = category.type
            
            return jsonify(data_dict)
        except Exception as error:
            print(error)
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods = ['DELETE'])

    def drop_question(id):          
        question = Question.query.filter(Question.id == question_id).one_or_none()                 
        try:         
            question.delete()
            data_dict = {
                'success': True,
                'message': 'Deleted question successfully',
                'deleted': id
            }
            return jsonify(data_dict)
        except Exception as error:
            print(error)
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods = ['POST'])

    def post_question():
        json_req = request.get_json()
        question = json_req.get('question', None)
        answer = json_req.get('answer', None)
        category = json_req.get('category', None)
        difficulty = json_req.get('difficulty', None)

        try:
            if not question or not answer: abort(422)
            question = Question(
                question = question,
                answer = answer,
                category = category,
                difficulty = difficulty
            )
            question.insert()
            data_dict = {
                'success': True,
                'message': 'Question created successfully.',
                **json_req
            }
            return jsonify({data_dict})
        except Exception as error:
            print(error)
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods = ['POST'])

    def search_question():
        page = request.args.get('page', 1, type = int)
        json_req = request.get_json()
        search = json_req.get("searchTerm", None)

        try:
            questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))).paginate(page, QUESTIONS_PER_PAGE)
            current_questions = [question.format() for question in questions.items]
            data_dict = {
                'success': True,
                'message': 'Questions-search returned successful',
                'questions': current_questions,
                'total_questions': len(questions)
            }

            return jsonify({data_dict})

        except Exception as error:
            print(error)
            abort(422)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions', methods = ['GET'], strict_slashes=False)

    def category_question(id):
        try:
            category_questions = Question.query.filter(Question.category == category_id).all()
            formatted_questions = [question.format() for question in category_questions]
            data_dict = {
                'success': True,
                'message': 'Category questions returned successfully.',
                'questions': formatted_questions,
                'total_questions': len(category_questions),
                'current_category': id,
                'current_category': None
            }
            return jsonify(data_dict)
        except Exception as error:
            print(error)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods = ['POST'])

    def play_quiz():
        json_req = request.get_json()
        previous_questions = json_req.get('previous_questions', [])
        quiz_category = json_req.get('quiz_category', None)        
        data_dict = {
            'success': True,
            'message': 'Quiz question returned successfully.',
        }

        try:
            quiz_question = Question.query.filter(
                and_(
                    Question.category == quiz_category['id'] if quiz_category['id'] else Question.category > 0,
                    Question.id.notin_(previous_questions)
                )).order_by(func.random()).first()            
            if quiz_question: data_dict['question'] = quiz_question.format()
            return jsonify(data_dict)
        except Exception as error:
            print(error)
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return(jsonify({"success": False, "error": 404, "message": "page not found"}),404,)

    @app.errorhandler(422)
    def unable(error):
        return(jsonify({"success": False, "error": 422, "message": "unable to process"}),422,)

    return app