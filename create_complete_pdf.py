#!/usr/bin/env python3
"""
Convert Markdown to PDF with embedded images
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os
import re

def process_markdown(md_content, base_dir):
    """Process markdown content - fix image paths"""
    # Convert relative image paths to absolute paths
    def fix_image_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        if not img_path.startswith('http') and not img_path.startswith('/'):
            # Convert relative to absolute
            abs_path = os.path.join(base_dir, img_path)
            if os.path.exists(abs_path):
                return f'![{alt_text}](file://{abs_path})'
        return match.group(0)
    
    # Fix markdown image syntax
    md_content = re.sub(r'!\[(.*?)\]\((.*?)\)', fix_image_path, md_content)
    return md_content

def md_to_pdf(md_file, output_file, title="", base_dir=""):
    """Convert markdown file to PDF with images"""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Process markdown for images
    md_content = process_markdown(md_content, base_dir)
    
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
        font-size: 9pt;
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
    img {
        max-width: 100%;
        height: auto;
        margin: 15px 0;
        border: 1px solid #ddd;
        border-radius: 5px;
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
    '''
    
    # Wrap in HTML structure with proper encoding
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
    HTML(string=full_html, base_url=base_dir).write_pdf(
        output_file, 
        stylesheets=[CSS(string=css)], 
        font_config=font_config
    )
    
    file_size = os.path.getsize(output_file)
    print(f"✓ Created: {output_file} ({file_size:,} bytes)")
    return output_file

def create_combined_pdf():
    """Create one combined PDF with all content and images"""
    
    base_dir = '/root/.openclaw/workspace/output/servicenow-copilot-routing'
    docs_dir = os.path.join(base_dir, 'docs')
    diagrams_dir = os.path.join(base_dir, 'diagrams')
    output_file = os.path.join(base_dir, 'pdf', 'ServiceNow-Copilot-Complete-Guide.pdf')
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Read all markdown files
    files_order = [
        ('README.md', 'Project Overview'),
        ('servicenow-copilot-architecture.md', 'System Architecture'),
        ('servicenow-copilot-implementation-guide.md', 'Implementation Guide'),
        ('feasibility-analysis.md', 'Feasibility Analysis'),
    ]
    
    all_html = []
    
    # Cover page
    cover_html = '''
    <div style="text-align: center; padding-top: 100px;">
        <h1 style="font-size: 36pt; color: #1e3a5f; border: none;">ServiceNow + Microsoft Copilot</h1>
        <h1 style="font-size: 36pt; color: #1e3a5f; border: none;">AI Incident Routing</h1>
        <h2 style="border: none; color: #666;">Complete Implementation Guide</h2>
        <p style="margin-top: 50px; color: #999;">Generated: March 8, 2026</p>
        <p style="color: #999;">Version 1.0</p>
    </div>
    <div style="page-break-after: always;"></div>
    '''
    all_html.append(cover_html)
    
    # Add table of contents
    toc_html = '<h1>Table of Contents</h1><ul>'
    for _, title in files_order:
        toc_html += f'<li>{title}</li>'
    toc_html += '</ul><div style="page-break-after: always;"></div>'
    all_html.append(toc_html)
    
    # Process each markdown file
    for filename, title in files_order:
        filepath = os.path.join(docs_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Process markdown for images
            md_content = process_markdown(md_content, base_dir)
            
            # Convert to HTML
            html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            
            # Add section header
            section_html = f'<h1>{title}</h1>' + html_content
            section_html += '<div style="page-break-after: always;"></div>'
            all_html.append(section_html)
    
    # Add diagrams section
    diagrams_html = '<h1>Architecture Diagrams</h1>'
    diagram_files = [
        ('01-architecture-overview.jpg', 'Overall System Architecture'),
        ('02-incident-flow.jpg', 'Incident Creation Data Flow'),
        ('03-copilot-interaction.jpg', 'Copilot Interaction Flow'),
        ('04-rag-process.jpg', 'RAG Retrieval Process'),
        ('05-p1-notification.jpg', 'P1 Notification Workflow'),
        ('06-component-relation.jpg', 'Component Relationship'),
    ]
    
    for img_file, caption in diagram_files:
        img_path = os.path.join(diagrams_dir, img_file)
        if os.path.exists(img_path):
            diagrams_html += f'<h2>{caption}</h2>'
            diagrams_html += f'<img src="file://{img_path}" style="max-width: 100%;" />'
            diagrams_html += '<div style="page-break-after: always;"></div>'
    
    all_html.append(diagrams_html)
    
    # Combine all HTML
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ServiceNow + Copilot Complete Guide</title>
</head>
<body>
    {''.join(all_html)}
</body>
</html>'''
    
    # CSS
    css = '''
    @page {
        size: A4;
        margin: 2cm;
        @bottom-center {
            content: counter(page);
            font-size: 10pt;
            color: #666;
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
        page-break-before: always;
    }
    h1:first-of-type {
        page-break-before: avoid;
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
        font-size: 9pt;
    }
    pre {
        background: #f5f5f5;
        padding: 12px;
        border-radius: 5px;
        overflow-x: auto;
        border-left: 4px solid #4a90d9;
        font-size: 8pt;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    pre code {
        background: none;
        padding: 0;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        font-size: 10pt;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 6px;
        text-align: left;
    }
    th {
        background: #1e3a5f;
        color: white;
    }
    tr:nth-child(even) {
        background: #f9f9f9;
    }
    img {
        max-width: 100%;
        max-height: 500px;
        height: auto;
        margin: 15px auto;
        display: block;
        border: 1px solid #ddd;
        border-radius: 5px;
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
    '''
    
    # Generate PDF
    print("Generating combined PDF with embedded images...")
    font_config = FontConfiguration()
    HTML(string=full_html, base_url=base_dir).write_pdf(
        output_file,
        stylesheets=[CSS(string=css)],
        font_config=font_config
    )
    
    file_size = os.path.getsize(output_file)
    print(f"✓ Created: {output_file}")
    print(f"  Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    return output_file

if __name__ == '__main__':
    create_combined_pdf()
    print("\nDone! PDF includes all documentation and 6 architecture diagrams.")
