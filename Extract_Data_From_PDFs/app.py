import re
import pdfplumber
import pytesseract
from PIL import Image
from fuzzywuzzy import fuzz


def extract_prep_questions(prep_pdf_path):
    questions = []
    with pdfplumber.open(prep_pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    if "Important Numerical" in full_text:
        full_text = full_text.split("Important Numerical", 1)[1]

    lines = full_text.strip().splitlines()

    current_num = None
    current_text = ""
    for line in lines:
        m = re.match(r'^\s*(\d+)[\.\)]\s*(.*)', line)
        if m:
            if current_num is not None and current_text:
                questions.append(current_text.strip())
            num, text_start = m.groups()
            current_num = num
            current_text = text_start
        else:
            if current_num is not None and line.strip():
                current_text += " " + line.strip()

    if current_num is not None and current_text:
        questions.append(current_text.strip())

    questions = questions[:45]
    return questions


def extract_chapters(physics_pdf_path):
    chapters = []
    with pdfplumber.open(physics_pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text or len(text.strip()) < 10:
                pil_image = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(pil_image)

            text = " ".join(text.split())

            match = re.search(r'Chapter\s+\d+', text, re.IGNORECASE)
            if match:
                start_idx = match.start()
                chapter_line = text[start_idx:].split("\n")[0]
                chapter_name = chapter_line.strip().strip(":").strip()
                chapters.append((chapter_name, i))
    return chapters


def find_question_in_book(question, pdf):
    best_score = 0
    best_page_idx = None
    best_line = None

    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text or len(text.strip()) < 10:
            pil_image = page.to_image(resolution=300).original
            text = pytesseract.image_to_string(pil_image)

        lines = text.splitlines()
        for line in lines:
            score = fuzz.token_sort_ratio(question, line)
            if score > best_score:
                best_score = score
                best_page_idx = i
                best_line = line

    return best_score, best_page_idx, best_line


def match_questions_to_book(prep_questions, physics_pdf_path, chapters):
    matches = []
    pdf = pdfplumber.open(physics_pdf_path)
    chapters_sorted = sorted(chapters, key=lambda x: x[1])

    for idx, question in enumerate(prep_questions, start=1):
        score, page_idx, matched_line = find_question_in_book(question, pdf)
        if page_idx is None:
            matches.append((idx, question, None, None, score))
            continue

        chapter_name = None
        for chap_name, chap_page in chapters_sorted:
            if chap_page <= page_idx:
                chapter_name = chap_name
            else:
                break

        book_q_num = None
        m = re.match(r'^\s*(\d+)[\.\)]', matched_line)
        if m:
            book_q_num = m.group(1)
        else:
            page_text = pdf.pages[page_idx].extract_text().splitlines()
            for line in page_text:
                m2 = re.match(r'^\s*(\d+)[\.\)]', line)
                if m2:
                    book_q_num = m2.group(1)
                    break

        matches.append((idx, question, chapter_name, book_q_num, score))

    pdf.close()
    return matches


def print_matches(matches):
    print(f"{'Prep #':<6} {'Chapter':<30} {'Book Q#':<7} {'Question (prep)'}")
    print("-" * 100)
    for idx, question, chapter, book_q_num, score in matches:
        chapter_str = chapter if chapter else "Unknown"
        qnum_str = book_q_num if book_q_num else "N/A"
        print(f"{idx:<6} {chapter_str:<30} {qnum_str:<7} {question[:60]}{'...' if len(question)>60 else ''}")


# Example usage (replace with actual file paths):
prep_questions = extract_prep_questions("preparation_paper.pdf")
chapters = extract_chapters("physics_book.pdf")
matches = match_questions_to_book(prep_questions, "physics_book.pdf", chapters)
print_matches(matches)

