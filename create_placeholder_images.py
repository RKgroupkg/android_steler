from PIL import Image, ImageDraw, ImageFont
import os

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Create icon (144x144 pixels)
icon = Image.new('RGB', (144, 144), color='white')
draw = ImageDraw.Draw(icon)
draw.rectangle([10, 10, 134, 134], outline='blue', width=5)
draw.text((72, 72), 'DS', fill='blue', anchor='mm', font=None)
icon.save('data/icon.png')

# Create presplash (480x800 pixels)
presplash = Image.new('RGB', (480, 800), color='white')
draw = ImageDraw.Draw(presplash)
draw.text((240, 400), 'Document Scanner', fill='blue', anchor='mm', font=None)
presplash.save('data/presplash.png')
