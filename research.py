import os
import requests
from fpdf import FPDF
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import List, Dict, Tuple

load_dotenv()

DOWNLOAD_DIR = "papers"
TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY", "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"
)


def search_and_summarize(query: str) -> Tuple[str, List[str], str]:
    """
    Uses Tavily to search for research papers and generate a comprehensive report.

    Returns:
        Tuple of (report_text, paper_titles, raw_results)
    """
    print(f"\n[Tavily] Searching for: {query}...")

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)

        # Search with advanced depth for better results
        response = client.search(
            query=f"{query} research paper academic",
            search_depth="advanced",
            include_answer="advanced",  # Get AI-generated comprehensive answer
            max_results=5,
        )

        print(f"[Tavily] Found {len(response.get('results', []))} results")

        # Extract paper titles and URLs
        paper_titles = []
        sources_text = []

        for result in response.get("results", []):
            title = result.get("title", "Unknown Title")
            url = result.get("url", "")
            content = result.get("content", "")

            paper_titles.append(title)
            sources_text.append(f"Title: {title}\nURL: {url}\nContent: {content}\n")

        # Get the AI-generated answer
        ai_answer = response.get("answer", "")

        # Combine AI answer with sources
        if ai_answer:
            report = f"""# Research Report: {query}

## Executive Summary
{ai_answer}

## Sources and Detailed Information

"""
        else:
            report = f"""# Research Report: {query}

## Sources and Information

"""

        # Add each source
        for i, source in enumerate(sources_text, 1):
            report += f"### Source {i}\n{source}\n"

        raw_results = "\n".join(sources_text)

        return report, paper_titles, raw_results

    except Exception as e:
        print(f"[Tavily] Error: {str(e)}")
        return f"Error during research: {str(e)}", [], ""


def write_markdown_to_pdf(text: str, usr_input: str) -> str:
    """Write markdown report to PDF with proper formatting using Times New Roman."""
    report_name = "final_report"

    # Create safe filename
    safe_input = "".join(
        c for c in usr_input if c.isalnum() or c in (" ", "-", "_")
    ).rstrip()
    safe_input = safe_input.replace(" ", "_")

    subfolder = os.path.join(DOWNLOAD_DIR, safe_input)
    filename = os.path.join(subfolder, report_name)

    print(f"[Report Writer] Writing markdown report to: {filename}")

    try:
        # Create directory if it doesn't exist
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
            print(f"[DEBUG] Created folder: {subfolder}")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=20)

        # Set margins
        pdf.set_left_margin(20)
        pdf.set_right_margin(20)

        # Process markdown line by line
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Skip empty lines but add spacing
            if not stripped:
                pdf.ln(3)
                i += 1
                continue

            # Check for headers
            if stripped.startswith("# "):
                # H1 Header
                pdf.set_font("Times", "B", 18)
                pdf.ln(5)
                header_text = stripped[2:].strip()
                # Handle inline formatting in headers
                segments = parse_inline_formatting(header_text)
                for segment_text, is_bold, is_italic in segments:
                    if is_bold and is_italic:
                        pdf.set_font("Times", "BI", 18)
                    elif is_bold:
                        pdf.set_font("Times", "B", 18)
                    elif is_italic:
                        pdf.set_font("Times", "I", 18)
                    else:
                        pdf.set_font("Times", "B", 18)
                    pdf.write(
                        8, segment_text.encode("latin-1", "replace").decode("latin-1")
                    )
                pdf.ln(8)
                pdf.ln(3)

            elif stripped.startswith("## "):
                # H2 Header
                pdf.set_font("Times", "B", 14)
                pdf.ln(4)
                header_text = stripped[3:].strip()
                segments = parse_inline_formatting(header_text)
                for segment_text, is_bold, is_italic in segments:
                    if is_bold and is_italic:
                        pdf.set_font("Times", "BI", 14)
                    elif is_bold:
                        pdf.set_font("Times", "B", 14)
                    elif is_italic:
                        pdf.set_font("Times", "I", 14)
                    else:
                        pdf.set_font("Times", "B", 14)
                    pdf.write(
                        6, segment_text.encode("latin-1", "replace").decode("latin-1")
                    )
                pdf.ln(6)
                pdf.ln(2)

            elif stripped.startswith("### "):
                # H3 Header
                pdf.set_font("Times", "B", 12)
                pdf.ln(3)
                header_text = stripped[4:].strip()
                segments = parse_inline_formatting(header_text)
                for segment_text, is_bold, is_italic in segments:
                    if is_bold and is_italic:
                        pdf.set_font("Times", "BI", 12)
                    elif is_bold:
                        pdf.set_font("Times", "B", 12)
                    elif is_italic:
                        pdf.set_font("Times", "I", 12)
                    else:
                        pdf.set_font("Times", "B", 12)
                    pdf.write(
                        5, segment_text.encode("latin-1", "replace").decode("latin-1")
                    )
                pdf.ln(5)
                pdf.ln(1)

            elif stripped.startswith("- ") or stripped.startswith("* "):
                # List item
                pdf.set_font("Times", "", 11)
                pdf.cell(5, 5, "", ln=False)  # Indent
                item_text = stripped[2:].strip()
                pdf.cell(5, 5, "\u2022", ln=False)  # Bullet
                pdf.cell(3, 5, "", ln=False)  # Space after bullet

                # Process inline formatting for list item
                segments = parse_inline_formatting(item_text)
                for segment_text, is_bold, is_italic in segments:
                    if is_bold and is_italic:
                        pdf.set_font("Times", "BI", 11)
                    elif is_bold:
                        pdf.set_font("Times", "B", 11)
                    elif is_italic:
                        pdf.set_font("Times", "I", 11)
                    else:
                        pdf.set_font("Times", "", 11)

                    safe_text = segment_text.encode("latin-1", "replace").decode(
                        "latin-1"
                    )
                    pdf.write(5, safe_text)

                pdf.ln(5)

            else:
                # Regular paragraph with inline formatting
                pdf.set_font("Times", "", 11)
                pdf.ln(2)

                # Process inline formatting
                segments = parse_inline_formatting(stripped)
                for segment_text, is_bold, is_italic in segments:
                    if is_bold and is_italic:
                        pdf.set_font("Times", "BI", 11)
                    elif is_bold:
                        pdf.set_font("Times", "B", 11)
                    elif is_italic:
                        pdf.set_font("Times", "I", 11)
                    else:
                        pdf.set_font("Times", "", 11)

                    safe_text = segment_text.encode("latin-1", "replace").decode(
                        "latin-1"
                    )
                    pdf.write(5, safe_text)

                pdf.ln(5)

            i += 1

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        pdf.output(filename)
        print(f"[Report Writer] Successfully saved markdown report to: {filename}")
        return filename

    except Exception as e:
        error_msg = f"Error creating PDF: {str(e)}"
        print(f"[Report Writer] {error_msg}")
        import traceback

        traceback.print_exc()
        return error_msg


