from PIL import Image
import os
import argparse
# берет картинки или пачку и обрезает их под стикеры в тг
def resize_image(input_path, output_path):
    """Resize a single image to have a maximum dimension of 512px, maintaining the aspect ratio."""
    with Image.open(input_path) as img:
        img_ratio = img.width / img.height
        target_size = 512

        if img.width > img.height:
            new_width = target_size
            new_height = round(target_size / img_ratio)
        else:
            new_height = target_size
            new_width = round(target_size * img_ratio)

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_img.save(output_path, format='PNG')

def process_folder(input_folder, output_folder):
    """Process all images in a folder and resize them."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')
            resize_image(input_path, output_path)

def main():
    parser = argparse.ArgumentParser(description='Resize images to fit within a 512x512 square while maintaining the aspect ratio.')
    parser.add_argument('input', help='Input file or folder containing images (JPG, JPEG, PNG)')
    parser.add_argument('output', help='Output file or folder for resized PNG images')

    args = parser.parse_args()

    if os.path.isdir(args.input):
        process_folder(args.input, args.output)
    elif os.path.isfile(args.input) and args.input.lower().endswith(('.jpg', '.jpeg', '.png')):
        output_path = args.output if args.output.lower().endswith('.png') else args.output + '.png'
        resize_image(args.input, output_path)
    else:
        print("Error: Input should be an image file or a folder containing images.")

if __name__ == '__main__':
    main()