import cv2
import os
import argparse
from detector import DefectDetector
from report import generate_report
from utils import load_image, save_image

def run_inspection(image_path, output_path, confidence=0.3):
    """Run full defect inspection pipeline on an image."""
    print(f"\nLoading image: {image_path}")
    image = load_image(image_path)

    print("Running defect detection...")
    detector = DefectDetector(confidence=confidence)
    annotated_image, defects = detector.detect(image)

    os.makedirs("results", exist_ok=True)
    save_image(annotated_image, output_path)

    report, status = generate_report(defects, image_path, output_path)

    return status

def main():
    parser = argparse.ArgumentParser(
        description="Industrial Defect Detection System"
    )
    parser.add_argument("--input", type=str,
                        default="sample_images/test.jpg",
                        help="Path to input image")
    parser.add_argument("--output", type=str,
                        default="results/output.jpg",
                        help="Path to save annotated output")
    parser.add_argument("--confidence", type=float, default=0.3,
                        help="Detection confidence threshold (0-1)")
    args = parser.parse_args()

    status = run_inspection(args.input, args.output, args.confidence)
    print(f"\nInspection complete. Status: {status}")

if __name__ == "__main__":
    main()