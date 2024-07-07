from PyPDF2 import PdfReader, PdfWriter


def extract_information(pdf_path):
    # Create a PDF reader object
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        information = pdf.metadata
        number_of_pages = len(pdf.pages)

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information


def extract_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf = PdfReader(pdf_file)

        # Iterate through all the pages
        for page in pdf.pages:
            # Extract the text from the page
            print(page.extract_text())


def rotate_pages(pdf_path):
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(pdf_path)
    # Rotate page 90 degrees
    page_1 = pdf_reader.pages[0].rotate(90)
    pdf_writer.add_page(page_1)
    # Rotate page 180 degrees
    page_2 = pdf_reader.pages[1].rotate(180)
    pdf_writer.add_page(page_2)
    # Add a page in normal orientation
    pdf_writer.add_page(pdf_reader.pages[2])

    with open('rotate_pages.pdf', 'wb') as fh:
        pdf_writer.write(fh)


def merge_two_pdfs(pdf1_path, pdf2_path):
    # Open the first PDF file
    with open(pdf1_path, 'rb') as pdf1_file:
        pdf1_reader = PdfReader(pdf1_file)

        # Open the second PDF file
        with open(pdf2_path, 'rb') as pdf2_file:
            pdf2_reader = PdfReader(pdf2_file)

            # Create a new PDF file
            pdf_writer = PdfWriter()

            # Add all the pages from the first PDF
            for page in pdf1_reader.pages:
                pdf_writer.add_page(page)

            # Add all the pages from the second PDF
            for page in pdf2_reader.pages:
                pdf_writer.add_page(page)

            # Save the output to a new PDF file
            with open('merged.pdf', 'wb') as output_file:
                pdf_writer.write(output_file)


def merge_pdfs(pdf_paths, output='merged.pdf'):
    # Create a new PDF file
    pdf_writer = PdfWriter()
    for path in pdf_paths:
        # Iterate through the pdfs
        pdf_reader = PdfReader(path)
        # Add all the pages from the PDFs
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    # Save the output to a new PDF file
    with open(output, 'wb') as output_file:
        pdf_writer.write(output_file)


def split_pdfs(pdf_path, output='split'):
    # Create a PDF reader object
    pdf = PdfReader(pdf_path)
    for i, page in enumerate(pdf.pages):
        # Create a PDF writer object
        pdf_writer = PdfWriter()
        # Split the PDF by adding each page separately
        pdf_writer.add_page(page)
        # Save the PDF
        result = f'{output}{i}.pdf'
        with open(result, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)


def split_pdfs_by_parts(pdf_path, pages_per_part=5, output='part'):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PdfReader(pdf_file)
        n_pages = len(pdf_reader.pages)
        # Define the number of pages per part

        # Create the PDF writer objects
        pdf_writers = [PdfWriter() for _ in range(n_pages // pages_per_part + 1)]

        # Split the PDF into multiple parts
        for page_num in range(n_pages):
            # Get the current page
            page = pdf_reader.pages[page_num]
            part_num = page_num // pages_per_part
            pdf_writers[part_num].add_page(page)

        for i, writer in enumerate(pdf_writers):
            with open(f'{output}{i+1}.pdf', 'wb') as output_file:
                writer.write(output_file)


def encrypt_pdf(pdf_path, output='encrypted.pdf', password='secretpassword'):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PdfReader(pdf_file)

        # Create a new PDF writer object
        pdf_writer = PdfWriter()

        # Add the pages from the reader to the writer
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # Encrypt the PDF with a password
        pdf_writer.encrypt(password)

        # Save the output to a new PDF file
        with open(output, 'wb') as output_file:
            pdf_writer.write(output_file)
