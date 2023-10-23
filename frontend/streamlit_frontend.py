import streamlit as st
from frontend_utils import base_models_list
from api_call import send_api_request
from frontend_utils.resize_image import resize_image
from frontend_utils.display import display_image_with_polygon, display_inpainted_image
from PIL import Image

def main():
    st.title("Inpaint Image")

    prompt = st.text_input("Enter a prompt for the image:", "Rabbit")

    selected_model = st.selectbox("Select a Model", base_models_list.models_list)
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    polygon_coordinates = get_coordinates_input()

    if uploaded_image is not None:
        uploaded_image_path, image = prepare_uploaded_image(uploaded_image)

        if st.button("Show Masked Image"):
            display_masked_image(image,polygon_coordinates, prompt, selected_model)

        if st.button("Submit"):
            if prompt:
                # Display a circular loading indicator
                with st.spinner("Inpainting in progress..."):
                    # Call the API function to perform inpainting
                    inpainted_image_pil = perform_inpainting(uploaded_image_path, polygon_coordinates, prompt, selected_model)
                display_inpainted_image(inpainted_image_pil)
            else:
                st.warning("Please enter a prompt before submitting.")

def get_coordinates_input():
    st.header("Enter 4 coordinates")
    x1 = st.number_input("X1", value=100)
    y1 = st.number_input("Y1", value=100)
    x2 = st.number_input("X2", value=100)
    y2 = st.number_input("Y2", value=600)
    x3 = st.number_input("X3", value=600)
    y3 = st.number_input("Y3", value=600)
    x4 = st.number_input("X4", value=600)
    y4 = st.number_input("Y4", value=100)
    polygon_coordinates = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    return polygon_coordinates

def prepare_uploaded_image(uploaded_image):
    image = Image.open(uploaded_image)
    image = resize_image(image, max_width=1024, max_height=1024)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    uploaded_image_path = "uploaded_image.png"
    image.save(uploaded_image_path, "PNG")
    return uploaded_image_path, image

def display_masked_image(image, coordinates, prompt, selected_model):

    display_image_with_polygon(image,coordinates)
    st.write("Coordinates:")
    st.write(f"Point 1: ({coordinates[0][0]}, {coordinates[0][1]}), Point 2: ({coordinates[1][0]}, {coordinates[1][1]}), Point 3: ({coordinates[2][0]}, {coordinates[2][1]}), Point 4: ({coordinates[3][0]}, {coordinates[3][1]})")
    st.write(f"Prompt: {prompt}")
    st.write(f"Model used: {selected_model}")

def perform_inpainting(image_path, polygon_coordinates, prompt, selected_model):
    inpainted_image_pil, prompt, _ = send_api_request(polygon_coordinates, prompt, image_path, base_model=selected_model)
    return inpainted_image_pil

if __name__ == '__main__':
    main()