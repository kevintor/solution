#!/usr/bin/env python3
"""
ServiceNow + Microsoft Copilot AI Incident Routing
PDF Document Generator - Simplified Version
"""

from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.cell(0, 10, 'ServiceNow + Microsoft Copilot Implementation Guide', 0, new_y='NEXT', align='C')
            
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, align='C')

def main():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Cover Page
    pdf.add_page()
    pdf.set_fill_color(30, 58, 95)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_y(80)
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, 'ServiceNow + Microsoft Copilot', 0, new_y='NEXT', align='C')
    pdf.cell(0, 20, 'AI Incident Routing', 0, new_y='NEXT', align='C')
    pdf.set_y(180)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 10, 'Implementation Guide & Architecture Design', 0, new_y='NEXT', align='C')
    pdf.set_y(220)
    pdf.cell(0, 10, 'Generated: March 8, 2026 | Version 1.0', 0, new_y='NEXT', align='C')
    
    # Content Pages
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Executive Summary', 0, new_y='NEXT')
    pdf.set_draw_color(30, 58, 95)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, 'This document provides a comprehensive guide for implementing an AI-driven incident routing system that integrates ServiceNow with Microsoft Copilot. The solution leverages Retrieval-Augmented Generation (RAG) to automatically recommend assignment groups based on Configuration Item (CI) associated Knowledge Base articles.')
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Key Objectives', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    objectives = [
        'Intelligent routing based on KB content analysis',
        'Natural language interface through Copilot',
        'Automated P1 incident notification',
        'Seamless integration with existing ITSM workflows'
    ]
    for obj in objectives:
        pdf.cell(5, 6, '-', 0)
        pdf.cell(0, 6, obj, 0, new_y='NEXT')
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Prerequisites', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    prereqs = [
        'ServiceNow: Xanadu Patch 1+ (Zurich Patch 2+ recommended)',
        'Now Assist Pro Plus license',
        'Microsoft 365 Copilot subscription',
        'Azure OpenAI Service (optional, for custom LLM)'
    ]
    for prereq in prereqs:
        pdf.cell(5, 6, '-', 0)
        pdf.cell(0, 6, prereq, 0, new_y='NEXT')
    
    # Architecture
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'System Architecture', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'The system architecture consists of four layers:')
    pdf.ln(3)
    
    layers = [
        ('Presentation Layer', 'User interaction interfaces including ServiceNow Incident Form, Microsoft Teams Copilot, and Virtual Agent/Now Assist chatbot.'),
        ('Business Logic Layer', 'Core processing components including Business Rules, AI Routing Engine, Notification Engine, and Flow Designer workflows.'),
        ('AI Service Layer', 'Microsoft Azure OpenAI Service providing GPT-4/GPT-4o models, RAG Engine for knowledge retrieval, and Embeddings for semantic search.'),
        ('Data Layer', 'ServiceNow tables: Incident, KB Articles, CMDB (CI), and AI Search Index.')
    ]
    
    for title, desc in layers:
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 7, title, 0, new_y='NEXT')
        pdf.set_font('helvetica', '', 10)
        pdf.multi_cell(0, 6, desc)
        pdf.ln(3)
    
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Architecture Diagrams', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    diagrams = [
        '01-architecture-overview.jpg - Overall system architecture',
        '02-incident-flow.jpg - Incident creation data flow',
        '03-copilot-interaction.jpg - Copilot interaction sequence',
        '04-rag-process.jpg - RAG retrieval process',
        '05-p1-notification.jpg - P1 notification workflow',
        '06-component-relation.jpg - Component relationship'
    ]
    for diagram in diagrams:
        pdf.cell(5, 6, '-', 0)
        pdf.cell(0, 6, diagram, 0, new_y='NEXT')
    
    # Implementation
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Implementation Summary', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'Complete implementation steps are provided in separate documentation files. Key components include:')
    pdf.ln(3)
    
    impl_items = [
        ('Plugin Installation', 'Now Assist, Virtual Agent, IntegrationHub, AI Search'),
        ('Azure OpenAI Configuration', 'REST Message setup, API key configuration'),
        ('CI-KB Association', 'CMDB field extension, KB article linking'),
        ('AI Routing Engine', 'Script Include development with RAG capabilities'),
        ('P1 Notification', 'Flow Designer workflow, Notification rules'),
        ('Copilot Integration', 'OAuth setup, Teams integration, Virtual Agent topics')
    ]
    
    for title, desc in impl_items:
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 7, title, 0, new_y='NEXT')
        pdf.set_font('helvetica', '', 10)
        pdf.multi_cell(0, 6, desc)
        pdf.ln(2)
    
    # Feasibility
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Feasibility Analysis', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'Based on comprehensive analysis, the integration is technically feasible with the following findings:')
    pdf.ln(5)
    
    findings = [
        ('Technical Feasibility: HIGH', [
            'Native support in Xanadu/Zurich versions',
            'Mature integration with Microsoft Copilot',
            'Well-documented APIs and configuration options'
        ]),
        ('Cost Considerations', [
            'Now Assist Plus license: +30-60% cost increase',
            'Microsoft 365 Copilot: ~$30/user/month',
            'Estimated 100-user annual cost: ~$205,000'
        ]),
        ('Risk Assessment: LOW-MEDIUM', [
            'Data privacy: Zero persistence, PII can be masked',
            'Fallback mechanisms: Traditional support channels remain',
            'Gradual rollout reduces implementation risk'
        ])
    ]
    
    for title, items in findings:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(30, 100, 60)
        pdf.cell(0, 8, title, 0, new_y='NEXT')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('helvetica', '', 10)
        for item in items:
            pdf.cell(5, 6, '-', 0)
            pdf.cell(0, 6, item, 0, new_y='NEXT')
        pdf.ln(3)
    
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 8, 'Conclusion', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, 'The integration is recommended for organizations with ServiceNow Xanadu+ or Zurich, existing Microsoft 365 Copilot licenses, and budget capacity for Now Assist Plus licensing. Implementation timeline: 4-8 weeks.')
    
    # Appendix
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Document References', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'All project files are located in /output/ directory:')
    pdf.ln(3)
    
    files = [
        'servicenow-copilot-architecture.md - Architecture design document',
        'servicenow-copilot-implementation-guide.md - Detailed implementation steps (30KB+)',
        'feasibility-analysis.md - Complete feasibility study',
        'nano-banana-prompts.md - Diagram generation prompts',
        'diagrams/01-06.jpg - Architecture diagrams (6 files)'
    ]
    for f in files:
        pdf.cell(5, 6, '-', 0)
        pdf.cell(0, 6, f, 0, new_y='NEXT')
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Support Resources', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    resources = [
        'ServiceNow Support: support.servicenow.com',
        'Microsoft Copilot: docs.microsoft.com/copilot',
        'Azure OpenAI: azure.microsoft.com/openai'
    ]
    for r in resources:
        pdf.cell(5, 6, '-', 0)
        pdf.cell(0, 6, r, 0, new_y='NEXT')
    
    # Save
    output_path = '/root/.openclaw/workspace/output/ServiceNow-Copilot-AI-Incident-Routing-Implementation-Guide.pdf'
    pdf.output(output_path)
    
    size = os.path.getsize(output_path)
    print(f'PDF generated successfully!')
    print(f'Path: {output_path}')
    print(f'Size: {size:,} bytes ({size/1024:.1f} KB)')
    print(f'Pages: {pdf.page_no()}')

if __name__ == '__main__':
    main()
