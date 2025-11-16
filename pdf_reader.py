import pytesseract
from pdf2image import convert_from_path
import os

class PDFReader:
    def __init__(self, tesseract_cmd=None):
        # Set the Tesseract command path if provided
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def read_pdf(self, pdf_path):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The file {pdf_path} does not exist.")

        # Convert PDF to images
        images = convert_from_path(pdf_path)

        # Extract text from each image
        content = []
        for image in images:
            text = pytesseract.image_to_string(image)
            content.append(text)

        # Combine all text into a single string
        return "\n".join(content)

# Example usage
if __name__ == "__main__":
    reader = PDFReader()
    try:
        pdf_content = reader.read_pdf("Radiation_detection_and_measurement.pdf")  # Replace with the actual PDF path
        print(pdf_content)
    except FileNotFoundError as e:
        print(e)

