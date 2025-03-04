import base64
from pd_ai_agent_core.core_types.session_service import SessionService
from pd_ai_agent_core.services.service_registry import ServiceRegistry
from pd_ai_agent_core.common.constants import OCR_SERVICE_NAME
import easyocr
import cv2
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)


class OCRTextItem:
    text: str
    bbox: List[int]
    confidence: float

    def __init__(self, text: str, bbox: List[int], confidence: float):
        self.text = text
        self.bbox = bbox
        self.confidence = confidence


class OCRResult:
    text: List[OCRTextItem] = []
    average_confidence: float = 0.0
    strings: List[str] = []

    def __init__(self):
        self.text = []
        self._confidence = 0.0
        self.average_confidence = 0.0
        self.strings = []

    def add(self, text: str, bbox: List[int], confidence: float):
        if confidence > 0.5:
            self.text.append(OCRTextItem(text, bbox, confidence))
            self.strings.append(text)
        self._confidence += confidence
        self.average_confidence = self._confidence / len(self.text)


class OCRService(SessionService):
    def __init__(self, session_id: str, debug: bool = False):
        self.session_id = session_id
        self.debug = debug
        self.reader = easyocr.Reader(["en"])
        self.register()

    def name(self) -> str:
        return OCR_SERVICE_NAME

    def register(self) -> None:
        """Register this service with the registry"""
        if not ServiceRegistry.register(self.session_id, OCR_SERVICE_NAME, self):
            logger.info(f"OCR service already registered for session {self.session_id}")
            return

        logger.info(f"OCR service registered for session {self.session_id}")

    def unregister(self) -> None:
        """Unregister this service from the registry"""
        logger.info(f"OCR service unregistered for session {self.session_id}")

    def ocr(self, image_data: str) -> OCRResult:
        """OCR an image, the image should be a base64 encoded string"""
        logger.info(self.session_id, f"OCRing image: {image_data}")
        imageBytes = base64.b64decode(image_data)
        np_array = np.frombuffer(imageBytes, dtype=np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        results = self.reader.readtext(gray)
        result: OCRResult = OCRResult()
        for bbox, text, confidence in results:
            if self.debug:
                logger.info(
                    f"[{self.session_id}] Detected Text: {text} (Confidence: {confidence:.2f})"
                )
            result.add(text, bbox, confidence)
        return result
