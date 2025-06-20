
import os
from PIL import Image 
import random
import string

ACTUAL_CTF_FLAG = "CTF{D0uble_St3g0_Ch4llenge_Unl0cked!}" 
FLAG_MAGIC_STRING = b"##FLAG_START##" 

XOR_ENCRYPTION_KEY = "Sup3rS3cr3tX0RKey!" 
KEY_MAGIC_STRING = b"##KEY_START##" 


BASE_IMAGE_PATH = os.environ.get('__file_content_fetcher_asset_path__base_image.png', 'base_image.png')

ICONS_DIR = "icons"
TARGET_FLAG_ICON_NUMBER = 11 
TARGET_KEY_ICON_NUMBER = 51 
TOTAL_ICONS_TO_GENERATE = 100 

def create_dummy_png(path):
    """Creates a simple 10x10 red PNG image if no base image is found.
    This function will now only be called if the BASE_IMAGE_PATH (even
    the fetched one) somehow doesn't exist.
    """
    print(f"DEBUG: '{path}' (BASE_IMAGE_PATH) not found or inaccessible. Creating a dummy PNG for fallback...")
    img = Image.new('RGB', (10, 10), color = 'red')
    fallback_path = "fallback_dummy_base_image.png"
    try:
        img.save(fallback_path)
        print(f"DEBUG: Dummy PNG created at '{fallback_path}'.")
        return fallback_path 
    except Exception as e:
        print(f"FATAL: Could not create fallback dummy PNG at '{fallback_path}': {e}")
        return None 

def generate_random_bytes(length):
    """Generates a string of random printable ASCII characters of a given length."""
    chars = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(chars) for _ in range(length)).encode('utf-8')

def inject_files():
    """
    Generates icon files, injecting the flag into the target flag icon,
    the key into the target key icon, and random data into decoy icons.
    """
    print(f"DEBUG: Attempting to create directory: {ICONS_DIR}")
    try:
        os.makedirs(ICONS_DIR, exist_ok=True)
        print(f"DEBUG: Directory '{ICONS_DIR}' ensured to exist.")
    except Exception as e:
        print(f"FATAL: Could not create or access directory '{ICONS_DIR}': {e}")
        print("Please check write permissions for the current folder.")
        return 

    current_base_image_path = BASE_IMAGE_PATH
    if not os.path.exists(current_base_image_path):
        print(f"DEBUG: Primary base image path '{current_base_image_path}' does not exist.")
        current_base_image_path = create_dummy_png(current_base_image_path)
        if not current_base_image_path or not os.path.exists(current_base_image_path):
            print("Fatal Error: Cannot find or create a base image for injection. Exiting.")
            return

    try:
        with open(current_base_image_path, 'rb') as f:
            original_image_bytes = f.read()

        print(f"\n[*] Generating {TOTAL_ICONS_TO_GENERATE} icons...")

        for i in range(1, TOTAL_ICONS_TO_GENERATE + 1):
            output_filepath = os.path.join(ICONS_DIR, f"icon{i}.png")
            stego_image_bytes = original_image_bytes 
            data_to_append = b"" 

            if i == TARGET_FLAG_ICON_NUMBER:
                data_to_append = FLAG_MAGIC_STRING + ACTUAL_CTF_FLAG.encode('utf-8')
                print(f"    - Injected REAL flag into '{output_filepath}'")
            elif i == TARGET_KEY_ICON_NUMBER:
                data_to_append = KEY_MAGIC_STRING + XOR_ENCRYPTION_KEY.encode('utf-8')
                print(f"    - Injected XOR Key into '{output_filepath}'")
            else:
                dummy_magic = b"##RANDOM_JUNK##"
                random_junk = generate_random_bytes(random.randint(50, 150))
                data_to_append = dummy_magic + random_junk
                print(f"    - Injected random data into '{output_filepath}' (Decoy)")

            stego_image_bytes += data_to_append
            with open(output_filepath, 'wb') as f:
                f.write(stego_image_bytes)

        print(f"\n[*] Icon generation complete.")
        print(f"    - Real flag is in 'icons/icon{TARGET_FLAG_ICON_NUMBER}.png'")
        print(f"    - XOR key is in 'icons/icon{TARGET_KEY_ICON_NUMBER}.png'")
        print("    Remember to run 'app.py' first!")

    except Exception as e:
        print(f"An error occurred during icon generation: {e}")
        print(f"Ensure that '{current_base_image_path}' is a valid PNG file and is accessible.")
        print(f"Also check that the directory '{ICONS_DIR}' is writable.")


if __name__ == '__main__':
    inject_files()

