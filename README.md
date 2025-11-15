# Microsoft PL-300 Power BI Data Analyst Exam Questions

## Overview
This folder contains all extracted questions, answers, options, images, and discussions for the Microsoft PL-300 (Power BI Data Analyst) certification exam.

## Contents

### Files
- **pl300_questions.html** - Interactive HTML page with all 296 questions
- **extract_pl300.py** - Python script used to extract data from database
- **PL-300/** - Folder containing all question images (323 images across 151 questions)

## Statistics

| Metric | Count |
|--------|-------|
| Total Questions | 296 |
| Total Images | 323 |
| Questions with Images | 151 |
| Question Directories | 151 |

## HTML Page Features

The `pl300_questions.html` file provides:

### Question Display
- **Collapsible interface** - Click any question to expand/collapse
- **Question text** with formatting
- **Embedded images** - All images are displayed inline
- **Answer choices** with correct answers highlighted in green
- **Suggested answers** shown in a highlighted box
- **Explanations** for each answer

### Discussion Comments
- **Top 3 highly voted comments** for each question
- **Collapsible comments** - Click to expand/collapse
- **Upvote counts** displayed for each comment
- **Selected answers** from community members
- **Username** of commenter

### Navigation
- **Question numbering** for easy reference
- **Stats** showing views and replies for each question
- **Exam info** at the top showing total question count

## How to Use

1. **Open the HTML file**:
   ```
   power_bi_pl_300/pl300_questions.html
   ```

2. **Navigate**:
   - Click question headers to expand/collapse questions
   - Click comment headers to expand/collapse discussions
   - Scroll through all 296 questions

3. **Study tips**:
   - Review questions sequentially
   - Check the suggested answer first
   - Read the explanation to understand why
   - Review highly voted community comments for additional insights
   - Pay special attention to questions with images

## Images

All images are organized in the `PL-300/` folder by discussion ID:
```
PL-300/
├── <discussion_id_1>/
│   ├── question_1.png
│   ├── option_A_1.png
│   └── explanation_1.png
├── <discussion_id_2>/
│   └── question_1.png
...
```

Image types:
- **question_X.png** - Images embedded in question text
- **option_X_Y.png** - Images in answer options
- **explanation_X.png** - Images in answer explanations

## Data Source

Extracted from database: `databanter_db`
- **Exam Code**: PL-300
- **Exam Name**: Microsoft Power BI Data Analyst
- **Provider**: Microsoft
- **Extraction Date**: November 15, 2025

## Re-generating the HTML

To regenerate the HTML page with updated data:

```bash
python power_bi_pl_300/extract_pl300.py
```

This will:
1. Query the database for latest PL-300 questions
2. Extract all related data (answers, options, images, discussions)
3. Generate a new `pl300_questions.html` file

## Notes

- All questions include top 3 highly voted community comments
- Some questions may not have discussions available
- Images are referenced using relative paths
- The HTML file is fully self-contained (except for images)
- Works in any modern web browser without internet connection

## Browser Compatibility

Tested and working in:
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Safari

## License

This data is extracted from ExamTopics.com for educational purposes only.
