from PIL import Image

def create_test_image(filename, width, height):
    # Create a new image with a white background
    img = Image.new('RGB', (width, height), color='white')

    # Get a drawing context
    d = img.getdata()

    # Draw a simple pattern (a cross)
    for i in range(width):
        img.putpixel((i, height // 2), (0, 0, 0))  # Horizontal line
    for i in range(height):
        img.putpixel((width // 2, i), (0, 0, 0))  # Vertical line

    # Save the image
    img.save(filename)

    print(f"Test image created: {filename}")

if __name__ == "__main__":
    create_test_image('test_image.png', 50, 50)
