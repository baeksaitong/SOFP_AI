from flask import Blueprint, current_app
from analysis.image_analysis import ImageAnalysis
from .database import Database
from .upload_handler import handle_file_upload
from .response_handler import create_response

routes = Blueprint('routes', __name__)

db = Database(db_name="image_analysis_db", user="postgres", password="1234")


@routes.route('/analyze', methods=['POST'])
def analyze_image():
    filepath, error, status = handle_file_upload()
    if error:
        return create_response(error=error, status=status)

    image_analysis = ImageAnalysis()
    dominant_colors, shape = image_analysis.analyze_image(filepath)
    result = f"Colors: {dominant_colors}, Shape: {shape}"

    with open(filepath, 'rb') as img_file:
        image_data = img_file.read()

    record_id = db.insert_analysis(image_data, result)
    return create_response(data={'id': record_id, 'result': result})


@routes.route('/history/<int:record_id>', methods=['GET'])
def get_analysis(record_id):
    db.cursor.execute("SELECT id, result, analyzed_at FROM image_analysis WHERE id = %s;", (record_id,))
    record = db.cursor.fetchone()
    if record:
        data = {'id': record[0], 'result': record[1], 'analyzed_at': record[2].isoformat()}
        return create_response(data=data)
    return create_response(error='Record not found', status=404)
