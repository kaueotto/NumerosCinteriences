from PIL import Image, ImageDraw

def paint_white(image_path, output_path, boxes):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    for box in boxes:
        draw.rectangle(box, fill="white")
    image.save(output_path)
    print(f"A imagem alterada foi salva em: {output_path}")