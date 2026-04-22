import cv2
import numpy as np

DEFECT_COLORS = {
    "scratch":      (0, 0, 255),      # Red
    "dent":         (0, 165, 255),    # Orange
    "crack":        (0, 255, 255),    # Yellow
    "corrosion":    (255, 0, 0),      # Blue
    "contamination":(128, 0, 128),    # Purple
    "default":      (0, 255, 0),      # Green
}

def draw_defect(image, x1, y1, x2, y2, label, confidence):
    """Draw a bounding box and defect label on the image."""
    defect_type = label.lower().split()[0]
    color = DEFECT_COLORS.get(defect_type, DEFECT_COLORS["default"])

    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    text = f"{label}: {confidence:.0%}"
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(image, (x1, y1 - h - 10), (x1 + w + 4, y1), color, -1)
    cv2.putText(image, text, (x1 + 2, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return image

def load_image(image_path):
    """Load an image from file."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    return image

def save_image(image, output_path):
    """Save an image to file."""
    cv2.imwrite(output_path, image)
    print(f"Result saved to {output_path}")