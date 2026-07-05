import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List

import pymupdf
import pymupdf4llm
from dotenv import load_dotenv


load_dotenv()



def pdf_to_markdown(pdf_path: str) -> Dict[str, str]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file '{pdf_path}' does not exist")

    doc = pymupdf.open(pdf_path)
    markdown = pymupdf4llm.to_markdown(
        doc,
        header=False,
        footer=False,
        pages=list(range(doc.page_count)),
    )
    return {
        "markdown": markdown,
        "file_name": Path(pdf_path).stem,
    }


def chunking(md_obj: Dict[str, str]) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    section = ""
    content = ""

    for line in md_obj.get("markdown", "").splitlines():
        if re.match(r"^##\s+[^**]", line):
            if content:
                chunks.append(
                    {
                        "section": section,
                        "content": content.strip(),
                        "file_name": md_obj.get("file_name", "unknown"),
                    }
                )
                content = ""
            section = line.strip()
        elif line.strip():
            content += line.strip() + " "

    if content:
        chunks.append(
            {
                "section": section,
                "content": content.strip(),
                "file_name": md_obj.get("file_name", "unknown"),
            }
        )

    for idx, chunk in enumerate(chunks):
        chunk["chunk_index"] = idx

    return chunks

