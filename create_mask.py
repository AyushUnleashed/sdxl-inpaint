from PIL import Image, ImageDraw

def create_mask(width, height, coordinates):
    try:
        mask = Image.new('L', (width, height), 0)  # 'L' mode for grayscale
        draw = ImageDraw.Draw(mask)
        draw.polygon(coordinates, fill=255)  # 255 is white
        mask_path = "assets/mask.png"
        mask.save(mask_path)
        return mask_path
    except OSError as e:
        print(f"Error creating the mask image: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    width = 512
    height = 512

    # Hardcoded coordinates for a square
    coordinates = [(100, 100), (300, 100), (300, 300), (100, 300)]

    mask_path = create_mask(width, height, coordinates)
    print(f"Mask image saved at {mask_path}")

if __name__ == "__main__":
    main()