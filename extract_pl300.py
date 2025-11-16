#!/usr/bin/env python3
"""Extract PL-300 exam questions and generate HTML page."""

import psycopg2
import os
import html as html_module

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'databanter_db',
    'user': 'postgres',
    'password': 'admin@123'
}

def get_pl300_questions():
    """Fetch all PL-300 questions with associated data."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Get PL-300 exam ID
    cur.execute("""
        SELECT exam_id, exam_code, exam_name
        FROM db_exams
        WHERE exam_code ILIKE '%PL-300%' OR exam_code ILIKE '%PL300%'
        LIMIT 1
    """)

    exam_result = cur.fetchone()
    if not exam_result:
        print("PL-300 exam not found in database!")
        return []

    exam_id, exam_code, exam_name = exam_result
    print(f"Found exam: {exam_code} - {exam_name} (ID: {exam_id})")

    # Get all questions for PL-300
    cur.execute("""
        SELECT
            q.question_id,
            q.discussion_id,
            q.question_url,
            q.question_text_plain,
            q.question_text_html,
            q.topic_number,
            q.question_number,
            q.view_count,
            q.reply_count
        FROM db_questions q
        WHERE q.exam_id = %s
        ORDER BY q.topic_number, q.question_number, q.question_id
    """, (exam_id,))

    questions = cur.fetchall()
    print(f"Found {len(questions)} questions for PL-300")

    all_questions_data = []

    for q in questions:
        question_id = q[0]
        question_data = {
            'question_id': q[0],
            'discussion_id': q[1],
            'url': q[2],
            'text_plain': q[3],
            'text_html': q[4],
            'topic_number': q[5],
            'question_number': q[6],
            'view_count': q[7],
            'reply_count': q[8],
            'options': [],
            'answer': None,
            'images': [],
            'discussions': []
        }

        # Get options
        cur.execute("""
            SELECT option_letter, option_text, is_correct
            FROM db_question_options
            WHERE question_id = %s
            ORDER BY option_letter
        """, (question_id,))
        question_data['options'] = cur.fetchall()

        # Get answer
        cur.execute("""
            SELECT suggested_answer, answer_explanation
            FROM db_question_answers
            WHERE question_id = %s
        """, (question_id,))
        answer_result = cur.fetchone()
        if answer_result:
            question_data['answer'] = {
                'suggested': answer_result[0],
                'explanation': answer_result[1]
            }

        # Get images
        cur.execute("""
            SELECT image_type, original_url, local_path, file_name
            FROM db_question_images
            WHERE question_id = %s AND is_downloaded = TRUE
            ORDER BY image_id
        """, (question_id,))
        question_data['images'] = cur.fetchall()

        # Get discussions (top 3 by upvotes)
        cur.execute("""
            SELECT
                username,
                comment_text,
                selected_answer,
                upvote_count
            FROM db_discussions
            WHERE question_id = %s
            ORDER BY upvote_count DESC
            LIMIT 3
        """, (question_id,))
        question_data['discussions'] = cur.fetchall()

        all_questions_data.append(question_data)

    cur.close()
    conn.close()

    return all_questions_data, exam_code, exam_name

def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return html_module.escape(str(text))

def generate_html(questions_data, exam_code, exam_name):
    """Generate HTML page with all questions."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(exam_code)} - {escape_html(exam_name)}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 2em;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 2em;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5em;
        }}
        .exam-info {{
            background-color: #ecf0f1;
            padding: 1em;
            border-radius: 5px;
            margin-bottom: 2em;
        }}
        .question-block {{
            margin-bottom: 2em;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }}
        .question-header {{
            background-color: #3498db;
            color: white;
            padding: 1em;
            font-size: 1.1em;
            font-weight: bold;
        }}
        .question-content {{
            padding: 1.5em;
        }}
        .question-text {{
            background-color: #f9f9f9;
            padding: 1em;
            border-left: 4px solid #3498db;
            margin-bottom: 1em;
        }}
        .question-images {{
            margin: 1em 0;
        }}
        .question-images img {{
            max-width: 100%;
            height: auto;
            margin: 0.5em 0;
            border: 1px solid #ddd;
        }}
        h3 {{
            color: #2c3e50;
            margin-top: 1.5em;
            border-left: 4px solid #3498db;
            padding-left: 0.5em;
        }}
        ul {{
            padding-left: 1.5em;
            list-style-type: none;
        }}
        ul li {{
            padding: 0.5em;
            margin: 0.3em 0;
            background-color: #f9f9f9;
            border-radius: 3px;
        }}
        ul li.correct {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            font-weight: bold;
        }}
        .answer-box {{
            background-color: #d4edda;
            padding: 1em;
            border-radius: 5px;
            margin: 1em 0;
            border-left: 4px solid #28a745;
        }}
        .answer-box strong {{
            color: #155724;
        }}
        .explanation {{
            background-color: #fff3cd;
            padding: 1em;
            border-radius: 5px;
            margin: 1em 0;
            border-left: 4px solid #ffc107;
        }}
        .comment {{
            margin: 0.5em 0;
            padding: 1em;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }}
        .user {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .upvotes {{
            color: #28a745;
            font-weight: bold;
            font-size: 0.9em;
        }}
        button.collapsible {{
            background-color: #f2f2f2;
            color: #333;
            cursor: pointer;
            padding: 15px;
            width: 100%;
            text-align: left;
            border: none;
            outline: none;
            font-size: 16px;
            transition: 0.3s;
            border-bottom: 1px solid #ddd;
        }}
        button.collapsible:hover {{
            background-color: #e0e0e0;
        }}
        button.collapsible.active {{
            background-color: #ddd;
        }}
        button.collapsible:after {{
            content: '\\25BC';
            float: right;
            font-size: 0.8em;
        }}
        button.collapsible.active:after {{
            content: '\\25B2';
        }}
        .content {{
            padding: 0;
            display: none;
            overflow: hidden;
            background-color: white;
        }}
        .stats {{
            color: #666;
            font-size: 0.9em;
            margin-top: 0.5em;
        }}
        .no-discussions {{
            color: #999;
            font-style: italic;
            padding: 1em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{escape_html(exam_code)} - All Questions and Answers</h1>
        <div class="exam-info">
            <strong>Exam:</strong> {escape_html(exam_name)}<br>
            <strong>Total Questions:</strong> {len(questions_data)}
        </div>
"""

    for idx, q in enumerate(questions_data, 1):
        question_num = q.get('question_number') or idx
        topic_num = q.get('topic_number')

        # Build title with topic and question number
        if topic_num:
            title = f"Topic {topic_num}: Question #{question_num}"
        else:
            title = f"Question #{question_num}"

        html += f"""
        <button class="collapsible">{title}</button>
        <div class="content">
            <div class="question-content">
                <div class="question-text">
                    <p>{escape_html(q['text_plain'])}</p>
"""

        # Add images if any
        if q['images']:
            html += '                    <div class="question-images">\n'
            for img in q['images']:
                img_type, original_url, local_path, file_name = img
                if local_path and os.path.exists(local_path):
                    # Use relative path from HTML file
                    rel_path = os.path.relpath(local_path, 'power_bi_pl_300').replace('\\', '/')
                    html += f'                        <img src="{rel_path}" alt="{img_type}">\n'
            html += '                    </div>\n'

        html += '                </div>\n'

        # Add options
        if q['options']:
            html += '                <h3>Answer Choices</h3>\n'
            html += '                <ul>\n'
            for option in q['options']:
                letter, text, is_correct = option
                correct_class = ' class="correct"' if is_correct else ''
                html += f'                    <li{correct_class}>{escape_html(letter)}. {escape_html(text)}</li>\n'
            html += '                </ul>\n'

        # Add answer
        if q['answer']:
            if q['answer']['suggested']:
                html += f"""                <div class="answer-box">
                    <strong>Suggested Answer:</strong> {escape_html(q['answer']['suggested'])}
                </div>
"""
            if q['answer']['explanation']:
                html += f"""                <div class="explanation">
                    <strong>Explanation:</strong><br>
                    {escape_html(q['answer']['explanation'])}
                </div>
"""

        # Add discussions
        html += '                <h3>Top Highly Voted Comments</h3>\n'

        if q['discussions']:
            for disc_idx, disc in enumerate(q['discussions'], 1):
                username, text, selected_answer, upvotes = disc
                html += f"""
                <button class="collapsible">Comment #{disc_idx} by {escape_html(username)}</button>
                <div class="content">
                    <div class="comment">
                        <div class="upvotes">Upvotes: {upvotes or 0}</div>
"""
                if selected_answer:
                    html += f'                        <div><strong>Selected Answer:</strong> {escape_html(selected_answer)}</div>\n'

                html += f"""                        <p>{escape_html(text)}</p>
                    </div>
                </div>
"""
        else:
            html += '                <div class="no-discussions">No discussions available for this question.</div>\n'

        # Question stats
        html += f"""                <div class="stats">
                    Views: {q['view_count'] or 0} | Replies: {q['reply_count'] or 0}
                </div>
            </div>
        </div>
"""

    html += """    </div>

    <script>
        const collapsibles = document.querySelectorAll(".collapsible");
        collapsibles.forEach(button => {
            button.addEventListener("click", function () {
                this.classList.toggle("active");
                const content = this.nextElementSibling;
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            });
        });
    </script>
</body>
</html>"""

    return html

def main():
    print("Extracting PL-300 questions from database...")
    questions_data, exam_code, exam_name = get_pl300_questions()

    if not questions_data:
        print("No questions found!")
        return

    print(f"\nGenerating HTML page for {len(questions_data)} questions...")
    html_content = generate_html(questions_data, exam_code, exam_name)

    # Write HTML file
    output_file = 'power_bi_pl_300/pl300_questions.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\nHTML page generated successfully!")
    print(f"Output: {output_file}")
    print(f"\nSummary:")
    print(f"  - Total Questions: {len(questions_data)}")
    print(f"  - Exam: {exam_code} - {exam_name}")

if __name__ == '__main__':
    main()
