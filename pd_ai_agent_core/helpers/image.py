import cv2
import numpy as np
from collections import Counter
import base64
import logging
import io

logger = logging.getLogger(__name__)

# Try to import PIL - this will be needed for optimize_image
try:
    from PIL import Image

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    logger.warning("PIL not available, image optimization functions will be limited")


def optimize_image(
    image_data: str,
    quality: int = 60,
    max_width: int = 800,
    format: str = "JPEG",
    debug: bool = False,
) -> str:
    """
    Optimize an image by resizing and compressing it.

    Args:
        image_data (str): Base64 encoded image data
        quality (int): Output image quality (0-100, JPEG only)
        max_width (int): Maximum width in pixels (maintains aspect ratio)
        format (str): Output format ('JPEG', 'PNG', etc.)
        debug (bool): Whether to log debug information

    Returns:
        str: Base64 encoded optimized image
    """
    if not PILLOW_AVAILABLE:
        logger.warning("PIL not available, cannot optimize image")
        return image_data

    try:
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)

        # Convert to PIL Image
        img = Image.open(io.BytesIO(image_bytes))

        # Calculate new dimensions maintaining aspect ratio
        width, height = img.size
        if width > max_width:
            ratio = max_width / width
            new_width = max_width
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to desired format with compression
        output = io.BytesIO()
        if format.upper() == "JPEG":
            img = img.convert("RGB")  # JPEG doesn't support alpha channel
            img.save(output, format=format, quality=quality, optimize=True)
        else:
            img.save(output, format=format, optimize=True)

        output.seek(0)

        # Convert back to base64
        optimized_base64 = base64.b64encode(output.read()).decode("utf-8")

        # Log size reduction
        if debug:
            original_size = len(image_data)
            new_size = len(optimized_base64)
            reduction = (1 - (new_size / original_size)) * 100
            logger.info(
                f"Image optimized: {original_size:,} bytes → {new_size:,} bytes ({reduction:.1f}% reduction)"
            )

        return optimized_base64
    except Exception as e:
        logger.error(f"Error optimizing image: {e}")
        return image_data


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


def scale_image(image_data: str, scale_factor: float = 0.5) -> str:
    """
    Scale an image by a given factor.
    """
    imageBytes = base64.b64decode(image_data)
    image = np.frombuffer(imageBytes, dtype=np.uint8)
    image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

    # Convert back to base64
    optimized_base64 = base64.b64encode(image).decode("utf-8")

    return optimized_base64
