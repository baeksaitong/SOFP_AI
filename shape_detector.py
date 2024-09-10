import cv2
import numpy as np

class ShapeDetector:
    """모양 검출을 위한 클래스"""

    def identify_shape(self, contour):
        """
        윤곽선을 바탕으로 모양을 추측하여 반환합니다.
        """
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        vertices = len(approx)

        # 윤곽선의 경계 상자를 계산하여 너비(w)와 높이(h)를 구함
        x, y, w, h = cv2.boundingRect(contour)

        # 꼭짓점 수에 따라 도형 추정
        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            aspect_ratio = w / float(h)
            if 0.95 <= aspect_ratio <= 1.05:
                return "Square"
            else:
                return "Ellipse"  # 직사각형이라고 판단될 경우 타원형으로 출력
        elif vertices == 5:
            return "Pentagon"
        elif vertices == 6:
            return "Hexagon"
        elif vertices == 8:
            return "Octagon"
        else:
            return "Circle"
