import pygame
import os

# بارگذاری فونت و اطلاعات
def load_font(fnt_file):
    if not os.path.exists(fnt_file):
        raise FileNotFoundError(f"Font file '{fnt_file}' not found.")

    with open(fnt_file, 'r') as file:
        lines = file.readlines()

    font_info = {}
    chars = {}

    for line in lines:
        if line.startswith("info") or line.startswith("page"):
            parts = line.split()
            for part in parts:
                if '=' in part:
                    key, value = part.split('=')
                    font_info[key] = value.strip().replace('"', '')

        elif line.startswith("char"):
            parts = line.split()
            char_info = {}
            for part in parts:
                if '=' in part:
                    key, value = part.split('=')
                    char_info[key] = float(value.strip()) if '.' in value else int(value.strip())

            if 'id' in char_info:
                chars[char_info['id']] = char_info

    return font_info, chars

# رندر کردن متن
def render_text(surface, text, font_chars, font_image, start_x, start_y):
    x = start_x
    for char in text:
        char_id = ord(char)
        if char_id in font_chars:
            char_info = font_chars[char_id]
            character_surface = font_image.subsurface((char_info['x'], char_info['y'], char_info['width'], char_info['height']))
            surface.blit(character_surface, (x + char_info['xoffset'], start_y - char_info['yoffset']))
            x += char_info['xadvance']
        else:
            # اگر کاراکتر موجود نیست، فاصله استاندارد را اضافه کنید
            x += font_chars.get(ord(' '), {'xadvance': 0})['xadvance']

# راه‌اندازی Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Font Rendering Example")

# بارگذاری فونت
try:
    font_info, font_chars = load_font('traitfont22.fnt')
except FileNotFoundError as e:
    print(e)
    pygame.quit()
    exit()

# بارگذاری تصویر فونت
font_image_path = font_info.get('page', 'traitfont22_0.png')
if not os.path.exists(font_image_path):
    print(f"Font image '{font_image_path}' not found.")
    pygame.quit()
    exit()

font_image = pygame.image.load(font_image_path)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # رنگ پس‌زمینه سیاه
    render_text(screen, "ABCDEFGabcd", font_chars, font_image, 50, 300)  # تنظیم موقعیت شروع

    pygame.display.flip()

pygame.quit()
