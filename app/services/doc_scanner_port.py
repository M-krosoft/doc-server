import io
from abc import abstractmethod
from typing import override

import numpy as np
from PIL import Image
from doc_scanner import run_scan_by_image
from werkzeug.datastructures.file_storage import FileStorage

from app import repository
from app.exceptions import InvalidFileExtensionError, RecognizeTextNotImplementedError
from app.services.vision_service import VisionService

_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def _is_allowed_extension(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in _ALLOWED_EXTENSIONS


class DocScanPort:

    @staticmethod
    def _prepare_image_content(file: FileStorage) -> bytes:
        if not _is_allowed_extension(file.filename):
            raise InvalidFileExtensionError
        return file.read()

    @staticmethod
    def _run_scan_image(image_content: bytes) -> np.ndarray:
        image = Image.open(io.BytesIO(image_content))
        image_np = np.array(image)
        return run_scan_by_image(image_np)

    @staticmethod
    def _prepare_image_response(scanned_image: np.ndarray) -> io.BytesIO:
        scanned_image_pil = Image.fromarray(scanned_image)
        img_byte_arr = io.BytesIO()
        scanned_image_pil.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

    @abstractmethod
    def scan_image(self, file: FileStorage) -> io.BytesIO:
        pass

    @abstractmethod
    def recognize_text(self, file: FileStorage) -> io.BytesIO:
        pass

    @staticmethod
    def count_receipts() -> int:
        return repository.count_receipts()


class DocScanApiKeyAdapter(DocScanPort):
    def __init__(self, vision_service: VisionService):
        self.vision_service = vision_service

    @override
    def scan_image(self, file: FileStorage) -> io.BytesIO:
        image_content = self._prepare_image_content(file)

        detected_text = self.vision_service.detect_text_in_image(image_content)
        repository.save_receipt(receipt_content=detected_text)

        scanned_image = self._run_scan_image(image_content=image_content)
        return self._prepare_image_response(scanned_image)

    @override
    def recognize_text(self, file: FileStorage) -> str:
        image_content = self._prepare_image_content(file)
        return self.vision_service.detect_text_in_image(image_content)


class DocScanNoApiKeyAdapter(DocScanPort):
    def __init__(self):
        super().__init__()

    @override
    def scan_image(self, file: FileStorage) -> io.BytesIO:
        image_content = self._prepare_image_content(file)
        scanned_image = self._run_scan_image(image_content=image_content)
        return self._prepare_image_response(scanned_image)

    @override
    def recognize_text(self, file: FileStorage) -> str:
        raise RecognizeTextNotImplementedError
