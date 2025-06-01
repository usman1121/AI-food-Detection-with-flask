from flask import Blueprint,session,redirect,url_for,jsonify
import sqlite3

delete_l = Blueprint("delete_l", __name__)

@delete_l.route('/delete/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    if session.get('role') != "Admin":
        return redirect(url_for('login_bp.login'))

    try:
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM predictions WHERE id = ?', (log_id,))
        record = cursor.fetchone()
        if record is None:
            return jsonify({'success': False, 'message': 'No record found with the provided ID'}), 404

        cursor.execute('DELETE FROM predictions WHERE id = ?', (log_id,))
        conn.commit()
        conn.close()

        return redirect(url_for('admin.admin_dashboard'))

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500