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
        
        # Add header
        self._add_header(c, width, height, dark_green, light_green)
        
        # Add recipient info
        self._add_recipient(c, width, height, token, primary_green)
        
        # Add achievement (the star of the show)
        self._add_achievement(c, width, height, token, light_green, gold)
        
        # Add verification section
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
        """Add clean header section"""
        y = height - 80
        
        # Logo area (simple green square as logo)
        logo_size = 40
        c.setFillColor(dark_green)
        c.rect(width/2 - logo_size/2, y - logo_size/2, logo_size, logo_size, fill=1)
        
        # Company name
        y -= 60
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(dark_green)
        c.drawCentredString(width/2, y, "ECO-CHAIN")
        
        # Tagline
        y -= 25
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawCentredString(width/2, y, "Verifiable Sustainability Proof Platform")
        
        # Title
        y -= 50
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(light_green)
        c.drawCentredString(width/2, y, "SUSTAINABILITY")
        
        y -= 40
        c.drawCentredString(width/2, y, "CERTIFICATE")
        
        # Decorative line
        y -= 20
        c.setStrokeColor(light_green)
        c.setLineWidth(2)
        c.line(width/2 - 180, y, width/2 + 180, y)
    
    def _add_recipient(self, c, width, height, token, primary_green):
        """Add recipient information clearly"""
        y = height - 340
        
        # "Awarded to" text
        c.setFont("Helvetica", 13)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, "This certificate is proudly awarded to")
        
        # Recipient name - LARGE and prominent
        y -= 45
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(primary_green)
        c.drawCentredString(width/2, y, token['sme_name'])
        
        # Business details - clean and organized
        y -= 35
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor('#424242'))
        c.drawCentredString(width/2, y, f"Business ID: {token['sme_id']}  •  {token['business_type']}")
    
    def _add_achievement(self, c, width, height, token, light_green, gold):
        """Highlight the achievement - this is the most important part"""
        y = height - 440
        
        # Achievement intro
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, "For achieving verified carbon emission reduction of")
        
        # THE BIG NUMBER - emissions reduced
        y -= 55
        emissions_kg = token['emissions_reduced_kg']
        emissions_tonnes = emissions_kg / 1000
        
        c.setFont("Helvetica-Bold", 48)
        c.setFillColor(light_green)
        c.drawCentredString(width/2, y, f"{emissions_tonnes:.3f}")
        
        # Units
        y -= 25
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, y, "tonnes CO₂")
        
        # Equivalent in kg (smaller)
        y -= 20
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor('#616161'))
        c.drawCentredString(width/2, y, f"({emissions_kg:,.0f} kg)")
        
        # Reduction percentage
        y -= 35
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        reduction_pct = token['reduction_percentage']
        c.drawCentredString(width/2, y, f"Representing a {reduction_pct:.1f}% reduction vs industry baseline")
        
        # Period
        y -= 25
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor('#757575'))
        c.drawCentredString(width/2, y, f"Period: {token['month']}")
        
        # VERIFIED badge
        y -= 55
        badge_size = 70
        c.setFillColor(light_green)
        c.circle(width/2, y, badge_size/2, fill=1)
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.white)
        c.drawCentredString(width/2, y + 8, "VERIFIED")
        c.drawCentredString(width/2, y - 8, "✓")
    
    def _add_verification(self, c, width, height, token, gray, light_gray):
        """Add verification details in clean box"""
        y = 220
        
        # Background box
        box_height = 110
        box_width = width - 100
        box_x = 50
        
        c.setStrokeColor(colors.HexColor('#E0E0E0'))
        c.setFillColor(light_gray)
        c.setLineWidth(1)
        c.rect(box_x, y - box_height, box_width, box_height, fill=1)
        
        # Section title
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(gray)
        c.drawString(box_x + 15, y - 20, "CRYPTOGRAPHIC VERIFICATION")
        
        # Verification details in two columns
        c.setFont("Courier", 8)
        c.setFillColor(colors.HexColor('#424242'))
        
        left_x = box_x + 15
        right_x = box_x + box_width/2 + 15
        
        # Left column
        y_pos = y - 45
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left_x, y_pos, "Token ID:")
        c.setFont("Courier", 7)
        c.drawString(left_x, y_pos - 12, token['token_id'])
        
        y_pos -= 30
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left_x, y_pos, "Timestamp:")
        c.setFont("Courier", 7)
        c.drawString(left_x, y_pos - 12, token['timestamp'][:19])
        
        # Right column
        y_pos = y - 45
        c.setFont("Helvetica-Bold", 8)
        c.drawString(right_x, y_pos, "Verification Hash:")
        c.setFont("Courier", 7)
        # Split hash into two lines for readability
        hash_str = token['hash']
        c.drawString(right_x, y_pos - 12, hash_str[:40])
        c.drawString(right_x, y_pos - 22, hash_str[40:] + "...")
        
        y_pos -= 30
        c.setFont("Helvetica-Bold", 8)
        c.drawString(right_x, y_pos, "Status:")
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor('#4CAF50'))
        c.drawString(right_x, y_pos - 12, "VERIFIED ON IMMUTABLE LEDGER ✓")
    
    def _add_footer(self, c, width, height, gray):
        """Add clean footer"""
        y = 80
        
        # Certificate authenticity statement
        c.setFont("Helvetica", 9)
        c.setFillColor(gray)
        c.drawCentredString(width/2, y, 
                          "This certificate is cryptographically verified and tamper-proof")
        
        y -= 18
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, y,
                          "Issued by Eco-Chain Platform | www.eco-chain.example.com")
        
        # Generation timestamp
        y -= 18
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor('#9E9E9E'))
        c.drawCentredString(width/2, y,
                          f"Certificate Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # QR Code placeholder (centered)
        y += 50
        qr_size = 35
        c.setStrokeColor(colors.HexColor('#BDBDBD'))
        c.setFillColor(colors.HexColor('#FAFAFA'))
        c.rect(width/2 - qr_size/2, y, qr_size, qr_size, fill=1)
        
        c.setFont("Helvetica", 6)
        c.setFillColor(gray)
        c.drawCentredString(width/2, y + qr_size/2 + 2, "VERIFY")
        c.drawCentredString(width/2, y + qr_size/2 - 6, "ONLINE")
