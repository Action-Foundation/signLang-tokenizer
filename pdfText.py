import pdfplumber
import os
from tokenizer import *

def extract_text_and_images_from_pdf(pdf_path, output_image_folder):
    extracted_text = ""
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract text
            extracted_text += page.extract_text() or ""

            # Convert full page to image and save it
            image_filename = f"page_{page_num + 1}.png"
            image_path = os.path.join(output_image_folder, image_filename)

            # Save the entire page as an image
            page.to_image().save(image_path)
            # print(f"Saved full page image to {image_path}")

    return extracted_text

# Example usage:
pdf_path = "pdf.pdf"  # Replace with your PDF file path
output_image_folder = "extracted_images"
extracted_text = extract_text_and_images_from_pdf(pdf_path, output_image_folder)

tokens = tokenize_sentence(extracted_text)

print("The tokens for the story",tokens)

# Save extracted text to a file
with open("extracted_text.txt", "w", encoding="utf-8") as file:
    file.write(extracted_text)

# print("Text extracted and saved to extracted_text.txt")


