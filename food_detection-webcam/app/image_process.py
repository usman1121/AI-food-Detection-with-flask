from flask import Blueprint,session,jsonify,request
from PIL import Image
import time
from io import BytesIO
import base64
import sqlite3
import google.generativeai as genai
model = genai.GenerativeModel('gemini-1.5-flash')
procees_image = Blueprint("image_process", __name__)

def predict_food_type(image):
    """Use Gemini AI for image understanding with detailed performance tracking."""
    
    total_start_time = time.time()  # Start overall execution time
 
    image_start_time = time.time()
    
    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # Convert to PNG format
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    image_processing_time = round((time.time() - image_start_time) * 1000, 2)  # Milliseconds

    # Start inference timing
    inference_start_time = time.time()

    try:
        response = model.generate_content([
            "Analyze this food image and respond in this exact format:",
            "Food Name: [name]",
            "Confidence: [percentage]%",
            "Country of Origin: [country]",
            "Description: [brief description]",
            "Nutrients: [benefit of the food]",
            {"mime_type": "image/png", "data": img_str}  # Properly formatted image
        ])

        inference_time = round((time.time() - inference_start_time) * 1000, 2)  # Milliseconds

        # Measure total execution time
        total_execution_time = round((time.time() - total_start_time) * 1000, 2)  # Milliseconds

        # Parse Gemini's response
        parts = response.text.split('\n')

        return {
            'food_type': parts[0].split(': ')[1],
            'confidence': parts[1].split(': ')[1],
            'country': parts[2].split(': ')[1],
            'description': parts[3].split(': ')[1],
            'nutrients': parts[4].split(': ')[1],
            'image_processing_time': image_processing_time,
            'inference_time': inference_time,
            'total_execution_time': total_execution_time
        }

    except Exception as e:
        return {'error': str(e)}
    

# model = genai.GenerativeModel('gemini-1.5-flash')
# def predict_food_type(image):
#     """Use Gemini AI for image understanding"""
#     start_time = time.time() 
#     try:
#         response = model.generate_content([
#             "Analyze this food image and respond in this exact format:",
#             "Food Name: [name]",
#             "Confidence: [percentage]%",
#             "Country of Origin: [country]",
#             "Description: [brief description]",
#             "Nutrients: [benefit of the food]",
#             image
#         ])
        
#         inference_time = round((time.time() - start_time) * 1000, 2)
#         # Parse Gemini's response
#         parts = response.text.split('\n')
#         return {
#             'food_type': parts[0].split(': ')[1],
#             'confidence': parts[1].split(': ')[1],
#             'country': parts[2].split(': ')[1],
#             'description': parts[3].split(': ')[1],
#             'nutrients': parts[4].split(': ')[1],
#             "inference_time": inference_time 
#         }
#     except Exception as e:
#         return {'error': str(e)}


# @procees_image.route('/upload', methods=['POST'])
# def upload_image():
    
#     if "id" not in session:  # Ensure the user is logged in
#         return jsonify({'error': 'You must be logged in to upload images.'}), 401

#     data = request.json
#     if 'image' not in data:
#         return jsonify({'error': 'No image data provided'}), 400

#     image_data = data['image'].split(",")[1] if "," in data['image'] else data['image']
#     image = Image.open(BytesIO(base64.b64decode(image_data)))

#         # Predict food type using Gemini
#     prediction = predict_food_type(image)
#     if 'error' in prediction:
#         return jsonify(prediction), 500

#         # Save prediction to database with the logged-in user's ID
#     conn = sqlite3.connect('predictions.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#             INSERT INTO predictions (food_type, country, confidence, description, nutrients,inference_time, user_id)
#             VALUES (?, ?, ?, ?, ?, ? , ?)
#         ''', (prediction['food_type'], prediction['country'], prediction['confidence'], prediction['description'],
#                prediction['nutrients'] , prediction["inference_time"], session['id']))
#     conn.commit()
#     conn.close()

#     return jsonify(prediction)



# @procees_image.route('/upload-file', methods=['POST'])
# def upload_file():
    
#     if 'file' not in request.files:
#             return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files.get("file")
#     image = Image.open(file)
#         # Predict food type
#     food_type, confidence = predict_food_type(image)
#         # Save prediction to database
#     conn = sqlite3.connect('predictions.db')
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO predictions (food_type, confidence) VALUES (?, ?)', 
#                        (food_type, confidence))
#     conn.commit()
#     conn.close()

#     return jsonify({'food_type': food_type, 'confidence': confidence})

@procees_image.route('/upload', methods=['POST'])
def upload_image():
    
    if "id" not in session:  # Ensure the user is logged in
        return jsonify({'error': 'You must be logged in to upload images.'}), 401

    data = request.json
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    image_data = data['image'].split(",")[1] if "," in data['image'] else data['image']
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image = image.convert("RGB")  # Ensure proper format

    # Predict food type using Gemini
    prediction = predict_food_type(image)
    
    if 'error' in prediction:
        return jsonify(prediction), 500

    # Save prediction to database with the logged-in user's ID
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (food_type, country, confidence, description, nutrients, inference_time, 
                                 image_processing_time, total_execution_time, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (prediction['food_type'], prediction['country'], float(prediction['confidence'].replace('%', '')),
          prediction['description'], prediction['nutrients'], prediction["inference_time"],
          prediction["image_processing_time"], prediction["total_execution_time"], session['id']))
    
    conn.commit()
    conn.close()

    return jsonify(prediction)
