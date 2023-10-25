from PIL import Image, ImageOps
import numpy as np

# Predefined list of special characters for unique binary value mapping.
special_chars = ['☉','✠', '✡', '✢', '✣', '✤', ...]  # abbreviated for brevity

# Binary mapping for each character.
freq_table = {char: format(idx, '08b') for idx, char in enumerate(special_chars)}

def signature_to_binary(signature):
    """Converts signature to binary representation using freq_table."""
    return ''.join(freq_table[char] for char in signature)

def generate_device_signature():
    """Generates a random signature."""
    return ''.join(np.random.choice(list(special_chars), 20))

def embed_signature_in_image(img, signature):
    """Embeds binary representation of signature into the image."""
    binary_signature = signature_to_binary(signature)
    img_data = np.array(img)
    idx = 0
    for i in range(img_data.shape[0]):
        for j in range(img_data.shape[1]):
            if idx >= len(binary_signature):
                return Image.fromarray(img_data)
            pixel = list(img_data[i][j])
            if binary_signature[idx] == '0' and pixel[2] % 2 == 1:
                pixel[2] -= 1
            elif binary_signature[idx] == '1' and pixel[2] % 2 == 0:
                pixel[2] += 1
            img_data[i][j] = tuple(pixel)
            idx += 1

def generate_random_image(width, height):
    """Generates a random image."""
    array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(array)
    return img

def generate_image_with_signature():
    """Generates an image with embedded signature."""
    signature = generate_device_signature()
    img = generate_random_image(500, 500)
    img_with_signature = embed_signature_in_image(img, signature)
    img_with_signature.save("Auth_image_with_signature.png", format="PNG")
    return signature

# Call function to generate the image with embedded signature
stored_signature = generate_image_with_signature()
print("Generated and stored signature:", stored_signature)
