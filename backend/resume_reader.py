import pdfplumber

def read_resume(file):
    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t
        return text
    except Exception:
        # Fallback for plain text resumes or unsupported formats
        try:
            file.seek(0)
            content = file.read()
            if isinstance(content, bytes):
                return content.decode("utf-8", errors="ignore")
            return str(content)
        except Exception:
            return ""
