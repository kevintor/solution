#!/usr/bin/env python3
"""
Generate complete PDF for ServiceNow Copilot v2 (with Historical Case Learning)
"""

from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.cell(0, 10, 'ServiceNow + Copilot with Historical Case Learning', 0, new_y='NEXT', align='C')
            
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, align='C')

def main():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Cover
    pdf.add_page()
    pdf.set_fill_color(30, 58, 95)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_y(70)
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, 'ServiceNow + Microsoft Copilot', 0, new_y='NEXT', align='C')
    pdf.cell(0, 15, 'AI Incident Routing', 0, new_y='NEXT', align='C')
    pdf.set_font('helvetica', 'B', 22)
    pdf.cell(0, 15, 'with Historical Case Learning', 0, new_y='NEXT', align='C')
    pdf.set_y(180)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 10, 'Enhanced Edition - History Weight > AI Weight', 0, new_y='NEXT', align='C')
    pdf.set_y(220)
    pdf.cell(0, 10, 'Generated: March 8, 2026 | Version 2.0', 0, new_y='NEXT', align='C')
    
    # Executive Summary
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Executive Summary', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'This enhanced solution adds Historical Case Learning to the AI-driven incident routing system. The system prioritizes historical similar cases over AI recommendations, achieving higher accuracy and faster ROI.')
    pdf.ln(5)
    
    # Key Enhancement
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Key Enhancement: History > AI', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'Traditional AI-only routing relies on KB articles. This enhanced version analyzes 12 months of resolved incidents, finds similar cases, and uses historical assignment patterns with 70% weight, complementing AI recommendations at 30% weight.')
    pdf.ln(5)
    
    # Comparison Table
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Version Comparison', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 9)
    
    # Table header
    pdf.set_fill_color(30, 58, 95)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(50, 8, 'Feature', 1, 0, 'C', True)
    pdf.cell(50, 8, 'v1.0 (AI Only)', 1, 0, 'C', True)
    pdf.cell(50, 8, 'v2.0 (History+AI)', 1, 0, 'C', True)
    pdf.cell(40, 8, 'Improvement', 1, 1, 'C', True)
    
    # Table rows
    pdf.set_text_color(0, 0, 0)
    rows = [
        ('Decision Source', 'KB + AI', 'History + AI', '+Historical'),
        ('History Weight', '0%', '70%', 'Major'),
        ('AI Weight', '100%', '30%', 'Supporting'),
        ('Expected Accuracy', '~75%', '~90%', '+15%'),
        ('Implementation', '4-8 weeks', '6-10 weeks', '+2 weeks'),
        ('ROI Period', '12-18 months', '6-12 months', 'Faster'),
    ]
    
    for i, (feature, v1, v2, imp) in enumerate(rows):
        fill = i % 2 == 1
        pdf.set_fill_color(240, 240, 240) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(50, 7, feature, 1, 0, 'L', fill)
        pdf.cell(50, 7, v1, 1, 0, 'C', fill)
        pdf.cell(50, 7, v2, 1, 0, 'C', fill)
        pdf.cell(40, 7, imp, 1, 1, 'C', fill)
    
    pdf.ln(10)
    
    # Architecture
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Enhanced Architecture', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'The enhanced architecture adds a Historical Case Learning Layer between the Business Logic and AI Service layers. This layer analyzes resolved incidents from the past 12 months to identify patterns and make routing recommendations.')
    pdf.ln(5)
    
    # New Components
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'New Components', 0, new_y='NEXT')
    
    components = [
        ('HistoricalCaseAnalyzer', 'Script Include that finds similar resolved incidents using Jaccard similarity and keyword matching'),
        ('EnhancedAIRoutingEngine', 'Updated routing engine that fuses historical and AI recommendations with configurable weights'),
        ('Similarity Matching', 'Algorithm comparing incident descriptions, categories, and CI information'),
        ('Pattern Recognition', 'Statistical analysis of assignment groups, resolution times, and success rates'),
    ]
    
    for name, desc in components:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(0, 7, name, 0, new_y='NEXT')
        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(0, 5, desc)
        pdf.ln(2)
    
    # Decision Algorithm
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Decision Algorithm', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'The routing decision follows a three-tier approach:')
    pdf.ln(3)
    
    algorithm_steps = [
        ('1. Historical Analysis', 'Query resolved incidents from past 12 months with same CI. Calculate similarity scores using keyword matching. Identify most common assignment patterns.'),
        ('2. Confidence Check', 'IF confidence >= 75% AND samples >= 5: Use History ONLY (100%). ELSE IF history exists: Use Hybrid (History 70% + AI 30%). ELSE: Use AI ONLY.'),
        ('3. Weighted Fusion', 'For hybrid decisions, calculate: FINAL = (History × 0.7) + (AI × 0.3). If history and AI agree, boost confidence by 15%.'),
        ('4. Update Incident', 'Set assignment_group, add work notes with decision trail (method, confidence, reasoning), log for analysis.'),
    ]
    
    for title, desc in algorithm_steps:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(0, 7, title, 0, new_y='NEXT')
        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(0, 5, desc)
        pdf.ln(3)
    
    # Implementation
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Implementation Summary', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'The enhanced solution requires two new Script Includes and updates to the existing Business Rule. Total additional development: ~2 weeks.')
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Key Scripts', 0, new_y='NEXT')
    
    scripts = [
        ('HistoricalCaseAnalyzer', 'Finds similar cases using Jaccard similarity, keyword extraction, and pattern analysis. Returns confidence score and assignment recommendation.'),
        ('EnhancedAIRoutingEngine', 'Orchestrates history analysis and AI calls. Implements weight fusion algorithm. Returns final recommendation with decision method.'),
    ]
    
    for name, desc in scripts:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(0, 7, name, 0, new_y='NEXT')
        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(0, 5, desc)
        pdf.ln(2)
    
    # Data Requirements
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Data Requirements', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    
    data_reqs = [
        'Minimum 6 months of resolved incident data',
        'At least 100 resolved cases per major CI',
        'Complete assignment_group and resolution fields',
        'Data quality: >80% complete records',
    ]
    
    for req in data_reqs:
        pdf.cell(5, 6, '-', 0)
        pdf.cell(0, 6, req, 0, new_y='NEXT')
    
    # Feasibility
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Feasibility Analysis', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    findings = [
        ('Technical Feasibility: HIGH', [
            'Similarity algorithms are mature and simple',
            'No external ML services required',
            'All processing within ServiceNow platform',
            'Performance: 50-100ms per analysis',
        ]),
        ('Data Feasibility: CONDITIONAL', [
            'Requires 6+ months of historical data',
            'Data quality must be >80% complete',
            'If data insufficient, auto-fallback to AI-only',
            'Data accumulates naturally over time',
        ]),
        ('Implementation Feasibility: HIGH', [
            'Additional 2 weeks development time',
            'No new plugins required',
            'Can be added to existing v1.0 deployment',
            'Rollback possible if issues arise',
        ]),
    ]
    
    for title, items in findings:
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(30, 100, 60)
        pdf.cell(0, 8, title, 0, new_y='NEXT')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('helvetica', '', 9)
        for item in items:
            pdf.cell(5, 5, '-', 0)
            pdf.cell(0, 5, item, 0, new_y='NEXT')
        pdf.ln(2)
    
    # Conclusion
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 12, 'Conclusion and Recommendations', 0, new_y='NEXT')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Final Verdict: RECOMMENDED', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, 'The enhanced solution with Historical Case Learning is technically feasible, delivers higher accuracy (~90% vs ~75%), and achieves faster ROI (6-12 months vs 12-18 months).')
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Deployment Strategy', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    
    strategy = [
        ('If Historical Data > 6 months:', 'Deploy Enhanced Version (v2.0) directly'),
        ('If Historical Data < 6 months:', 'Deploy v1.0 first, upgrade to v2.0 after 3 months'),
        ('Recommended Approach:', 'Phased rollout - start with 70/30 weights, adjust based on results'),
    ]
    
    for condition, action in strategy:
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(0, 6, condition, 0, new_y='NEXT')
        pdf.set_font('helvetica', '', 9)
        pdf.cell(10, 6, '', 0)
        pdf.cell(0, 6, action, 0, new_y='NEXT')
        pdf.ln(2)
    
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, 'Expected Outcomes', 0, new_y='NEXT')
    pdf.set_font('helvetica', '', 10)
    
    outcomes = [
        'Routing Accuracy: 75% → 90% (+15%)',
        'Mean Time to Resolve: -20% improvement',
        'Manual Reassignment: 25% → 10% (-15%)',
        'User Satisfaction: +25% improvement',
        'ROI Achievement: 6-12 months',
    ]
    
    for outcome in outcomes:
        pdf.cell(5, 6, '-', 0)
        pdf.cell(0, 6, outcome, 0, new_y='NEXT')
    
    # Save
    output_file = '/root/.openclaw/workspace/output/servicenow-copilot-routing-v2/pdf/ServiceNow-Copilot-v2-Historical-Learning-Complete-Guide.pdf'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    pdf.output(output_file)
    
    size = os.path.getsize(output_file)
    print(f'PDF generated: {output_file}')
    print(f'Size: {size:,} bytes ({size/1024:.1f} KB)')
    print(f'Pages: {pdf.page_no()}')

if __name__ == '__main__':
    main()
