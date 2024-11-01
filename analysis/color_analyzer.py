import cv2
import numpy as np
from collections import Counter

# 사전 정의된 색상과 그 RGB 값들
PREDEFINED_COLORS = {
    '하양': (255, 255, 255),  # white
    '노랑': (255, 255, 0),    # yellow
    '주황': (255, 165, 0),    # orange
    '분홍': (255, 192, 203),  # pink
    '빨강': (255, 0, 0),      # red
    '갈색': (165, 42, 42),    # brown
    '연두': (144, 238, 144),  # light green
    '초록': (0, 128, 0),      # green
    '청록': (0, 255, 255),    # cyan
    '파랑': (0, 0, 255),      # blue
    '남색': (0, 0, 128),      # navy
    '자주': (128, 0, 128),    # purple
    '보라': (238, 130, 238),  # violet
    '회색': (128, 128, 128),  # grey
    '검정': (0, 0, 0)         # black
}


class ColorAnalyzer:
    """색상 분석을 위한 클래스"""

    def find_closest_color(self, color):
        """
        입력 색상에 가장 가까운 사전 정의된 색상을 찾습니다.
        """
        min_distance = float('inf')
        closest_color_name = None

        for color_name, predefined_color in PREDEFINED_COLORS.items():
            distance = np.linalg.norm(np.array(color) - np.array(predefined_color))
            if distance < min_distance:
                min_distance = distance
                closest_color_name = color_name

        return closest_color_name

    def extract_dominant_colors(self, image, top_n=2):
        """
        이미지에서 주요 색상을 추출하고 사전 정의된 색상으로 매핑합니다.
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixels = image_rgb.reshape(-1, 3)
        mapped_colors = [self.find_closest_color(pixel) for pixel in pixels]
        color_counts = Counter(mapped_colors)
        total_pixels = len(mapped_colors)
        return color_counts.most_common(top_n), total_pixels
