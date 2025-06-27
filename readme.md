# Automated Book Publication

This project automates the process of scraping, rewriting, and reviewing book chapters from online sources using AI models (Google Gemini API), and provides an interactive workflow for human feedback and editing.

---

## Features

- **Web Scraping:** Extracts chapters from online sources (e.g., Wikisource).
- **AI Rewriting:** Uses Google Gemini models to rewrite or summarize chapters.
- **Semantic Embeddings:** Stores and retrieves chapter embeddings using ChromaDB.
- **Interactive Review:** Prompts users for feedback, ratings, and manual edits.
- **Environment Configuration:** Uses `.env` for API keys and settings.
- **Command-Line Interface:** Easily run and control the workflow from the terminal.

---

## Requirements

- Python 3.8+
- [Google Gemini API access](https://ai.google.dev/)
- [ChromaDB](https://docs.trychroma.com/)
- [Playwright](https://playwright.dev/python/)
- See `requirements.txt` for all dependencies.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone [<repo-url>](https://github.com/RAHULMANDHABALA/Automated_Book_publishing.git)
   ```

2. **Create and activate a virtual environment (recommended):**
   ```sh
   conda create -n bookpub_new python=3.10
   conda activate bookpub_new
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   playwright install
   ```

4. **Set up your `.env` file:**
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

---

## Usage

### Basic Command

```sh
python main.py "<chapter_url>" --chapter-name "<ChapterName>"
```

**Example:**
```sh
python main.py "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1" --chapter-name "Chapter1"
```

### Workflow

1. **Scraping:** The script downloads the chapter text from the provided URL.
2. **AI Rewriting:** The chapter is rewritten using the selected Gemini model.
3. **Review:** You are prompted to rate, comment, and optionally edit the rewritten text.
   - If prompted for an editor, set the `EDITOR` environment variable (e.g., `set EDITOR=notepad` on Windows).
4. **Storage:** The processed chapter and feedback are stored for future use.

---

## Troubleshooting

- **Quota Errors:**  
  If you see `429` errors, you have exceeded your Gemini API quota. Wait for reset, reduce usage, or upgrade your plan.

- **Editor Errors:**  
  If you see `Unable to find a viable editor`, set your `EDITOR` environment variable:
  - Windows: `set EDITOR=notepad`
  - PowerShell: `$env:EDITOR="notepad"`

- **Permission Errors:**  
  If you see `Permission denied` for temp files, ensure your user has full control over `C:\Users\<yourname>\AppData\Local\Temp` and try running your terminal as administrator.

---

## Customization

- **Change AI Model:**  
  Edit `modules/ai_processor.py` and set `self.writer_model = genai.GenerativeModel("models/gemini-2.5-pro")` or another available model.

- **Environment Variables:**  
  Store sensitive keys and configuration in `.env`.

---


