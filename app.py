from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from main import ImageAnalysis
from database import Database

app = Flask(__name__)

# 데이터베이스 연결 설정
db = Database(db_name="image_analysis_db", user="postgres", password="1234")

# 업로드된 파일을 저장할 경로
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 허용된 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 이미지 분석
        image_analysis = ImageAnalysis()
        dominant_colors, shape = image_analysis.analyze_image(filepath)
        result = f"Colors: {dominant_colors}, Shape: {shape}"

        # 이미지 데이터를 바이너리로 읽기
        with open(filepath, 'rb') as img_file:
            image_data = img_file.read()

        # 분석 결과를 데이터베이스에 저장
        record_id = db.insert_analysis(image_data, result)

        # 결과 반환
        return jsonify({'id': record_id, 'result': result}), 200

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/history/<int:record_id>', methods=['GET'])
def get_analysis(record_id):
    db.cursor.execute("SELECT id, result, analyzed_at FROM image_analysis WHERE id = %s;", (record_id,))
    record = db.cursor.fetchone()
    if record:
        return jsonify({'id': record[0], 'result': record[1], 'analyzed_at': record[2].isoformat()}), 200
    return jsonify({'error': 'Record not found'}), 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
