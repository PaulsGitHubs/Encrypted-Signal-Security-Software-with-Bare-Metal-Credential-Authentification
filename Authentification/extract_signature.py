from PIL import Image

def binary_to_signature(binary):
    """Converts binary representation to signature using freq_table."""
    signature = []
    for i in range(0, len(binary), 8):
        bin_segment = binary[i:i+8]
        signature.append(list(freq_table.keys())[list(freq_table.values()).index(bin_segment)])
    return ''.join(signature)

def extract_signature_from_image(img, signature_length):
    """Extracts signature from image."""
    img_data = np.array(img)
    extracted_binary = ''
    for i in range(img_data.shape[0]):
        for j in range(img_data.shape[1]):
            pixel = img_data[i][j]
            extracted_binary += '0' if pixel[2] % 2 == 0 else '1'
            if len(extracted_binary) == signature_length * 8:
                return binary_to_signature(extracted_binary)

# Extract and verify the signature
extracted_img = Image.open("Auth_image_with_signature.png")
extracted_signature = extract_signature_from_image(extracted_img, 20)  # assuming length is 20
print("Extracted signature:", extracted_signature)
