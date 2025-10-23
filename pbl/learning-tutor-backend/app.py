from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os # Often used for environment variables

# --- 1. DATABASE SETUP ---
# IMPORTANT: Replace the placeholder below with your actual MongoDB Atlas connection string.
# It's best practice to store this in an environment variable for security.
MONGO_URI = os.environ.get('MONGO_URI', "mongodb+srv://admin:aa09ro08@firstcluster.zi5undw.mongodb.net/?retryWrites=true&w=majority&appName=FirstCluster")
client = MongoClient(MONGO_URI)
db = client.learning_tutor # This is your database name
progress_collection = db.progress # This is your collection name for storing user progress

# --- 2. FLASK APP INITIALIZATION ---
app = Flask(__name__)
# Allow your React app (running on localhost:3000) to make requests to this backend.
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# --- 3. IN-MEMORY DATA (will eventually move to database) ---

# Data for the initial 10-question assessment
initial_quiz_questions = [
    {'questionText': 'What is the primary goal of Supervised Learning?','answerOptions': [{'answerText': 'To find hidden patterns in unlabeled data', 'isCorrect': False},{'answerText': 'To make predictions based on labeled data', 'isCorrect': True},{'answerText': 'To learn through trial and error with rewards', 'isCorrect': False},{'answerText': 'To reduce the dimensionality of data', 'isCorrect': False},],},
    {'questionText': 'Which of these is a classification algorithm?','answerOptions': [{'answerText': 'Linear Regression', 'isCorrect': False},{'answerText': 'K-Means Clustering', 'isCorrect': False},{'answerText': 'Logistic Regression', 'isCorrect': True},{'answerText': 'Principal Component Analysis (PCA)', 'isCorrect': False},],},
    {'questionText': 'Overfitting occurs when a model...','answerOptions': [{'answerText': 'Performs well on new, unseen data', 'isCorrect': False},{'answerText': 'Is too simple to capture the data\'s underlying trend', 'isCorrect': False},{'answerText': 'Learns the training data too well, including its noise', 'isCorrect': True},{'answerText': 'Fails to converge during training', 'isCorrect': False},],},
    {'questionText': 'Which task is an example of Unsupervised Learning?','answerOptions': [{'answerText': 'Predicting house prices', 'isCorrect': False},{'answerText': 'Classifying emails as spam or not spam', 'isCorrect': False},{'answerText': 'Customer segmentation based on purchase history', 'isCorrect': True},{'answerText': 'Identifying tumors in medical images', 'isCorrect': False},],},
    {'questionText': 'What does the "K" in K-Nearest Neighbors (KNN) represent?','answerOptions': [{'answerText': 'The number of clusters to create', 'isCorrect': False},{'answerText': 'The number of features in the dataset', 'isCorrect': False},{'answerText': 'The number of neighboring points to consider for classification', 'isCorrect': True},{'answerText': 'A constant learning rate', 'isCorrect': False},],},
    {'questionText': 'A "hyperparameter" is a parameter that is...','answerOptions': [{'answerText': 'Learned by the model during training', 'isCorrect': False},{'answerText': 'Set before the training process begins', 'isCorrect': True},{'answerText': 'The output prediction of the model', 'isCorrect': False},{'answerText': 'Automatically adjusted by the dataset', 'isCorrect': False},],},
    {'questionText': 'What is a common metric for evaluating a regression model?','answerOptions': [{'answerText': 'Accuracy', 'isCorrect': False},{'answerText': 'Precision', 'isCorrect': False},{'answerText': 'Mean Squared Error (MSE)', 'isCorrect': True},{'answerText': 'F1-Score', 'isCorrect': False},],},
    {'questionText': 'What is the purpose of a validation set?','answerOptions': [{'answerText': 'To train the final model', 'isCorrect': False},{'answerText': 'To tune the model\'s hyperparameters', 'isCorrect': True},{'answerText': 'To provide a final, unbiased evaluation of the model', 'isCorrect': False},{'answerText': 'To pre-process the raw data', 'isCorrect': False},],},
    {'questionText': 'Reinforcement Learning is a type of machine learning where an agent learns by...','answerOptions': [{'answerText': 'Studying labeled examples', 'isCorrect': False},{'answerText': 'Finding clusters in data', 'isCorrect': False},{'answerText': 'Interacting with an environment and receiving rewards or penalties', 'isCorrect': True},{'answerText': 'Memorizing the entire dataset', 'isCorrect': False},],},
    {'questionText': 'Which of the following is NOT a deep learning framework?','answerOptions': [{'answerText': 'TensorFlow', 'isCorrect': False},{'answerText': 'PyTorch', 'isCorrect': False},{'answerText': 'Scikit-learn', 'isCorrect': True},{'answerText': 'Keras', 'isCorrect': False},],},
]

