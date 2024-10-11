import json
from flask import Blueprint, current_app, Response
from analysis.image_analysis import ImageAnalysis
from .database import Database
from .response_handler import create_response
from .upload_handler import handle_file_upload

routes = Blueprint('routes', __name__)

db = Database(db_name="image_analysis_db", user="postgres", password="1234")


@routes.route('/analyze', methods=['POST'])
def analyze_image():
    # 파일 업로드 처리
    filepath, error, status = handle_file_upload()
    if error:
        return create_response(error=error, status=status)

    # 이미지 분석 (색상 및 모양)
    image_analysis = ImageAnalysis()
    dominant_colors, shape = image_analysis.analyze_image(filepath)

    # 분석 결과를 JSON 형식으로 구조화
    result = {
        "Colors": dominant_colors,  # 예: [('갈색', 52530), ('파랑', 12345)]
        "Shape": shape  # 예: '타원형'
    }

    # 이미지 데이터를 바이너리 형식으로 읽기
    with open(filepath, 'rb') as img_file:
        image_data = img_file.read()

    # result를 JSON 문자열로 변환
    result_json = json.dumps(result)

    # 데이터베이스에 분석 결과 저장
    record_id = db.insert_analysis(image_data, result_json)

    # 최소화된 JSON 응답 생성
    response_data = {
        'data': {
            'id': record_id,
            'result': result
        }
    }

    # compact JSON 형식으로 응답 (separators 사용하여 공백 최소화)
    return Response(json.dumps(response_data, separators=(',', ':')), mimetype='application/json')
