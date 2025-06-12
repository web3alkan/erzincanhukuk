import os
import re

# --- CONFIGURATION ---
SOURCE_FILE = '/Users/web3alkan/Documents/GitHub/erzincanhukuk/Borçlar özel final.txt'
OUTPUT_DIR = 'sorular'
INDEX_FILE = 'index.html'
MAIN_TITLE = 'Erzincan Hukuk Borçlar Hukuku Özel Hükümler Çıkmış Sorular'

# --- HTML TEMPLATES (Identical to previous versions) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soru {question_number} | {main_title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; margin: 0; padding: 2rem; background-color: #f8f9fa; color: #343a40; }}
        .container {{ max-width: 800px; margin: auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .question-header {{ background-color: #007bff; color: white; padding: 1.5rem; border-top-left-radius: 8px; border-top-right-radius: 8px; }}
        .question-header h1 {{ margin: 0; font-size: 1.5rem; }}
        .question-body {{ padding: 1.5rem; }}
        .question-text {{ font-size: 1.2rem; font-weight: 500; margin-bottom: 1.5rem; }}
        .options ul {{ list-style-type: none; padding: 0; }}
        .options li {{ margin-bottom: 1rem; padding: 1rem; border: 1px solid #dee2e6; border-radius: 5px; transition: background-color 0.2s; }}
        .options li:hover {{ background-color: #e9ecef; }}
        .navigation {{ display: flex; justify-content: space-between; padding: 1.5rem; border-top: 1px solid #dee2e6; }}
        .nav-link {{ display: inline-block; padding: 0.75rem 1.5rem; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; transition: background-color 0.2s; }}
        .nav-link:hover {{ background-color: #0056b3; }}
        .nav-link.disabled {{ background-color: #6c757d; cursor: not-allowed; }}
        .home-link {{ text-align: center; padding-bottom: 1.5rem; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question-header">
            <h1>Soru {question_number}</h1>
        </div>
        <div class="question-body">
            <p class="question-text">{question_text}</p>
            <div class="options">
                <ul>
                    {options_html}
                </ul>
            </div>
        </div>
        <div class="home-link">
             <a href="../{index_file}" class="nav-link">Ana Sayfa</a>
        </div>
        <div class="navigation">
            {prev_button}
            {next_button}
        </div>
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{main_title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; margin: 0; padding: 2rem; background-color: #f8f9fa; color: #343a40; }}
        .container {{ max-width: 800px; margin: auto; }}
        h1 {{ text-align: center; color: #007bff; margin-bottom: 2rem; }}
        .question-list {{ list-style-type: none; padding: 0; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .question-list li {{ border-bottom: 1px solid #dee2e6; }}
        .question-list li:last-child {{ border-bottom: none; }}
        .question-list a {{ display: block; padding: 1.25rem 1.5rem; text-decoration: none; color: #212529; font-size: 1.1rem; transition: background-color 0.2s; }}
        .question-list a:hover {{ background-color: #e9ecef; color: #0056b3; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{main_title}</h1>
        <ul class="question-list">
            {question_links}
        </ul>
    </div>
</body>
</html>
"""

# --- THE ACTUAL FINAL, MOST ROBUST LOGIC ---
def parse_questions_final_v2(content):
    """
    Segments the entire text by the start of each question's options.
    This is the most reliable method as it uses the most consistent marker.
    """
    questions = []
    
    # 1. Find all reliable start markers: a newline followed by "A)" or "A.".
    # This marks the beginning of every question's option block.
    # The `re.IGNORECASE` flag handles cases where the letter might be lowercase.
    # The `(?=...)` is a positive lookahead to ensure the next line starts with B, which confirms it's a real option block.
    option_A_starts = [m.start() for m in re.finditer(r'\n\s*A[)\.\s].*\n\s*B[)\.\s]', content, re.IGNORECASE)]
    
    # Add the end of the content as the final boundary.
    boundaries = option_A_starts + [len(content)]

    # 2. Iterate through the boundaries to get each full question block.
    for i in range(len(boundaries) - 1):
        start_pos = boundaries[i]
        end_pos = boundaries[i+1]
        
        # The text from the start of one A-block to the next A-block is one full Q&A.
        full_block = content[start_pos:end_pos].strip()

        # 3. Within this block, the question is everything before the first newline.
        #    This assumes the question text is the first line(s) of the block we've found.
        try:
            first_newline = full_block.index('\n')
            question_text = full_block[:first_newline].strip()
            # If the question text is the A option, we need to find the real question text before this block
            if i > 0:
                prev_block_end = boundaries[i-1]
                # Search backwards from start_pos to find the text
                search_area = content[prev_block_end:start_pos]
                # Clean up junk comments from the previous question
                search_area = re.sub(r'([a-zA-Z])\1{2,}', '', search_area)
                search_area = re.sub(r'd ya da e.*', '', search_area, flags=re.I)
                question_text = search_area.strip()
            else: # First question
                 question_text = content[:start_pos].strip()

            options_text = full_block
        except ValueError:
            # If there's no newline, something is wrong with the block.
            continue
            
        # 4. Parse the options from the options text.
        options = re.findall(r'([A-E])[)\.\s](.*)', options_text)
        
        cleaned_options = [f"{opt[0]}) {opt[1].strip()}" for opt in options]

        # Final validation
        if question_text and len(cleaned_options) >= 4: # At least A, B, C, D
            questions.append({
                'question_text': ' '.join(question_text.split()),
                'options': cleaned_options
            })
            
    return questions
    
def create_question_page(q_idx, total_questions, question_data):
    # Same as before
    question_number = q_idx + 1
    options_html = "".join([f"<li>{opt}</li>" for opt in question_data['options']])
    prev_button = f'<a href="bo{q_idx}.html" class="nav-link">‹ Önceki Soru</a>' if q_idx > 0 else '<a class="nav-link disabled">‹ Önceki Soru</a>'
    next_button = f'<a href="bo{q_idx + 2}.html" class="nav-link">Sonraki Soru ›</a>' if question_number < total_questions else '<a class="nav-link disabled">Sonraki Soru ›</a>'
    html_content = HTML_TEMPLATE.format(question_number=question_number, main_title=MAIN_TITLE, question_text=question_data['question_text'], options_html=options_html, prev_button=prev_button, next_button=next_button, index_file=INDEX_FILE)
    filepath = os.path.join(OUTPUT_DIR, f'bo{question_number}.html')
    with open(filepath, 'w', encoding='utf-8') as f: f.write(html_content)

def create_index_page(total_questions):
    # Same as before
    question_links = "".join([f'<li><a href="{OUTPUT_DIR}/bo{i}.html">Soru {i}</a></li>' for i in range(1, total_questions + 1)])
    html_content = INDEX_TEMPLATE.format(main_title=MAIN_TITLE, question_links=question_links)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f: f.write(html_content)

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f: content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Source file not found: '{SOURCE_FILE}'"); return

    questions = parse_questions_final_v2(content)
    total_questions = len(questions)
    if total_questions == 0:
        print("No questions could be parsed. Check source file and parsing logic."); return
        
    print(f"Found {total_questions} questions. Generating HTML files...")
    for i, q_data in enumerate(questions): create_question_page(i, total_questions, q_data)
    print("Question pages created successfully.")
    create_index_page(total_questions)
    print(f"'{INDEX_FILE}' created successfully.")

if __name__ == '__main__':
    main() 