# Full question bank for adaptive practice tests
# NOTE: In a real application, this would also be stored in the database.
question_bank = [
    {'difficulty': 'Beginner', 'questionText': 'What does AI stand for?', 'answerOptions': [{'answerText': 'Artificial Intelligence', 'isCorrect': True}, {'answerText': 'Automated Interaction', 'isCorrect': False}]},
    {'difficulty': 'Beginner', 'questionText': 'Is Python a common programming language for ML?', 'answerOptions': [{'answerText': 'Yes', 'isCorrect': True}, {'answerText': 'No', 'isCorrect': False}]},
    {'difficulty': 'Beginner', 'questionText': 'What is "data" in the context of ML?', 'answerOptions': [{'answerText': 'Information used to train or test a model', 'isCorrect': True}, {'answerText': 'The programming language used', 'isCorrect': False}]},
    {'difficulty': 'Beginner', 'questionText': 'Which is an example of a task AI is used for?', 'answerOptions': [{'answerText': 'Recommending a movie', 'isCorrect': True}, {'answerText': 'Storing a file', 'isCorrect': False}]},
    {'difficulty': 'Beginner', 'questionText': 'What does "training" a model mean?', 'answerOptions': [{'answerText': 'The process of teaching a model by showing it examples', 'isCorrect': True}, {'answerText': 'Writing the code for the model', 'isCorrect': False}]},
    {'difficulty': 'Intermediate', 'questionText': 'What is the main difference between classification and regression?', 'answerOptions': [{'answerText': 'Classification predicts a category, regression predicts a number', 'isCorrect': True}, {'answerText': 'Classification uses neural networks, regression does not', 'isCorrect': False}]},
    {'difficulty': 'Intermediate', 'questionText': 'What is "feature engineering"?', 'answerOptions': [{'answerText': 'Creating new input variables from existing ones to improve a model', 'isCorrect': True}, {'answerText': 'A type of neural network architecture', 'isCorrect': False}]},
    {'difficulty': 'Intermediate', 'questionText': 'What does it mean if a model is "overfitting"?', 'answerOptions': [{'answerText': 'It performs very well on training data but poorly on new data', 'isCorrect': True}, {'answerText': 'It is too simple to learn from the data', 'isCorrect': False}]},
    {'difficulty': 'Intermediate', 'questionText': 'What is a "confusion matrix" used for?', 'answerOptions': [{'answerText': 'To evaluate the performance of a classification model', 'isCorrect': True}, {'answerText': 'To calculate the speed of a regression model', 'isCorrect': False}]},
    {'difficulty': 'Intermediate', 'questionText': 'What is a "learning rate"?', 'answerOptions': [{'answerText': 'A hyperparameter that controls how much to change the model in response to estimated error', 'isCorrect': True}, {'answerText': 'The speed of the computer\'s processor', 'isCorrect': False}]},
    {'difficulty': 'Advanced', 'questionText': 'What is the "vanishing gradient" problem in deep neural networks?', 'answerOptions': [{'answerText': 'Gradients become very small, preventing deep networks from training effectively', 'isCorrect': True}, {'answerText': 'The model overfits to the validation data', 'isCorrect': False}]},
    {'difficulty': 'Advanced', 'questionText': 'In RL, what is the difference between "on-policy" and "off-policy" learning?', 'answerOptions': [{'answerText': 'On-policy learns from the agent\'s current actions; off-policy can learn from past or others\' actions', 'isCorrect': True}, {'answerText': 'On-policy is for games, off-policy is for robotics', 'isCorrect': False}]},
    {'difficulty': 'Advanced', 'questionText': 'What is the main function of an "activation function" in a neural network?', 'answerOptions': [{'answerText': 'To introduce non-linearity into the model', 'isCorrect': True}, {'answerText': 'To normalize the input data', 'isCorrect': False}]},
    {'difficulty': 'Advanced', 'questionText': 'What kind of problem are Generative Adversarial Networks (GANs) typically used for?', 'answerOptions': [{'answerText': 'Generating new, synthetic data that resembles a known dataset', 'isCorrect': True}, {'answerText': 'Classifying text into different categories', 'isCorrect': False}]},
    {'difficulty': 'Advanced', 'questionText': 'What is "transfer learning"?', 'answerOptions': [{'answerText': 'Reusing a pre-trained model on a new, related problem', 'isCorrect': True}, {'answerText': 'Transferring data between servers', 'isCorrect': False}]},
]


# --- 4. API ENDPOINTS ---

@app.route('/api/questions/initial', methods=['GET'])
def get_initial_questions():
    """Serves the fixed set of 10 initial assessment questions."""
    return jsonify(initial_quiz_questions)

@app.route('/api/questions/practice/<level>', methods=['GET'])
def get_practice_questions(level):
    """Serves practice questions filtered by the requested difficulty level."""
    valid_levels = ['Beginner', 'Intermediate', 'Advanced']
    if level not in valid_levels:
        return jsonify({'status': 'error', 'message': f'Invalid level. Choose from {valid_levels}'}), 400
        
    filtered_questions = [q for q in question_bank if q.get('difficulty') == level]
    
    return jsonify(filtered_questions)

@app.route('/api/progress', methods=['POST'])
def submit_progress():
    """Receives quiz results from the frontend and saves them to the database."""
    try:
        user_data = request.get_json()
        
        # Simple validation
        if not all(key in user_data for key in ['userId', 'score', 'totalQuestions', 'level']):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Insert the submitted data into the MongoDB collection
        result = progress_collection.insert_one(user_data)
        
        return jsonify({'status': 'success', 'message': 'Progress saved successfully', 'inserted_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# --- 5. RUN THE APP ---
if __name__ == '__main__':
    # The server will run on http://localhost:5000
    app.run(debug=True, port=5000)