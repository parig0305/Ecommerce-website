from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from PIL import Image as PILImage, ImageDraw
from pathlib import Path

# Create output directory
BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / 'tests_output'
OUT_DIR.mkdir(exist_ok=True)

# Create a simple PNG image using PIL
img_path = OUT_DIR / 'test_image.png'
img = PILImage.new('RGB', (300, 150), color=(73, 109, 137))
d = ImageDraw.Draw(img)
d.text((10, 60), "Test Image", fill=(255, 255, 255))
img.save(img_path)

# Build PDF
pdf_path = OUT_DIR / 'invoice_test.pdf'
doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
styles = getSampleStyleSheet()
content = []
content.append(Paragraph('Invoice Test - Image Embed', styles['Title']))
content.append(Spacer(1, 12))
content.append(Paragraph('This PDF includes an embedded PNG image generated at runtime.', styles['Normal']))
content.append(Spacer(1, 12))

# Embed the image
content.append(Image(str(img_path), width=300, height=150))

# Save PDF
doc.build(content)
print('Generated PDF at:', pdf_path)
