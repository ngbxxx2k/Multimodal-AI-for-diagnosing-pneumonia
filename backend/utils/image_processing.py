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

def draw_bounding_boxes(image: Image.Image, detections: list) -> Image.Image:
    """
    Vẽ các bounding box lên ảnh PIL.
    detections: Danh sách các dict hoặc object có 'box', 'conf', 'label'.
    """
    draw = ImageDraw.Draw(image)
    # Cố gắng load font, nếu không thì dùng mặc định
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
        
    for det in detections:
    # Giả sử định dạng det từ kết quả YOLO
        # Tùy thuộc vào cách chúng ta bọc YOLO, điều này có thể cần điều chỉnh.
        # Giả sử định dạng chuẩn: {'box': [x1, y1, x2, y2], 'label': str, 'conf': float}
        box = det.get('box')
        label = det.get('label')
        conf = det.get('conf', 0.0)
        
        if box:
            x1, y1, x2, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            text = f"{conf:.2f}"
            
            # Vẽ nền chữ
            text_bbox = draw.textbbox((x1, y1), text, font=font)
            draw.rectangle(text_bbox, fill="red")
            draw.text((x1, y1), text, fill="white", font=font)
            
    return image

def get_lesion_location_text(bbox, lung_mask):
    """Logic xác định vị trí: Phổi nào? Thùy nào? Hay toàn bộ?"""
    # bbox: [x1, y1, x2, y2]
    x1, y1, x2, y2 = bbox
    H, W = lung_mask.shape
    mid_x = W // 2
    
    bbox_center_x = (x1 + x2) / 2
    if bbox_center_x < mid_x:
        side = "Phổi Phải"
        hemic_mask = lung_mask[:, :mid_x]
        # Tọa độ x cho việc cắt phải nằm trong giới hạn của hemic_mask (tương ứng với 0..mid_x)
        # Tuy nhiên, chúng ta đang cắt mask gốc với x1:min(x2, mid_x), nên nó ánh xạ chính xác sang các pixel bên trái.
        roi_mask_area = lung_mask[y1:y2, x1:min(x2, mid_x)]
    else:
        side = "Phổi Trái"
        hemic_mask = lung_mask[:, mid_x:]
        roi_mask_area = lung_mask[y1:y2, max(x1, mid_x):x2]

    total_lung_area = hemic_mask.sum()
    lesion_in_lung_area = roi_mask_area.sum()

    if total_lung_area == 0: return "Vùng không xác định"

    coverage_ratio = lesion_in_lung_area / total_lung_area

    if coverage_ratio > 0.50:
        return f"{side} (Toàn bộ)"

    # Sử dụng NonZero để tìm ranh giới dọc của phổi
    ys_lung = np.where(hemic_mask > 0)[0]
    if len(ys_lung) == 0: return f"{side} (Không xác định)"
    
    lung_top = ys_lung.min()
    lung_bottom = ys_lung.max()
    lung_height = lung_bottom - lung_top
    
    ys_lesion = np.where(roi_mask_area > 0)[0]
    if len(ys_lesion) == 0:
        center_y_rel = ((y1 + y2) / 2) - lung_top
    else:
        center_y_rel = (ys_lesion.mean() + y1) - lung_top

    ratio = center_y_rel / lung_height

    lobe = "Không xác định"
    if side == "Phổi Phải":
        if ratio < 0.35: lobe = "Thùy Trên"
        elif ratio < 0.65: lobe = "Thùy Giữa"
        else: lobe = "Thùy Dưới"
    else: 
        if ratio < 0.5: lobe = "Thùy Trên"
        else: lobe = "Thùy Dưới"

    return f"{side} - {lobe}"

def preprocess_for_unet(image: Image.Image) -> np.ndarray:
    """Thay đổi kích thước và chuẩn hóa ảnh cho U-Net."""
    # Chỗ giữ chỗ: logic thay đổi kích thước cụ thể thường cần thiết (ví dụ: 256x256)
    # Prompt không chỉ định kích thước đầu vào U-Net, giả sử là chuẩn.
    # Cần phải mạnh mẽ.
    # Hiện tại, trả về numpy.
    return np.array(image.convert("L"))
