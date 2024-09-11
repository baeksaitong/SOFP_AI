import os
from werkzeug.utils import secure_filename
from flask import current_app, request

def allowed_file(filename):
    """
    파일 이름의 확장자를 확인하여 허용된 파일인지 검증합니다.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    """
    파일을 서버에 저장하고, 저장된 경로를 반환합니다.
    """
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath

def handle_file_upload():
    """
    파일 업로드 요청을 처리하고, 업로드된 파일 경로를 반환합니다.
    """
    if 'file' not in request.files:
        return None, 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return None, 'No selected file', 400
    if file and allowed_file(file.filename):
        filepath = save_file(file)
        return filepath, None, 200
    return None, 'File type not allowed', 400
