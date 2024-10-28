import json
from flask import Blueprint, current_app, Response
from analysis.image_analysis import ImageAnalysis
from .database import Database
from .response_handler import create_response
from .upload_handler import handle_file_upload

routes = Blueprint('routes', __name__)

# 데이터베이스 연결
db = Database(db_name="image_analysis_db", user="postgres", password="1234")


@routes.route('/analyze', methods=['POST'])
def analyze_image():
    # 파일 업로드 처리
    filepath, error, status = handle_file_upload()
    if error:
        return create_response(error=error, status=status)

    # 이미지 분석 수행
    analysis = ImageAnalysis()
    image_color_data, image_shape = analysis.analyze_image(filepath)

    # color에서 숫자를 제거 후, 리스트를 단순화 (색상 이름만 추출)
    image_colors = [color[0] for color in image_color_data]

    # 분석 결과를 데이터베이스에 저장
    inserted_id = db.insert_result(filepath, color=", ".join(image_colors), shape=image_shape)

    # 결과 반환 (색상은 문자열로 반환)
    return create_response(data={
        "id": inserted_id,
        "color": ", ".join(image_colors),  # 필요없는 부분 제거 후, 색상 이름만 반환
        "shape": image_shape
    })



@routes.route('/results', methods=['GET'])
def get_results():
    # 데이터베이스에서 결과 가져오기
    results = db.fetch_results()
    response_data = []

    # 결과를 JSON으로 변환
    for row in results:
        response_data.append({
            "image_path": row[0],
            "color": row[1],  # 색상 값
            "shape": row[2],  # 모양 값
            "analyzed_at": row[3]
        })

    return create_response(data=response_data)
