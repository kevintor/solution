#!/usr/bin/env python3
"""
Convert all Markdown files to PDF using WeasyPrint
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def md_to_pdf(md_file, output_file, title=""):
    """Convert markdown file to PDF"""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
    
    # Add styling
    css = '''
    @page {
        size: A4;
        margin: 2cm;
        @bottom-center {
            content: counter(page);
            font-size: 10pt;
        }
    }
    body {
        font-family: 'DejaVu Sans', 'Arial', sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
    }
    h1 {
        color: #1e3a5f;
        font-size: 24pt;
        border-bottom: 3px solid #1e3a5f;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    h2 {
        color: #2c5282;
        font-size: 18pt;
        border-bottom: 2px solid #4a90d9;
        padding-bottom: 5px;
        margin-top: 25px;
    }
    h3 {
        color: #2d3748;
        font-size: 14pt;
        margin-top: 20px;
    }
    code {
        background: #f5f5f5;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: 'DejaVu Sans Mono', monospace;
        font-size: 10pt;
    }
    pre {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        border-left: 4px solid #4a90d9;
    }
    pre code {
        background: none;
        padding: 0;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background: #1e3a5f;
        color: white;
    }
    tr:nth-child(even) {
        background: #f9f9f9;
    }
    blockquote {
        border-left: 4px solid #4a90d9;
        margin: 15px 0;
        padding: 10px 20px;
        background: #f8f9fa;
        font-style: italic;
    }
    ul, ol {
        margin: 10px 0;
        padding-left: 25px;
    }
    li {
        margin: 5px 0;
    }
    .cover {
        text-align: center;
        padding-top: 150px;
    }
    .cover h1 {
        border: none;
        font-size: 32pt;
        color: #1e3a5f;
    }
    '''
    
    # Wrap in HTML structure
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    {html_content}
</body>
</html>'''
    
    # Convert to PDF
    font_config = FontConfiguration()
    HTML(string=full_html).write_pdf(output_file, stylesheets=[CSS(string=css)], font_config=font_config)
    
    file_size = os.path.getsize(output_file)
    print(f"✓ Created: {output_file} ({file_size:,} bytes)")
    return output_file

def main():
    base_dir = '/root/.openclaw/workspace/output/servicenow-copilot-routing/docs'
    output_dir = '/root/.openclaw/workspace/output/servicenow-copilot-routing/pdf'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Files to convert
    files = [
        ('README.md', 'ServiceNow-Copilot-Overview.pdf', 'ServiceNow + Copilot Overview'),
        ('servicenow-copilot-architecture.md', 'ServiceNow-Copilot-Architecture.pdf', 'Architecture Design'),
        ('servicenow-copilot-implementation-guide.md', 'ServiceNow-Copilot-Implementation.pdf', 'Implementation Guide'),
        ('feasibility-analysis.md', 'ServiceNow-Copilot-Feasibility.pdf', 'Feasibility Analysis'),
    ]
    
    print("Converting Markdown files to PDF...")
    print("=" * 50)
    
    for md_name, pdf_name, title in files:
        md_path = os.path.join(base_dir, md_name)
        pdf_path = os.path.join(output_dir, pdf_name)
        
        if os.path.exists(md_path):
            try:
                md_to_pdf(md_path, pdf_path, title)
            except Exception as e:
                print(f"✗ Error converting {md_name}: {e}")
        else:
            print(f"✗ File not found: {md_path}")
    
    print("=" * 50)
    print("Conversion complete!")
    
    # List generated files
    print("\nGenerated PDFs:")
    for f in os.listdir(output_dir):
        if f.endswith('.pdf'):
            size = os.path.getsize(os.path.join(output_dir, f))
            print(f"  - {f} ({size:,} bytes)")

if __name__ == '__main__':
    main()
