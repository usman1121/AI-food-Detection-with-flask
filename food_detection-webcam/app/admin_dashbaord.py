
# from flask import Blueprint,render_template,session,url_for,redirect
# import sqlite3

# admin = Blueprint("admin", __name__)

# @admin.route('/admin', methods=['GET', 'POST'])
# def admin_dashboard():
#     if session.get('role') != "Admin":
#         return redirect(url_for('login_bp.login'))
    
#     conn = sqlite3.connect('predictions.db')
#     cursor = conn.cursor()

#     # Fetch logs with user names instead of country
#     cursor.execute("""
#         SELECT p.id, p.food_type, u.name, p.confidence, p.timestamp, p.user_id 
#         FROM predictions p
#         JOIN users u ON p.user_id = u.id
#         ORDER BY p.timestamp DESC
#     """)
#     logs = cursor.fetchall()

#     # Calculate statistics
#     cursor.execute("SELECT COUNT(*) FROM predictions")
#     total_predictions = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT food_type, COUNT(food_type) AS count 
#         FROM predictions 
#         GROUP BY food_type 
#         ORDER BY count DESC 
#         LIMIT 1
#     """)
#     most_common_food = cursor.fetchone()
#     most_common_food = most_common_food[0] if most_common_food else "No Data"

#     cursor.execute("SELECT AVG(confidence), AVG(inference_time) FROM predictions")
#     avg_confidence, avg_inference = cursor.fetchone()
#     avg_confidence = round(avg_confidence, 2) if avg_confidence else 0.0
#     avg_inference = round(avg_inference, 2) if avg_inference else 0.0

#     # Get total user count
#     cursor.execute("SELECT COUNT(*) FROM users")
#     total_users = cursor.fetchone()[0]

#     # Prepare data for visualization
#     cursor.execute("""
#         SELECT food_type, COUNT(*) 
#         FROM predictions 
#         GROUP BY food_type 
#         ORDER BY COUNT(*) DESC
#     """)
#     food_stats = cursor.fetchall()

#     food_labels = [row[0] for row in food_stats]  # Extract food types
#     food_data = [row[1] for row in food_stats]    # Extract counts

#     # Get the user who made the most searches
#     cursor.execute("""
#         SELECT u.name, COUNT(p.id) AS prediction_count 
#         FROM predictions p
#         JOIN users u ON p.user_id = u.id 
#         GROUP BY u.id 
#         ORDER BY prediction_count DESC 
#         LIMIT 1
#     """)
#     most_searched = cursor.fetchone()
#     most_searched_name = most_searched[0] if most_searched else "No Data"
#     most_predictions = most_searched[1] if most_searched else "0"

#     conn.close()

#     return render_template(
#         'admin.html',
#         logs=logs,
#         total_predictions=total_predictions,
#         most_common_food=most_common_food,
#         avg_confidence=avg_confidence,
#         avg_inference=avg_inference,
#         total_users=total_users,
#         food_labels=food_labels,
#         food_data=food_data,
#         most_searched=most_searched_name,
#         most_predictions=most_predictions,
#     )
from flask import Blueprint, render_template, session, url_for, redirect
import sqlite3

admin = Blueprint("admin", __name__)

@admin.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('role') != "Admin":
        return redirect(url_for('login_bp.login'))
    
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()

    # Fetch logs with additional ML performance metrics
    cursor.execute("""
        SELECT p.id, p.food_type, u.name, p.confidence, p.timestamp, p.user_id, 
               p.image_processing_time, p.inference_time, p.total_execution_time
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.timestamp DESC
    """)
    logs = cursor.fetchall()

    # Calculate total number of predictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    # Find the most common food type
    cursor.execute("""
        SELECT food_type, COUNT(food_type) AS count 
        FROM predictions 
        GROUP BY food_type 
        ORDER BY count DESC 
        LIMIT 1
    """)
    most_common_food = cursor.fetchone()
    most_common_food = most_common_food[0] if most_common_food else "No Data"

    # Calculate average confidence and ML performance times
    cursor.execute("""
        SELECT AVG(confidence), 
               AVG(CAST(image_processing_time AS REAL)), 
               AVG(CAST(inference_time AS REAL)), 
               AVG(CAST(total_execution_time AS REAL)) 
        FROM predictions
    """)
    avg_confidence, avg_image_processing, avg_inference, avg_total_execution = cursor.fetchone()

    avg_confidence = round(avg_confidence, 2) if avg_confidence else 0.0
    avg_image_processing = round(avg_image_processing, 2) if avg_image_processing else 0.0
    avg_inference = round(avg_inference, 2) if avg_inference else 0.0
    avg_total_execution = round(avg_total_execution, 2) if avg_total_execution else 0.0

    # Get total number of users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Prepare data for visualization
    cursor.execute("""
        SELECT food_type, COUNT(*) 
        FROM predictions 
        GROUP BY food_type 
        ORDER BY COUNT(*) DESC
    """)
    food_stats = cursor.fetchall()

    food_labels = [row[0] for row in food_stats]  # Extract food types
    food_data = [row[1] for row in food_stats]    # Extract counts

    # Get the user who made the most predictions
    cursor.execute("""
        SELECT u.name, COUNT(p.id) AS prediction_count 
        FROM predictions p
        JOIN users u ON p.user_id = u.id 
        GROUP BY u.id 
        ORDER BY prediction_count DESC 
        LIMIT 1
    """)
    most_searched = cursor.fetchone()
    most_searched_name = most_searched[0] if most_searched else "No Data"
    most_predictions = most_searched[1] if most_searched else "0"

    conn.close()

    return render_template(
        'admin.html',
        logs=logs,
        total_predictions=total_predictions,
        most_common_food=most_common_food,
        avg_confidence=avg_confidence,
        avg_image_processing=avg_image_processing,
        avg_inference=avg_inference,
        avg_total_execution=avg_total_execution,
        total_users=total_users,
        food_labels=food_labels,
        food_data=food_data,
        most_searched=most_searched_name,
        most_predictions=most_predictions,
    )
