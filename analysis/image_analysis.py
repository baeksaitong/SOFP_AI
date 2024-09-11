from .color_analyzer import ColorAnalyzer
from .shape_detector import ShapeDetector
from .image_processor import ImageProcessor


class ImageAnalysis:
    """이미지 분석을 수행하는 클래스"""

    def __init__(self):
        self.color_analyzer = ColorAnalyzer()
        self.shape_detector = ShapeDetector()
        self.image_processor = ImageProcessor()

    def analyze_image(self, input_image_path):
        """
        이미지를 분석하여 주요 색상과 모양을 반환.
        """
        # 이미지 로드 및 윤곽선 찾기
        image = self.image_processor.load_and_preprocess_image(input_image_path)
        contours, original_contour = self.image_processor.find_image_contours(image)

        # 이미지 잘라내기
        bounding_box = self.image_processor.get_bounding_box(contours)
        cropped_image = self.image_processor.crop_shape(image, bounding_box)

        # 주요 색상 추출
        dominant_colors, total_pixels = self.color_analyzer.extract_dominant_colors(cropped_image)

        # 첫 번째 주요 색상이 전체의 절반 이상을 차지하는지 확인
        if dominant_colors[0][1] >= total_pixels / 2:
            dominant_colors = [dominant_colors[0]]

        # 모양 식별
        shape = self.shape_detector.identify_shape(original_contour)

        return dominant_colors, shape


# 사용 예제
if __name__ == "__main__":
    image_analysis = ImageAnalysis()
    dominant_colors, shape = image_analysis.analyze_image('C:\\temp\\img3.PNG')
    print(f"Dominant Colors: {dominant_colors}")
    print(f"Identified Shape: {shape}")
