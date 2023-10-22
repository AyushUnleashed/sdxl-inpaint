import streamlit as st
from PIL import Image, ImageDraw
from frontend_utils import base_models_list
from api_call import send_api_request
from frontend_utils.resize_image import resize_image

# Define the Streamlit app
st.title("Inpaint Image ")

# Add a text input for the prompt
prompt = st.text_input("Enter a prompt for the image:","Rabbit")

# Dropdown to select the base model
selected_model = st.selectbox("Select a Model", base_models_list.models_list)
base_model = selected_model

# Upload an image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

# Define input fields for the coordinates
st.header("Enter 4 coordinates")
x1 = st.number_input("X1", value=100)
y1 = st.number_input("Y1", value=100)
x2 = st.number_input("X2", value=100)
y2 = st.number_input("Y2", value=600)
x3 = st.number_input("X3", value=600)
y3 = st.number_input("Y3", value=600)
x4 = st.number_input("X4", value=600)
y4 = st.number_input("Y4", value=100)


# Display the uploaded image
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    width, height = image.size

    image = resize_image(image,max_width=1024,max_height=1024)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    uploaded_image_path = "assets/uploaded_image.png"
    image.save(uploaded_image_path, "PNG")

    polygon_coordinates = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

    if st.button("Show Masked Image"):

        # Draw a polygon on the image
        polygon_image = image.copy()
        draw = ImageDraw.Draw(polygon_image)
        draw.polygon(polygon_coordinates, fill=(0, 0, 0, 50))

        # Display the image with the polygon
        st.image(polygon_image, caption="Image with Polygon", use_column_width=True)

        st.write("Coordinates:")
        st.write(f"Point 1: ({x1}, {y1}), Point 2: ({x2}, {y2}), Point 3: ({x3}, {y3}), Point 4: ({x4}, {y4})")

        st.write(f"Prompt: {prompt}")
        st.write(f"Model used: {selected_model}")


    if st.button("Submit"):
        # Check if the prompt is not empty
        if prompt:
            # Display a circular loading indicator
            with st.spinner("Inpainting in progress..."):
                # Call the API function to perform inpainting
                inpainted_image_pil, prompt, coordinates =send_api_request(polygon_coordinates, prompt, uploaded_image_path, base_model=base_model)

            # Display the inpainted image on the frontend
            st.image(inpainted_image_pil, caption="Inpainted Image")
        else:
            st.warning("Please enter a prompt before submitting.")