import os
from PIL import Image, ImageSequence

def is_webp_animated(image):
    try:
        image.seek(1)
    except EOFError:
        return False
    else:
        return True

def remove_alpha_channel(frame):
    if frame.mode in ('RGBA', 'LA') or (frame.mode == 'P' and 'transparency' in frame.info):
        frame = frame.convert('RGB')
    return frame

def convert_webp_to_png_gif(source_directory):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith('.webp'):
                file_path = os.path.join(root, file)
                webp_image = Image.open(file_path)

                # Check if the WebP file is animated
                if is_webp_animated(webp_image):
                    # Save as GIF
                    gif_path = os.path.splitext(file_path)[0] + '.gif'
                    frames = [remove_alpha_channel(frame.copy()) for frame in ImageSequence.Iterator(webp_image)]
                    frames[0].save(gif_path, format='GIF', save_all=True, append_images=frames[1:], loop=0)
                    print(f'Converted {file_path} to {gif_path}')
                else:
                    # Save as PNG
                    png_path = os.path.splitext(file_path)[0] + '.png'
                    webp_image = remove_alpha_channel(webp_image)
                    webp_image.save(png_path, format='PNG')
                    print(f'Converted {file_path} to {png_path}')

                # Close the WebP image and delete the original file
                webp_image.close()
                os.remove(file_path)
                print(f'Deleting {file_path}')


if __name__ == '__main__':
    source_directory = os.path.dirname(os.path.abspath(__file__))  # Replace with the path to the directory containing the WebP files
    convert_webp_to_png_gif(source_directory)


