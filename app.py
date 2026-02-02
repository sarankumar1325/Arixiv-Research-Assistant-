from flask import Flask, render_template, request, jsonify, send_file
from research import run_research
import asyncio
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/research", methods=["POST"])
def research():
    query = request.form["query"]
    print(f"[Flask] Received research request for query: {query}")
    try:
        print("[Flask] Starting research process...")
        pdf_path, paper_titles, report_text = asyncio.run(
            run_research(query, generate_pdf=False)
        )
        print(f"[Flask] Research completed. Found {len(paper_titles)} papers")
        if paper_titles:
            return jsonify(
                {
                    "success": True,
                    "paper_titles": paper_titles,
                    "report_text": report_text,
                    "query": query,
                    "message": "Research completed successfully!",
                }
            )
        else:
            return jsonify(
                {"success": False, "error": "No papers found for this topic."}
            )
    except Exception as e:
        print(f"[Flask] Error in research: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": f"Error: {str(e)}"})


@app.route("/export_pdf", methods=["POST"])
def export_pdf():
    """Generate PDF on-demand with markdown formatting"""
    data = request.get_json()
    query = data.get("query", "")
    report_text = data.get("report_text", "")

    print(f"[Flask] Received PDF export request for: {query}")

    try:
        from research import write_markdown_to_pdf

        pdf_path = write_markdown_to_pdf(report_text, query)

        if pdf_path and pdf_path.endswith(".pdf") and os.path.exists(pdf_path):
            return jsonify(
                {
                    "success": True,
                    "pdf_path": pdf_path,
                    "download_url": f"/download/{pdf_path}",
                }
            )
        else:
            return jsonify({"success": False, "error": "Failed to generate PDF"})
    except Exception as e:
        print(f"[Flask] Error generating PDF: {str(e)}")
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)})


@app.route("/download/<path:filename>")
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5000)
