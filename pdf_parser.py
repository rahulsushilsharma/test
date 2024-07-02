import fitz  # PyMuPDF
import re
import uuid
import pandas as pd
import os

def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    images = []
    tables = []
    
    for page in doc:
        text += page.get_text()
        
        # Extract images
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)
        
        # Extract tables (simplified approach, might need improvement)
        tables.extend(page.find_tables())
    
    doc.close()
    return text, images, tables

def generate_unique_id():
    return str(uuid.uuid4())[:8]

def replace_content_with_placeholders(text, images, tables):
    modified_text = text
    image_dict = {}
    table_dict = {}
    
    # Replace images with placeholders
    for i, img in enumerate(images):
        img_id = f"IMG_{generate_unique_id()}"
        image_dict[img_id] = img
        modified_text = re.sub(r'\[Image \d+\]', f'[{img_id}]', modified_text, count=1)
    
    # Replace tables with placeholders
    for i, table in enumerate(tables):
        table_id = f"TBL_{generate_unique_id()}"
        table_dict[table_id] = table
        modified_text = re.sub(r'\[Table \d+\]', f'[{table_id}]', modified_text, count=1)
    
    return modified_text, image_dict, table_dict

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def save_images(image_dict, output_folder):
    for img_id, img_bytes in image_dict.items():
        try:
            with open(f"{output_folder}/{img_id}.png", 'wb') as f:
                f.write(img_bytes)
        except Exception as e:
            print(f"Error saving image {img_id}: {str(e)}")

def save_tables(table_dict, output_folder):
    for table_id, table in table_dict.items():
        try:
            df = pd.DataFrame(table.extract())
            df.to_csv(f"{output_folder}/{table_id}.csv", index=False)
        except Exception as e:
            print(f"Error saving table {table_id}: {str(e)}")

def create_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Main process
pdf_path = "sample.pdf"
output_text_path = "output_text.txt"
output_folder = "extracted_content"

# Create output directory
create_output_directory(output_folder)

# Extract content from PDF
text, images, tables = extract_pdf_content(pdf_path)

# Replace content with placeholders
modified_text, image_dict, table_dict = replace_content_with_placeholders(text, images, tables)

# Save modified text to file
save_text_to_file(modified_text, output_text_path)

# Save images and tables
save_images(image_dict, output_folder)
save_tables(table_dict, output_folder)

print(f"Processed PDF. Text saved to {output_text_path}. Images and tables saved in {output_folder}.")
