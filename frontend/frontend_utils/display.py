import streamlit as st
from PIL import Image, ImageDraw

def display_image_with_polygon(image, polygon_coordinates):
    # Create a copy of the image to draw the polygon
    polygon_image = image.copy()
    draw = ImageDraw.Draw(polygon_image)
    draw.polygon(polygon_coordinates, fill=(0, 0, 0, 50))

    # Display the image with the polygon
    st.image(polygon_image, caption="Image with Polygon", use_column_width=True)

def display_inpainted_image(image):
    st.image(image, caption="Inpainted Image")