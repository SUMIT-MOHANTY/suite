from docxtpl import DocxTemplate
from io import BytesIO
from datetime import datetime

def generate_release_letter(claim):
    """DOCX/Jinja2 stub for release letter generation"""
    doc = DocxTemplate("templates/release_template.docx")
    context = {
        'claim_number': claim.claim_number,
        'claimant_name': claim.claimant_name,
        'settlement_amount': claim.reserve_amount,
        'today_date': datetime.today().strftime('%B %d, %Y'),
        'policy_number': claim.policy_number
    }
    doc.render(context)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
