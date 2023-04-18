from PIL import Image, ImageDraw, ImageFont
import json
import zipfile
import io


def create_color_palette(values: list) -> bytes:
    hex_codes = values
    width, height = 300, 150

    palette_image = Image.new('RGB', (width, height), color='white')

    box_width = width // len(hex_codes)
    box_height = height - 20

    draw = ImageDraw.Draw(palette_image)
    font = ImageFont.truetype('arial.ttf', size=14)

    for i, color in enumerate(hex_codes):
        box = (i*box_width, 0, (i+1)*box_width, box_height)
        palette_image.paste(color, box)

        hex_code = color.upper().replace('#', '')
        text_width, text_height = draw.textsize(hex_code, font)
        text_x = i*box_width + (box_width - text_width) // 2
        text_y = box_height + 5
        draw.text((text_x, text_y), hex_code, fill='black', font=font)

    # Save the image to a byte buffer instead of a file
    buffer = io.BytesIO()
    palette_image.save(buffer, format='PNG')
    return buffer.getvalue()


if __name__ == '__main__':
    with open('color_palette.json') as arq_json:
        data = json.load(arq_json)
        with zipfile.ZipFile('color_palette.zip', 'w') as myzip:
            for k, v in data.items():
                image_bytes = create_color_palette(v)
                myzip.writestr(f'{k}.png', image_bytes)