import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.question_string = {

            "question": "What is the colour of magic?",
            "answer": "Rainbow",
            "category": 2,
            "difficulty": 2

        }

        self.search_string = {

            "search": "What is the colour of magic?"

        }

        self.answers = {

            "previous_questions": [20, 22],
            "quiz_category": {
                "id": 3,
                "type": "Arts"
            }

        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def new_test_question(self):
        quest = self.client().post("/questions", json=self.question_string)
        json_load = json.loads(quest.data)

        self.asserEqual(quest.status_code, 200)
        self.assertEqual(json_load["success"], True)
        self.assertEqual(json_load["question"])
        self.assertEqual(json_load["answer"])
        self.assertEqual(json_load["category"])
        self.assertEqual(json_load["difficulty"])

    def test_categories(self):
        quest = self.client().get("/categories")
        json_load = json.loads(quest.data)

        self.assertEqual(quest.status_code, 200)
        self.assertEqual(json_load["success"], True)

    def test_categories_question(self):
        quest = self.client().get("/categories/2/questions")
        json_load = json.loads(quest.data)

        self.assertEqual(quest.status_code, 200)
        self.assertEqual(json_load["success"], True)

    def test_search(self):
        quest = self.client().get("/questions/search", json=self.search_string)
        json_load = json.loads(quest.data)

        self.assertEqual(quest.status_code, 200)
        self.assertEqual(json_load["success"], True)

    def test_quiz(self):
        quest = self.client().get("/quizzes", json=self.answers)
        json_load = json.loads(quest.data)

        self.assertEqual(quest.status_code, 200)
        self.assertEqual(json_load["success"], True)
        self.assertTrue(json_load["question"]["id"] not in self.answers["previous_questions"])

    def test_paginated(self):
        quest = self.client().get("/questions")
        json_load = json.loads(quest.data)

        self.assertEqual(quest.status_code, 200)
        self.assertEqual(json_load["success"], True)
        self.assertTrue(len(json_load["questions"]) <= 10)
        self.assertTrue(json_load["total_question"])
        self.assertTrue(json_load["categories"])

    def test_delete(self):
        quest = self.client().delete("/questions/4")
        json_load = json.loads(quest.data)

        question = Question.query.filter(Question.id == 4)

        self.assertEqual(quest.status_code, 200)
        self.assertEqual(json_load["success"], False)
        self.assertEqual(json_load["deleted"], 4)
        self.assertEqual(question, None)

    def test_404(self):
        quest = self.client().get("/questions?page=200")
        json_load = json.loads(quest.data)

        self.assertEqual(quest.status_code, 404)
        self.assertEqual(json_load["success"], False)
        self.assertEqual(json_load["message"], "page not found")

    def test_422(self):
        quest = self.client().get("/questions?page=200")
        json_load = json.loads(quest.data)

        self.assertEqual(quest.status_code, 422)
        self.assertEqual(json_load["success"], False)
        self.assertEqual(json_load["message"], "not able to complete")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()