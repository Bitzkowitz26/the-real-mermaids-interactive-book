#!/usr/bin/env python3
"""
Professional Real Estate Underwriting Report Generator
Property: 3015 North Oakwood Avenue, Muncie, Indiana
"""

import pandas as pd
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

class ProfessionalUnderwritingReport:
    def __init__(self):
        self.property_address = "3015 North Oakwood Avenue, Muncie, Indiana 47304"
        self.analysis_date = datetime.now()
        self.recipient_email = "Benitzkowitz@agenticforce.dev"
        
    def create_pdf_report(self):
        """Generate comprehensive PDF report"""
        filename = "/workspace/Real_Estate_Underwriting_Report_3015_N_Oakwood.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=5
        )
        
        # Build story
        story = []
        
        # Title Page
        story.append(Paragraph("PROFESSIONAL REAL ESTATE", title_style))
        story.append(Paragraph("UNDERWRITING REPORT", title_style))
        story.append(Spacer(1, 0.5*inch))
        
        story.append(Paragraph(f"<b>Property Address:</b><br/>{self.property_address}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"<b>Analysis Date:</b> {self.analysis_date.strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Paragraph(f"<b>Prepared for:</b> {self.recipient_email}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
        executive_summary = """
        This comprehensive underwriting analysis evaluates the investment potential of 3015 North Oakwood Avenue, 
        Muncie, Indiana. The property has been analyzed under three potential scenarios: Single Family Rental, 
        Duplex, and Multi-Family configuration. Based on current market conditions and financial modeling, 
        the Multi-Family scenario presents the strongest investment opportunity with a 9.9% cap rate and 
        13.9% cash-on-cash return.
        
        <b>Key Findings:</b>
        • Multi-Family configuration shows superior returns across all metrics
        • Duplex scenario meets minimum investment thresholds
        • Single Family rental shows marginal returns requiring price negotiation
        • Muncie market presents challenges due to population decline but benefits from Ball State University proximity
        """
        story.append(Paragraph(executive_summary, styles['Normal']))
        story.append(PageBreak())
        
        # Market Analysis
        story.append(Paragraph("MARKET ANALYSIS", heading_style))
        market_analysis = """
        <b>Muncie, Indiana Market Overview:</b><br/>
        • Population: 65,194 (2020 Census) - 7% decline from 2010<br/>
        • Economic Base: Ball State University (16,000+ students) and manufacturing<br/>
        • Median Home Value: Approximately $85,000<br/>
        • Rental Market: Driven by university housing demand<br/>
        • Investment Climate: Moderate risk due to population decline, offset by stable university presence<br/><br/>
        
        <b>Rental Rate Analysis:</b><br/>
        • Studio: $400-$550 (avg $475)<br/>
        • 1BR: $450-$650 (avg $550)<br/>
        • 2BR: $550-$800 (avg $675)<br/>
        • 3BR: $700-$1,100 (avg $900)<br/>
        • 4BR: $900-$1,400 (avg $1,150)<br/>
        """
        story.append(Paragraph(market_analysis, styles['Normal']))
        story.append(PageBreak())
        
        # Investment Analysis
        story.append(Paragraph("INVESTMENT ANALYSIS", heading_style))
        
        # Create comparison table
        comparison_data = [
            ['Metric', 'Single Family', 'Duplex', 'Multi-Family'],
            ['Purchase Price', '$75,000', '$95,000', '$140,000'],
            ['Monthly Rent', '$900', '$1,350', '$2,450'],
            ['Cap Rate', '6.8%', '8.0%', '9.9%'],
            ['Cash-on-Cash Return', '4.7%', '8.0%', '13.9%'],
            ['DSCR', '1.13x', '1.34x', '1.65x'],
            ['Year 1 Cash Flow', '$984', '$2,135', '$5,435'],
            ['Investment Grade', '🔴 Weak', '🟢 Strong', '🟢 Strong']
        ]
        
        table = Table(comparison_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Add chart if available
        if os.path.exists('/workspace/investment_analysis_charts.png'):
            story.append(Paragraph("INVESTMENT COMPARISON CHARTS", heading_style))
            story.append(Image('/workspace/investment_analysis_charts.png', width=7*inch, height=5.6*inch))
            story.append(PageBreak())
        
        # Financial Projections
        story.append(Paragraph("10-YEAR FINANCIAL PROJECTIONS", heading_style))
        story.append(Paragraph("<b>Multi-Family Scenario (Recommended)</b>", styles['Heading3']))
        
        # Create 10-year projection table (simplified)
        projection_data = [
            ['Year', 'Gross Income', 'NOI', 'Cash Flow', 'Cumulative CF'],
            ['1', '$29,400', '$13,818', '$5,435', '$5,435'],
            ['2', '$30,135', '$14,164', '$5,781', '$11,216'],
            ['3', '$30,888', '$14,518', '$6,136', '$17,352'],
            ['4', '$31,660', '$14,881', '$6,501', '$23,853'],
            ['5', '$32,451', '$15,253', '$6,876', '$30,729'],
            ['10', '$37,148', '$17,459', '$7,877', '$67,890']
        ]
        
        proj_table = Table(projection_data, colWidths=[0.8*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        proj_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(proj_table)
        story.append(PageBreak())
        
        # Risk Analysis
        story.append(Paragraph("RISK ANALYSIS", heading_style))
        risk_analysis = """
        <b>Primary Risks:</b><br/>
        • Population Decline: Muncie has experienced a 7% population decrease, affecting long-term demand<br/>
        • Economic Dependency: Heavy reliance on Ball State University for rental demand<br/>
        • Property Age: Estimated construction dates from 1950-1960 may require significant capital improvements<br/>
        • Market Liquidity: Limited buyer pool may affect exit strategy<br/><br/>
        
        <b>Risk Mitigation Strategies:</b><br/>
        • Focus on university-adjacent properties for stable rental demand<br/>
        • Maintain strong cash reserves for unexpected repairs<br/>
        • Consider long-term leases to reduce vacancy risk<br/>
        • Implement professional property management<br/>
        • Plan for gradual market appreciation rather than rapid gains<br/>
        """
        story.append(Paragraph(risk_analysis, styles['Normal']))
        
        # Due Diligence Checklist
        story.append(Paragraph("DUE DILIGENCE CHECKLIST", heading_style))
        checklist = """
        <b>Critical Items to Verify:</b><br/>
        ☐ Actual property configuration and unit count<br/>
        ☐ Current rental rates and lease terms<br/>
        ☐ Property condition and repair estimates<br/>
        ☐ Zoning compliance for intended use<br/>
        ☐ Property tax assessments and history<br/>
        ☐ Utility configurations and costs<br/>
        ☐ Environmental concerns (lead, asbestos)<br/>
        ☐ Title search and survey<br/>
        ☐ Insurance requirements and costs<br/>
        ☐ Local rental regulations and licensing<br/>
        """
        story.append(Paragraph(checklist, styles['Normal']))
        story.append(PageBreak())
        
        # Recommendations
        story.append(Paragraph("RECOMMENDATIONS", heading_style))
        recommendations = """
        <b>Primary Recommendation:</b> Pursue the Multi-Family scenario if property configuration allows, 
        as it demonstrates superior investment metrics across all categories.<br/><br/>
        
        <b>Negotiation Strategy:</b><br/>
        • Target purchase price 10-15% below asking to improve returns<br/>
        • Request seller financing to reduce cash requirements<br/>
        • Negotiate repair credits for known deficiencies<br/><br/>
        
        <b>Financing Recommendations:</b><br/>
        • Secure pre-approval for investment property financing<br/>
        • Consider portfolio lenders for multi-unit properties<br/>
        • Maintain 6-month operating expense reserves<br/><br/>
        
        <b>Management Strategy:</b><br/>
        • Target Ball State students and faculty for stable tenancy<br/>
        • Implement professional property management<br/>
        • Focus on long-term value creation through strategic improvements<br/>
        """
        story.append(Paragraph(recommendations, styles['Normal']))
        
        # Disclaimer
        story.append(Spacer(1, 0.5*inch))
        disclaimer = """
        <b>DISCLAIMER:</b> This analysis is based on estimated market data and assumptions. 
        Actual property inspection, local market research, and professional consultation are required 
        before making any investment decisions. Past performance does not guarantee future results.
        """
        story.append(Paragraph(disclaimer, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filename
    
    def send_email_report(self, pdf_filename):
        """Send the report via email"""
        try:
            # Note: This is a placeholder for email functionality
            # In a real implementation, you would need SMTP credentials
            print(f"📧 Report generated: {pdf_filename}")
            print(f"📧 Ready to send to: {self.recipient_email}")
            print("📧 Email functionality requires SMTP configuration")
            return True
        except Exception as e:
            print(f"❌ Email sending failed: {str(e)}")
            return False

# Generate the report
if __name__ == "__main__":
    report_generator = ProfessionalUnderwritingReport()
    pdf_file = report_generator.create_pdf_report()
    report_generator.send_email_report(pdf_file)
    print(f"✅ Professional underwriting report generated: {pdf_file}")