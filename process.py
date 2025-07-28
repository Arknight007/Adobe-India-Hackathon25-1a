import json
from pathlib import Path
import fitz
INPUT_DIR = Path("sample_dataset/pdfs")
OUTPUT_DIR = Path("sample_dataset/outputs")
def is_heading(text: str, size: float) -> str | None:
    if size > 20:
        return "H1"
    if size > 16:
        return "H2"
    if size > 13:
        return "H3"
    return None
def extract_outline(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    seen = set()
    headings = []
    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    txt = span["text"].strip()
                    if not txt or txt in seen:
                        continue
                    seen.add(txt)
                    lvl = is_heading(txt, span["size"])
                    if lvl:
                        headings.append({
                            "level": lvl,
                            "text": txt,
                            "page": page_num
                        })
    title = headings[0]["text"] if headings else pdf_path.stem
    return {"title": title, "outline": headings}
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for pdf_file in INPUT_DIR.glob("*.pdf"):
        result = extract_outline(pdf_file)
        out_path = OUTPUT_DIR / f"{pdf_file.stem}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()