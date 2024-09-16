import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
import random
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    # Create and configure the Flask app
    app = Flask(__name__)

    if test_config is None:
        # Get MongoDB URI and Database Name from environment variables
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/quiz_db')
        mongo_db_name = os.getenv('MONGO_DB', 'quiz_db')
        client = MongoClient(mongo_uri)
        db = client[mongo_db_name]
    else:
        # If test config is passed in, use it (e.g., for mocking)
        client = test_config['client']
        db = test_config['db']

    questions_collection = db['questions']

    def get_random_choices(choices, correct_answer):
        incorrect_choices = [choice for choice in choices if choice != correct_answer]
        if len(incorrect_choices) < 3:
            raise ValueError("Not enough incorrect choices")
        
        random_incorrect_choices = random.sample(incorrect_choices, 3)
        all_choices = random_incorrect_choices + [correct_answer]
        random.shuffle(all_choices)
        return all_choices

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.json

        required_fields = ['question', 'answer', 'choices', 'level', 'difficulty', 'category']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields in the request'}), 400

        question = data['question']
        answer = data['answer']
        choices = data['choices']
        level = data['level']
        difficulty = data['difficulty']
        category = data['category']

        if len(choices) < 4:
            return jsonify({'error': 'At least 4 choices are required'}), 400
        if answer not in choices:
            return jsonify({'error': 'The correct answer must be one of the choices'}), 400

        valid_levels = ['grade1', 'grade2', 'grade3']
        valid_difficulties = ['easy', 'average', 'difficult']
        if level not in valid_levels:
            return jsonify({'error': f'Invalid level: {level}. Must be one of {valid_levels}'}), 400
        if difficulty not in valid_difficulties:
            return jsonify({'error': f'Invalid difficulty: {difficulty}. Must be one of {valid_difficulties}'}), 400

        question_data = {
            'question': question,
            'answer': answer,
            'choices': choices,
            'level': level,
            'difficulty': difficulty,
            'category': category
        }

        questions_collection.insert_one(question_data)
        return jsonify({'message': 'Question added successfully'}), 201

    @app.route('/questions', methods=['GET'])
    def get_question():
        level = request.args.get('level')
        difficulty = request.args.get('difficulty')
        category = request.args.get('category')

        query = {}
        if level:
            query['level'] = level
        if difficulty:
            query['difficulty'] = difficulty
        if category:
            query['category'] = category

        question_doc = questions_collection.aggregate([{"$match": query}, {"$sample": {"size": 1}}])
        question_data = next(question_doc, None)

        if not question_data:
            return jsonify({'error': 'No question found'}), 404

        correct_answer = question_data['answer']
        all_choices = get_random_choices(question_data['choices'], correct_answer)

        return jsonify({
            'question': question_data['question'],
            'choices': all_choices
        }), 200

    return app
