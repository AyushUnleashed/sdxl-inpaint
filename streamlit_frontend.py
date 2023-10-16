import streamlit as st
from PIL import Image, ImageDraw

# Define the Streamlit app
st.title("Inpaint Image ")

# Upload an image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

# Define input fields for the coordinates
st.header("Enter 4 coordinates")
x1 = st.number_input("X1", value=100)
y1 = st.number_input("Y1", value=100)
x2 = st.number_input("X2", value=100)
y2 = st.number_input("Y2", value=800)
x3 = st.number_input("X3", value=800)
y3 = st.number_input("Y3", value=800)
x4 = st.number_input("X4", value=800)
y4 = st.number_input("Y4", value=100)

# Add a text input for the prompt
prompt = st.text_input("Enter a prompt for the image:", "Draw a polygon with the given coordinates.")

# Display the uploaded image
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    uploaded_image_path = "assets/uploaded_image.png"
    image.save(uploaded_image_path, "PNG")
    # Draw a polygon on the image
    polygon_image = image.copy()
    draw = ImageDraw.Draw(polygon_image)
    polygon_coordinates = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    draw.polygon(polygon_coordinates, fill=(0, 0, 0, 100))  # RGBA color with 100 transparency

    # Display the image with the polygon
    st.image(polygon_image, caption="Image with Polygon", use_column_width=True)

    # Submit button to print coordinates
    if st.button("Show"):
        st.write("Coordinates:")
        st.write(f"Point 1: ({x1}, {y1})")
        st.write(f"Point 2: ({x2}, {y2})")
        st.write(f"Point 3: ({x3}, {y3})")
        st.write(f"Point 4: ({x4}, {y4})")

        st.write(f"Prompt: {prompt}")
        st.write(f"Uploaded Image Path: {uploaded_image_path}")

    if st.button("Submit"):
        # You can use 'uploaded_image_path' and 'prompt' in your send_api_request function
        from handle_input import send_api_request
        send_api_request(polygon_coordinates, prompt, uploaded_image_path)