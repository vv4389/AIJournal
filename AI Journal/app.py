import time

import streamlit as st
from PIL import Image

from ProjectRun import ProjectRun
from UserClass import User


def typewriter(text: str, speed: int, st):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)


def main():
    st.title("Welcome to AI-Journal")
    time.sleep(2)
    st.subheader("Let's upload an image for the journal entry")
    time.sleep(2)
    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg", "JPG"])

    if uploaded_file is not None:
        with st.spinner("Loading!!!!"):
            # Display the uploaded image
            image = Image.open(uploaded_file)
            # You can perform further processing on the image here if needed
            result = ProjectRun(User(img=image), image, st).SystemRun()

        if result is not None and len(result) > 1:
            st.image(image, use_column_width=True)
            typewriter(result, speed=5, st=st)


if __name__ == "__main__":
    import SetupEnv

    SetupEnv.setup()
    main()
