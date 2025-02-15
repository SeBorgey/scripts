from PIL import Image
import os
import argparse
import io
# получает изображение jpg и сжимает его в png  до нужного размера
def resize_to_target_size(input_image, target_size_bytes):
    """Resize image to fit within the target size in bytes by adjusting its dimensions."""
    width, height = input_image.size
    scale_factor = 0.9

    while True:
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        resized_image = input_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        resized_image.save(buffer, format='PNG', optimize=True)
        size = buffer.tell()

        if size <= target_size_bytes or (new_width < 10 or new_height < 10):
            return resized_image

        width, height = new_width, new_height

def compress_and_convert_image(input_path, output_path, target_size_kb=128):
    """Convert a JPG image to PNG and compress it to fit within a specified size in kilobytes."""
    target_size_bytes = target_size_kb * 1024

    with Image.open(input_path) as img:
        img = img.convert('RGBA')

        resized_image = resize_to_target_size(img, target_size_bytes)

        resized_image.save(output_path, format='PNG', optimize=True)

def main():
    parser = argparse.ArgumentParser(description='Convert JPG to PNG and compress to less than 256kB.')
    parser.add_argument('input', help='Input JPG file')
    parser.add_argument('output', help='Output PNG file')

    args = parser.parse_args()

    if os.path.isfile(args.input) and args.input.lower().endswith('.jpg'):
        compress_and_convert_image(args.input, args.output)
    else:
        print("Error: Input should be a JPG file.")

if __name__ == '__main__':
    main()