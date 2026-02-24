import shutil
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = BASE_DIR / 'products'
MEDIA_PRODUCTS_DIR = BASE_DIR / 'media' / 'products'

MEDIA_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

image_exts = {'.png', '.jpg', '.jpeg', '.gif', '.avif', '.webp'}

moved_files = []
for p in PRODUCTS_DIR.iterdir():
    if p.is_file() and p.suffix.lower() in image_exts:
        dest = MEDIA_PRODUCTS_DIR / p.name
        try:
            shutil.move(str(p), str(dest))
            moved_files.append(p.name)
            print(f"Moved {p.name} -> {dest}")
        except Exception as e:
            print(f"Failed to move {p.name}: {e}")

# Update DB entries
sys.path.insert(0, str(BASE_DIR))
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
import django
django.setup()
from products.models import Product

basename_to_rel = {name: f'products/{name}' for name in moved_files}

updated = []
for product in Product.objects.all():
    # current image name
    cur = product.image.name if product.image else ''
    if cur:
        # if current basename matches one we moved, update to new relative path
        b = Path(cur).name
        if b in basename_to_rel and cur != basename_to_rel[b]:
            product.image.name = basename_to_rel[b]
            product.save()
            updated.append((product.id, product.name, basename_to_rel[b]))
    else:
        # try to auto-assign if filename contains product name (case-insensitive)
        candidates = [name for name in moved_files if product.name.lower().replace(' ', '') in name.lower().replace(' ', '')]
        if len(candidates) == 1:
            product.image.name = basename_to_rel[candidates[0]]
            product.save()
            updated.append((product.id, product.name, basename_to_rel[candidates[0]]))

print('\nSummary:')
print(f'Moved files: {len(moved_files)}')
print(f'Products updated: {len(updated)}')
for u in updated:
    print(f'Product id={u[0]} name="{u[1]}" image="{u[2]}"')

if not moved_files:
    print('No image files found in products/ to move.')
else:
    print('Done.')
