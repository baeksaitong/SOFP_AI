import cv2
import numpy as np

class ImageProcessor:
    """이미지 전처리 및 윤곽선 검출을 위한 클래스"""

    def load_and_preprocess_image(self, input_image_path):
        """
        이미지를 불러오고 전처리합니다.
        """
        image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
        return cv2.medianBlur(image, 55)

    def find_image_contours(self, image):
        """
        이미지에서 윤곽선을 찾습니다.
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        contours, _ = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours[0].transpose(), contours[0]

    def crop_shape(self, image, bounding_box):
        """
        윤곽선을 기준으로 이미지를 자릅니다.
        알파 채널이 있는 경우와 없는 경우를 모두 처리합니다.
        """
        left_x, right_x, left_y, right_y = bounding_box
        cropped_image = image[left_y:right_y, left_x:right_x]

        # 이미지가 알파 채널(RGBA)이 있는지 확인
        if cropped_image.shape[2] == 4:
            # 알파 채널이 있을 때 처리
            trans_mask = cropped_image[:, :, 3] == 0
            cropped_image[trans_mask] = [255, 255, 255, 255]
        else:
            # 알파 채널이 없을 때 (RGB 이미지)
            trans_mask = np.zeros(cropped_image.shape[:2], dtype=bool)  # 투명 영역 없음
            cropped_image[trans_mask] = [255, 255, 255]

        return cropped_image

    def get_bounding_box(self, contours):
        """
        윤곽선의 경계 상자를 계산합니다.
        """
        right_point_x = np.max(contours[0])
        left_point_x = np.min(contours[0])
        right_point_y = np.max(contours[1])
        left_point_y = np.min(contours[1])
        return left_point_x, right_point_x, left_point_y, right_point_y
