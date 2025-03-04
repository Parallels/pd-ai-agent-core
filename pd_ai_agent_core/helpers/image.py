import cv2
import numpy as np
from collections import Counter
import base64
import logging

logger = logging.getLogger(__name__)


def get_dominant_border_color(
    image_data: str, border_percentage: float = 0.2, debug: bool = False
) -> str:
    """
    Detect the most prevalent color in the borders of an image.

    Args:
        image (np.ndarray): Input image (BGR format).
        border_percentage (float): Percentage of the border to consider (0.0 to 1.0).

    Returns:
        tuple: Dominant BGR color (B, G, R).
    """
    imageBytes = base64.b64decode(image_data)
    np_array = np.frombuffer(imageBytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        return "#F2F2F7"

    if len(image.shape) == 2:  # Grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    height, width, _ = image.shape
    border_thickness_h = int(height * border_percentage)
    border_thickness_w = int(width * border_percentage)

    top_border = image[:border_thickness_h, :]
    bottom_border = image[-border_thickness_h:, :]
    left_border = image[:, :border_thickness_w]
    right_border = image[:, -border_thickness_w:]

    borders_combined = np.concatenate(
        (
            top_border.reshape(-1, 3),
            bottom_border.reshape(-1, 3),
            left_border.reshape(-1, 3),
            right_border.reshape(-1, 3),
        ),
        axis=0,
    )

    # Count the most common color
    pixel_counts = Counter(map(tuple, borders_combined))
    dominant_color = pixel_counts.most_common(1)[0][0]

    hex_color = "#%02X%02X%02X" % dominant_color

    if debug:
        logger.info(f"Dominant Border Color: {hex_color}")

    return hex_color


def detect_black_screen(
    image_data: str,
    black_threshold: int = 30,
    black_percentage: float = 0.9,
    debug: bool = False,
) -> bool:
    """
    Detect if an image is mostly black.

    Args:
        image (np.ndarray): The input image (BGR or grayscale).
        black_threshold (int): Pixel values below this are considered black (0-255).
        black_percentage (float): Percentage threshold to classify as mostly black (0.0 - 1.0).

    Returns:
        bool: True if the image is mostly black, False otherwise.
    """
    imageBytes = base64.b64decode(image_data)
    image = np.frombuffer(imageBytes, dtype=np.uint8)

    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    black_pixels_mask = gray < black_threshold

    black_pixels_count = np.sum(black_pixels_mask)
    total_pixels = gray.size

    black_ratio = black_pixels_count / total_pixels

    if debug:
        logger.info(
            f"Black Pixels: {black_pixels_count}, Total Pixels: {total_pixels}, Black Ratio: {black_ratio:.2%}"
        )

    return bool(black_ratio >= black_percentage)
