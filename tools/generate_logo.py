import math
from PIL import Image, ImageDraw, ImageFont

def draw_glowing_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def generate_logo():
    # 1. 512x512 Logo Icon
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base background: Deep Obsidian / Cosmic Navy Squircle
    margin = 24
    radius = 96
    bg_box = [margin, margin, size - margin, size - margin]
    
    # Outer gold & cyan subtle glow rings
    for i in range(12, 0, -1):
        alpha = int(18 * (1.0 - i / 12.0))
        draw.rounded_rectangle([margin - i, margin - i, size - margin + i, size - margin + i],
                               radius=radius + i, outline=(255, 215, 0, alpha), width=2)

    # Card background gradient simulated
    for y in range(margin, size - margin):
        ratio = (y - margin) / float(size - 2 * margin)
        # Gradient from #1A1F2C to #0D111A
        r = int(26 * (1 - ratio) + 13 * ratio)
        g = int(31 * (1 - ratio) + 17 * ratio)
        b = int(44 * (1 - ratio) + 26 * ratio)
        draw.line([(margin, y), (size - margin, y)], fill=(r, g, b, 255))

    # Mask to rounded rect
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(bg_box, radius=radius, fill=255)
    
    # Combine with mask
    base_card = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base_card.paste(img, (0, 0), mask=mask)
    draw = ImageDraw.Draw(base_card)

    # Gold rim border
    draw.rounded_rectangle(bg_box, radius=radius, outline=(255, 215, 0, 220), width=4)

    # Internal elements: USB Drive + Cinema Play Ring
    cx, cy = size // 2, size // 2 - 28

    # Glowing Circle behind icon
    for r in range(120, 70, -4):
        alpha = int(35 * (1.0 - (r - 70) / 50.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 180, 0, alpha))

    # USB Drive Body
    usb_w, usb_h = 76, 120
    usb_x0, usb_y0 = cx - usb_w // 2, cy - usb_h // 2
    # USB cap/connector
    conn_w, conn_h = 44, 38
    draw.rounded_rectangle([cx - conn_w // 2, usb_y0 - conn_h + 8, cx + conn_w // 2, usb_y0 + 8],
                           radius=6, fill=(210, 220, 235, 255), outline=(255, 255, 255, 240), width=2)
    # Connector pins
    draw.rectangle([cx - 14, usb_y0 - conn_h + 14, cx - 6, usb_y0 - 2], fill=(60, 70, 85, 255))
    draw.rectangle([cx + 6, usb_y0 - conn_h + 14, cx + 14, usb_y0 - 2], fill=(60, 70, 85, 255))

    # Main USB metallic body
    draw.rounded_rectangle([usb_x0, usb_y0, usb_x0 + usb_w, usb_y0 + usb_h],
                           radius=18, fill=(35, 42, 58, 255), outline=(255, 215, 0, 240), width=3)

    # Cinema Play Triangle in center of USB
    tri_cx, tri_cy = cx + 3, cy + 10
    tri_size = 22
    points = [
        (tri_cx - tri_size * 0.7, tri_cy - tri_size),
        (tri_cx + tri_size * 1.1, tri_cy),
        (tri_cx - tri_size * 0.7, tri_cy + tri_size)
    ]
    draw.polygon(points, fill=(255, 215, 0, 255))

    # Glow Status LED on USB
    draw.ellipse([cx - 5, usb_y0 + usb_h - 22, cx + 5, usb_y0 + usb_h - 12], fill=(0, 240, 255, 255))

    # Text Branding (NLRC & PENDRIVE VIEWER)
    try:
        font_nlrc = ImageFont.truetype("arialbd.ttf", 46)
        font_sub = ImageFont.truetype("arialbd.ttf", 22)
        font_tag = ImageFont.truetype("arial.ttf", 15)
    except:
        font_nlrc = font_sub = font_tag = ImageFont.load_default()

    # NLRC
    nlrc_text = "NLRC"
    bbox_nlrc = draw.textbbox((0, 0), nlrc_text, font=font_nlrc)
    tw_nlrc = bbox_nlrc[2] - bbox_nlrc[0]
    draw.text((cx - tw_nlrc // 2, size - 142), nlrc_text, fill=(255, 255, 255, 255), font=font_nlrc)

    # PENDRIVE VIEWER
    pv_text = "PENDRIVE VIEWER"
    bbox_pv = draw.textbbox((0, 0), pv_text, font=font_sub)
    tw_pv = bbox_pv[2] - bbox_pv[0]
    draw.text((cx - tw_pv // 2, size - 92), pv_text, fill=(255, 215, 0, 255), font=font_sub)

    # FAMILY ARCHIVE
    fa_text = "PERSONAL MEDIA ARCHIVE"
    bbox_fa = draw.textbbox((0, 0), fa_text, font=font_tag)
    tw_fa = bbox_fa[2] - bbox_fa[0]
    draw.text((cx - tw_fa // 2, size - 62), fa_text, fill=(180, 195, 215, 255), font=font_tag)

    # Save 512x512 logo
    out_logo = r"c:\Users\ck528\Downloads\experiments\tv-vibehack\launcher\app\src\main\res\drawable-nodpi\logo_pendrive_viewer.png"
    base_card.save(out_logo, "PNG")
    print(f"Saved logo: {out_logo}")

    # 2. 16:9 Banner (320x180) for TV Card
    banner_w, banner_h = 320, 180
    banner = Image.new("RGBA", (banner_w, banner_h), (12, 16, 24, 255))
    bdraw = ImageDraw.Draw(banner)

    # Draw gradient background
    for y in range(banner_h):
        ratio = y / float(banner_h)
        r = int(22 * (1 - ratio) + 8 * ratio)
        g = int(26 * (1 - ratio) + 12 * ratio)
        b = int(38 * (1 - ratio) + 18 * ratio)
        bdraw.line([(0, y), (banner_w, y)], fill=(r, g, b, 255))

    # Paste scaled icon on left
    icon_small = base_card.resize((130, 130), Image.LANCZOS)
    banner.paste(icon_small, (18, 25), mask=icon_small)

    # Text on right
    try:
        f_b_title = ImageFont.truetype("arialbd.ttf", 20)
        f_b_sub = ImageFont.truetype("arialbd.ttf", 13)
        f_b_desc = ImageFont.truetype("arial.ttf", 11)
    except:
        f_b_title = f_b_sub = f_b_desc = ImageFont.load_default()

    tx = 158
    bdraw.text((tx, 42), "NLRC", fill=(255, 215, 0, 255), font=f_b_sub)
    bdraw.text((tx, 60), "PenDrive Viewer", fill=(255, 255, 255, 255), font=f_b_title)
    bdraw.text((tx, 90), "Media Archive", fill=(255, 215, 0, 230), font=f_b_sub)
    bdraw.text((tx, 110), "Part 1 · Part 2 · Part 3", fill=(160, 175, 195, 255), font=f_b_desc)

    out_banner = r"c:\Users\ck528\Downloads\experiments\tv-vibehack\launcher\app\src\main\res\drawable-nodpi\banner_pendrive_viewer.png"
    banner.save(out_banner, "PNG")
    print(f"Saved banner: {out_banner}")

if __name__ == "__main__":
    generate_logo()
