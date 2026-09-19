import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def calculate_mask_area_ratio(mask: np.ndarray) -> float:
    """Tính tỷ lệ pixel trắng (phổi) so với tổng diện tích ảnh."""
    if mask is None:
        return 0.0
    total_pixels = mask.size
    white_pixels = np.count_nonzero(mask)
    return white_pixels / total_pixels

def count_blobs(mask: np.ndarray) -> int:
    """Đếm số vùng liên thông (pixel trắng) trong mask."""
    if mask is None:
        return 0
    # Đảm bảo mask là uint8
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    
    num_labels, _ = cv2.connectedComponents(mask)
    # num_labels bao gồm cả nền (0), nên trừ đi 1
    return num_labels - 1

def crop_lung_region(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Cắt ảnh theo bounding box của mask."""
    if mask is None:
        return image
        
    # Tìm đường viền hoặc hình chữ nhật bao quanh của các pixel khác 0
    coords = cv2.findNonZero(mask)
    if coords is None:
        return image
        
    x, y, w, h = cv2.boundingRect(coords)
    
    # Thêm một chút đệm nếu có thể? Hiện tại, cắt chặt chẽ như ngụ ý.
    cropped = image[y:y+h, x:x+w]
    return cropped

