# Define a function to resize an image while maintaining its aspect ratio
def resize_image(image, max_width=1024, max_height=1024):
    width, height = image.size
    if width > max_width or height > max_height:
        if width > height:
            new_width = max_width
            new_height = int(max_width / width * height)
        else:
            new_height = max_height
            new_width = int(max_height / height * width)
        return image.resize((new_width, new_height))
    return image