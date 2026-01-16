"""
Professional Certificate Generator for Eco-Chain
Creates clean, modern sustainability certificates
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


class CertificateGenerator:
    """Generate professional sustainability certificates"""
    
    def __init__(self):
        """Initialize certificate generator"""
        pass
    
    def generate_certificate(self, token):
        """
        Generate a professional sustainability certificate
        
        Args:
            token: Dictionary containing token information
        
        Returns:
            bytes: PDF file content
        """
        buffer = BytesIO()
        
        # Create PDF with better page setup
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Professional color scheme
        primary_green = colors.HexColor('#2E7D32')
        light_green = colors.HexColor('#4CAF50')
        dark_green = colors.HexColor('#1B5E20')
        gold = colors.HexColor('#FFB300')
        gray = colors.HexColor('#616161')
        light_gray = colors.HexColor('#F5F5F5')
        
        # Draw border
        self._draw_border(c, width, height, light_green, primary_green)
        
        # Add header (without logo)
        self._add_header(c, width, height, dark_green, light_green)
        
        # Add recipient info
        self._add_recipient(c, width, height, token, primary_green)
        
        # Add achievement (the star of the show)
        self._add_achievement(c, width, height, token, light_green, gold)
        
        # Add verification section (fixed layout)
        self._add_verification(c, width, height, token, gray, light_gray)
        
        # Add footer
        self._add_footer(c, width, height, gray)
        
        # Save PDF
        c.save()
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _draw_border(self, c, width, height, light_green, primary_green):
        """Draw clean professional border"""
        margin = 30
        
        # Outer border - light green
        c.setStrokeColor(light_green)
        c.setLineWidth(3)
        c.rect(margin, margin, width - 2*margin, height - 2*margin, fill=0)
        
        # Inner border - primary green
        c.setStrokeColor(primary_green)
        c.setLineWidth(1.5)
        c.rect(margin + 10, margin + 10, width - 2*margin - 20, height - 2*margin - 20, fill=0)
    
    def _add_header(self, c, width, height, dark_green, light_green):
        """Add clean header section without logo"""
        y = height - 70
        
        # Company name
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(dark_green)
        c.drawString(60, y, "ECO-CHAIN")
        
        # Tagline (smaller, left-aligned)
        y -= 18
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawString(60, y, "Verifiable Sustainability...")
        
        # Title
        y -= 50
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(light_green)
        c.drawCentredString(width/2, y, "SUSTAINABILITY")
        
        y -= 28
        c.drawCentredString(width/2, y, "CERTIFICATE")
        
        # Decorative line
        y -= 15
        c.setStrokeColor(colors.HexColor('#CCCCCC'))
        c.setLineWidth(1)
        c.line(60, y, width - 60, y)
    
    def _add_recipient(self, c, width, height, token, primary_green):
        """Add recipient information clearly"""
        y = height - 230
        
        # "Awarded to" text
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        c.drawString(60, y, "This certificate is proudly...")
        
        # Recipient name - centered, prominent
        y -= 40
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, f"[{token['sme_name']}]")
        
        # Business details
        y -= 30
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawCentredString(width/2, y, f"ID: {token['sme_id']} • {token['business_type']}")
    
    def _add_achievement(self, c, width, height, token, light_green, gold):
        """Highlight the achievement"""
        y = height - 320
        
        # Achievement intro
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        c.drawString(60, y, "For achieving verified carbon...")
        
        # THE BIG NUMBER - emissions reduced
        y -= 40
        emissions_kg = token['emissions_reduced_kg']
        emissions_tonnes = emissions_kg / 1000
        
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(light_green)
        c.drawCentredString(width/2, y, f"{emissions_tonnes:.3f}")
        
        # Units
        y -= 20
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, y, "tonnes CO₂")
        
        # Equivalent in kg (smaller)
        y -= 15
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor('#616161'))
        c.drawCentredString(width/2, y, f"({emissions_kg:,.0f} kg)")
        
        # Reduction percentage and period
        y -= 30
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        reduction_pct = token['reduction_percentage']
        c.drawString(60, y, f"Representing a {reduction_pct:.1f}% reduction")
        
        y -= 18
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor('#757575'))
        c.drawString(60, y, f"Period: {token['month']}")
        
        # VERIFIED badge
        y -= 35
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, "[VERIFIED ✓]")
    
    def _add_verification(self, c, width, height, token, gray, light_gray):
        """Add verification details in table format"""
        y = height - 545
        
        # Section title
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)
        c.drawString(60, y, "CRYPTOGRAPHIC VERIFICATION")
        
        # Draw table box
        y -= 10
        box_height = 85
        box_width = width - 120
        box_x = 60
        
        c.setStrokeColor(colors.HexColor('#000000'))
        c.setLineWidth(1)
        c.rect(box_x, y - box_height, box_width, box_height, fill=0, stroke=1)
        
        # Vertical divider in middle
        c.line(box_x + box_width/2, y - box_height, box_x + box_width/2, y)
        
        # Horizontal divider in middle
        c.line(box_x, y - box_height/2, box_x + box_width, y - box_height/2)
        
        # Left top - Token ID
        y_text = y - 20
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        c.drawString(box_x + 10, y_text, "Token ID:")
        y_text -= 15
        c.setFont("Courier", 7)
        token_id = token['token_id']
        if len(token_id) > 18:
            c.drawString(box_x + 10, y_text, token_id[:18])
            y_text -= 10
            c.drawString(box_x + 10, y_text, token_id[18:])
        else:
            c.drawString(box_x + 10, y_text, token_id)
        
        # Right top - Hash
        y_text = y - 20
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        c.drawString(box_x + box_width/2 + 10, y_text, "Hash:")
        y_text -= 15
        c.setFont("Courier", 7)
        hash_str = token['hash']
        c.drawString(box_x + box_width/2 + 10, y_text, hash_str[:18])
        y_text -= 10
        c.drawString(box_x + box_width/2 + 10, y_text, hash_str[18:36] + "...")
        
        # Left bottom - Timestamp
        y_text = y - box_height/2 - 20
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        c.drawString(box_x + 10, y_text, "Timestamp:")
        y_text -= 15
        c.setFont("Courier", 8)
        c.drawString(box_x + 10, y_text, token['timestamp'][:10])
        
        # Right bottom - Status
        y_text = y - box_height/2 - 20
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        c.drawString(box_x + box_width/2 + 10, y_text, "Status:")
        y_text -= 15
        c.setFont("Helvetica", 8)
        c.drawString(box_x + box_width/2 + 10, y_text, "VERIFIED ✓")
    
    def _add_footer(self, c, width, height, gray):
        """Add clean footer"""
        y = height - 660
        
        # Certificate authenticity statement
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawString(60, y, "Cryptographically verified...")
        
        y -= 15
        c.drawString(60, y, "Issued by Eco-Chain Platform")
        
        y -= 15
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor('#9E9E9E'))
        c.drawString(60, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Verify online text
        y -= 25
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, "[VERIFY ONLINE]")