def parse_inline_formatting(text: str):
    """
    Parse inline markdown formatting (**bold**, *italic*, ***bold+italic***).
    Returns list of tuples: (text, is_bold, is_italic)
    """
    segments = []
    current_text = ""
    i = 0

    while i < len(text):
        # Check for bold+italic (***text***)
        if i + 2 < len(text) and text[i : i + 3] == "***":
            if current_text:
                segments.append((current_text, False, False))
                current_text = ""
            # Find closing ***
            end = text.find("***", i + 3)
            if end != -1:
                segments.append((text[i + 3 : end], True, True))
                i = end + 3
            else:
                current_text += text[i]
                i += 1

        # Check for bold (**text**)
        elif i + 1 < len(text) and text[i : i + 2] == "**":
            if current_text:
                segments.append((current_text, False, False))
                current_text = ""
            # Find closing **
            end = text.find("**", i + 2)
            if end != -1:
                segments.append((text[i + 2 : end], True, False))
                i = end + 2
            else:
                current_text += text[i]
                i += 1

        # Check for italic (*text* or _text_)
        elif text[i] == "*" or text[i] == "_":
            if current_text:
                segments.append((current_text, False, False))
                current_text = ""
            # Find closing * or _
            marker = text[i]
            end = text.find(marker, i + 1)
            if end != -1:
                segments.append((text[i + 1 : end], False, True))
                i = end + 1
            else:
                current_text += text[i]
                i += 1

        else:
            current_text += text[i]
            i += 1

    # Add any remaining text
    if current_text:
        segments.append((current_text, False, False))

    # If no formatting found, return the whole text as one segment
    if not segments:
        segments.append((text, False, False))

    return segments


# Keep old function for backward compatibility
def write_to_pdf(text: str, usr_input: str) -> str:
    """Backward compatibility - calls write_markdown_to_pdf"""
    return write_markdown_to_pdf(text, usr_input)


async def run_research(
    query: str, generate_pdf: bool = False
) -> Tuple[str, List[str], str]:
    """
    Main research function that searches and generates a report.

    Args:
        query: Research topic
        generate_pdf: Whether to generate PDF (default False for on-demand)

    Returns:
        Tuple of (pdf_path, paper_titles, report_text)
    """
    print(f"\n{'=' * 60}")
    print(f"Starting research on: {query}")
    print(f"{'=' * 60}\n")

    try:
        # Search and get report
        report_text, paper_titles, raw_results = search_and_summarize(query)

        if not paper_titles:
            print("[System] No papers found.")
            return "", [], report_text

        print(f"[System] Found {len(paper_titles)} papers")

        pdf_path = ""
        if generate_pdf:
            # Write to PDF only if requested
            pdf_path = write_to_pdf(report_text, query)
            if pdf_path and pdf_path.endswith(".pdf"):
                print(f"[System] Report saved successfully!")
            else:
                print(f"[System] Failed to save report: {pdf_path}")

        return pdf_path, paper_titles, report_text

    except Exception as e:
        print(f"[System] Error in research: {str(e)}")
        import traceback

        traceback.print_exc()
        return "", [], f"Error: {str(e)}"


if __name__ == "__main__":
    # Test the function
    import asyncio

    query = input("Enter research topic: ")
    pdf_path, titles, report_text = asyncio.run(run_research(query, generate_pdf=True))
    if pdf_path:
        print(f"\n✓ Report saved to: {pdf_path}")
        print(f"✓ Papers found: {len(titles)}")
    else:
        print(f"\n✓ Papers found: {len(titles)}")
        print("✓ Report generated (PDF not saved)")
