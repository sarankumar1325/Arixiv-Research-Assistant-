# Test script for markdown PDF generation
import sys

sys.path.insert(
    0, r"C:\Users\GANES\Downloads\ARXIV RESEARCH ASSISTANT\Arxiv-Research-Assistant"
)

from research import write_markdown_to_pdf

# Sample markdown text for testing
test_markdown = """# Research Report: Machine Learning

## Executive Summary

This is a **comprehensive** report on machine learning advances. The field has grown *exponentially* in recent years.

### Key Findings

- Deep learning models show **superior performance**
- Transfer learning reduces training time *significantly*
- Neural networks can solve complex problems

## Detailed Analysis

The research indicates that **artificial intelligence** and *machine learning* are transforming industries. ***Important breakthroughs*** have been made in:

- Natural language processing
- Computer vision
- Reinforcement learning

### Source 1

Title: Deep Learning Revolution
URL: https://example.com/paper1
Content: This paper discusses **neural networks** and their applications.

### Source 2

Title: Advanced ML Techniques
URL: https://example.com/paper2
Content: *Innovative approaches* to machine learning.

## Conclusion

The future of **AI** is *bright* and full of ***exciting possibilities***.
"""

# Test the PDF generation
print("Testing markdown PDF generation...")
result = write_markdown_to_pdf(test_markdown, "test_ml_research_v2")

if result.endswith(".pdf"):
    print(f"✓ PDF generated successfully: {result}")
else:
    print(f"✗ Error: {result}")
