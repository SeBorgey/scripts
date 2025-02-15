import fitz
import os

input_folder = "input"
output_folder = "output"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        input_pdf = fitz.open(input_path)
        output_pdf = fitz.open()
        previous_page_text = "ЫЫЫЫЫЫ"
        current_slide_pages = []

        for page_num in range(len(input_pdf)):
            page = input_pdf.load_page(page_num)
            text = page.get_text("text")

            if previous_page_text[:-1] in text:
                current_slide_pages.append(page)
            else:
                if current_slide_pages:
                    output_pdf.insert_pdf(input_pdf, from_page=current_slide_pages[-1].number,
                                          to_page=current_slide_pages[-1].number)
                current_slide_pages = [page]
                previous_page_text = text

        if current_slide_pages:
            output_pdf.insert_pdf(input_pdf, from_page=current_slide_pages[-1].number,
                                  to_page=current_slide_pages[-1].number)

        output_pdf.save(output_path)
        input_pdf.close()
        output_pdf.close()

print("Файлы сохранены в папке:", output_folder)
