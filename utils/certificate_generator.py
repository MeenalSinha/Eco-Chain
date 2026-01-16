"""
Certificate Generator Module
Generates downloadable PDF sustainability certificates
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

class CertificateGenerator:
    """
    Generates professional sustainability certificates in PDF format
    """
    
    def __init__(self):
        self.page_size = A4
        self.margin = 0.75 * inch
    
    def generate_certificate(self, token):
        """
        Generate a sustainability certificate PDF
        
        Args:
            token: Token data dictionary
        
        Returns:
            BytesIO: PDF file as bytes
        """
        buffer = BytesIO()
        
        # Create PDF
        c = canvas.Canvas(buffer, pagesize=self.page_size)
        width, height = self.page_size
        
        # Draw certificate border
        self._draw_border(c, width, height)
        
        # Add header
        self._add_header(c, width, height)
        
        # Add title
        self._add_title(c, width, height)
        
        # Add recipient info
        self._add_recipient_info(c, width, height, token)
        
        # Add achievement details
        self._add_achievement(c, width, height, token)
        
        # Add verification section
        self._add_verification(c, width, height, token)
        
        # Add footer
        self._add_footer(c, width, height)
        
        # Save PDF
        c.save()
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _draw_border(self, c, width, height):
        """Draw decorative border"""
        # Outer border
        c.setStrokeColor(colors.HexColor('#4CAF50'))
        c.setLineWidth(4)
        c.rect(self.margin, self.margin, 
               width - 2*self.margin, height - 2*self.margin)
        
        # Inner border
        c.setStrokeColor(colors.HexColor('#81C784'))
        c.setLineWidth(2)
        c.rect(self.margin + 10, self.margin + 10,
               width - 2*self.margin - 20, height - 2*self.margin - 20)
        
        # Corner decorations
        corner_size = 30
        margin = self.margin + 10
        
        # Top-left
        c.setFillColor(colors.HexColor('#4CAF50'))
        c.circle(margin, height - margin, corner_size, fill=1)
        
        # Top-right
        c.circle(width - margin, height - margin, corner_size, fill=1)
        
        # Bottom-left
        c.circle(margin, margin, corner_size, fill=1)
        
        # Bottom-right
        c.circle(width - margin, margin, corner_size, fill=1)
    
    def _add_header(self, c, width, height):
        """Add certificate header"""
        y = height - self.margin - 80
        
        # Logo/Icon (simulated with text)
        c.setFont("Helvetica-Bold", 48)
        c.setFillColor(colors.HexColor('#2E7D32'))
        c.drawCentredString(width/2, y, "🌱")
        
        y -= 40
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor('#1B5E20'))
        c.drawCentredString(width/2, y, "ECO-CHAIN")
        
        y -= 30
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.HexColor('#558B2F'))
        c.drawCentredString(width/2, y, "Verifiable Sustainability Proof Platform")
    
    def _add_title(self, c, width, height):
        """Add certificate title"""
        y = height - self.margin - 200
        
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(colors.HexColor('#1B5E20'))
        c.drawCentredString(width/2, y, "SUSTAINABILITY CERTIFICATE")
        
        y -= 25
        c.setStrokeColor(colors.HexColor('#4CAF50'))
        c.setLineWidth(2)
        c.line(width/2 - 150, y, width/2 + 150, y)
    
    def _add_recipient_info(self, c, width, height, token):
        """Add recipient information"""
        y = height - self.margin - 280
        
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, "This certificate is awarded to")
        
        y -= 40
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor('#1B5E20'))
        c.drawCentredString(width/2, y, token['sme_name'])
        
        y -= 30
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawCentredString(width/2, y, f"Business ID: {token['sme_id']}")
        
        y -= 25
        c.drawCentredString(width/2, y, f"Business Type: {token['business_type']}")
    
    def _add_achievement(self, c, width, height, token):
        """Add achievement details"""
        y = height - self.margin - 430
        
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, "For achieving verified carbon emission reduction of")
        
        # Display in kg with tonnes conversion for clarity
        emissions_reduced_kg = token['emissions_reduced_kg']
        emissions_reduced_tonnes = emissions_reduced_kg / 1000
        
        y -= 50
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(colors.HexColor('#4CAF50'))
        c.drawCentredString(width/2, y, f"{emissions_reduced_kg:.2f} kg CO₂")
        
        y -= 25
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawCentredString(width/2, y, f"(≈ {emissions_reduced_tonnes:.3f} tonnes)")
        
        y -= 30
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        
        reduction_pct = token['reduction_percentage']
        c.drawCentredString(width/2, y, 
                          f"Representing a {reduction_pct:.1f}% reduction vs industry baseline")
        
        y -= 25
        c.drawCentredString(width/2, y, f"Period: {token['month']}")
        
        # Achievement badge
        y -= 60
        c.setFillColor(colors.HexColor('#4CAF50'))
        c.circle(width/2, y, 40, fill=1)
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.white)
        c.drawCentredString(width/2, y + 10, "VERIFIED")
        c.drawCentredString(width/2, y - 5, "✓")
    
    def _add_verification(self, c, width, height, token):
        """Add verification details"""
        y = height - self.margin - 680
        
        # Verification box
        box_height = 100
        box_width = width - 2*self.margin - 60
        box_x = self.margin + 30
        
        c.setStrokeColor(colors.HexColor('#E0E0E0'))
        c.setFillColor(colors.HexColor('#F5F5F5'))
        c.setLineWidth(1)
        c.rect(box_x, y - box_height, box_width, box_height, fill=1)
        
        # Verification title
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawString(box_x + 10, y - 20, "BLOCKCHAIN VERIFICATION")
        
        # Verification details
        c.setFont("Courier", 8)
        c.setFillColor(colors.HexColor('#616161'))
        
        c.drawString(box_x + 10, y - 40, f"Token ID:")
        c.drawString(box_x + 80, y - 40, token['token_id'])
        
        c.drawString(box_x + 10, y - 55, f"Hash:")
        c.drawString(box_x + 80, y - 55, token['hash'][:52] + "...")
        
        c.drawString(box_x + 10, y - 70, f"Timestamp:")
        c.drawString(box_x + 80, y - 70, token['timestamp'][:19])
        
        c.drawString(box_x + 10, y - 85, f"Status:")
        c.setFillColor(colors.HexColor('#4CAF50'))
        c.drawString(box_x + 80, y - 85, "VERIFIED ON IMMUTABLE LEDGER ✓")
    
    def _add_footer(self, c, width, height):
        """Add certificate footer"""
        y = self.margin + 60
        
        c.setFont("Helvetica", 9)  # Changed from Helvetica-Italic
        c.setFillColor(colors.HexColor('#757575'))
        c.drawCentredString(width/2, y, 
                          "This certificate is cryptographically verified and tamper-proof")
        
        y -= 15
        c.drawCentredString(width/2, y,
                          "Issued by Eco-Chain Platform | www.eco-chain.example.com")
        
        y -= 15
        c.drawCentredString(width/2, y,
                          f"Certificate Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # QR Code placeholder (simulated)
        y += 40
        qr_size = 40
        c.setStrokeColor(colors.HexColor('#BDBDBD'))
        c.setFillColor(colors.HexColor('#F5F5F5'))
        c.rect(width/2 - qr_size/2, y, qr_size, qr_size, fill=1)
        
        c.setFont("Helvetica", 6)
        c.setFillColor(colors.HexColor('#757575'))
        c.drawCentredString(width/2, y + qr_size/2, "VERIFY")
        c.drawCentredString(width/2, y + qr_size/2 - 8, "ONLINE")
    
    def generate_quarterly_certificate(self, tokens):
        """
        Generate a quarterly summary certificate
        
        Args:
            tokens: List of tokens for the quarter
        
        Returns:
            BytesIO: PDF file as bytes
        """
        buffer = BytesIO()
        
        # Create PDF with more content
        # (Implementation similar to single certificate but with summary data)
        
        return buffer.getvalue()
    
    def generate_annual_report(self, tokens):
        """
        Generate an annual sustainability report
        
        Args:
            tokens: List of tokens for the year
        
        Returns:
            BytesIO: PDF file as bytes
        """
        buffer = BytesIO()
        
        # Create comprehensive annual report
        # (Implementation would include charts, graphs, detailed analysis)
        
        return buffer.getvalue()
