import streamlit as st
import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from diffusers import StableDiffusionPipeline

# -------------------------
# Load Models Once (cached)
# -------------------------
@st.cache_resource
def load_image_to_text_model():
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    return processor, tokenizer, model

@st.cache_resource
def load_text_to_image_model():
    pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/sd-turbo",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        safety_checker=None   # disable safety checker for simplicity
    )
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    return pipe

# Load models
processor, tokenizer, img2txt_model = load_image_to_text_model()
txt2img_pipe = load_text_to_image_model()

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Lightweight Multi-Modal Chatbot", layout="wide")
st.title("🖼️ Lightweight Multi-Modal Chatbot")

tab1, tab2 = st.tabs(["📷 Image → Text", "📝 Text → Image"])

# -------------------------
# Tab 1: Image → Text
# -------------------------
with tab1:
    st.header("Describe an Image")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Generate Description"):
            with st.spinner("Analyzing image..."):
                pixel_values = processor(images=image, return_tensors="pt").pixel_values
                output_ids = img2txt_model.generate(pixel_values, max_length=16, num_beams=4)
                caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            st.success("Generated Caption:")
            st.write(caption)

# -------------------------
# Tab 2: Text → Image
# -------------------------
with tab2:
    st.header("Generate Image from Text")
    prompt = st.text_area("Enter your image prompt")

    if st.button("Generate Image") and prompt:
        with st.spinner("Generating image..."):
            image = txt2img_pipe(prompt).images[0]
        st.image(image, caption="Generated Image", use_container_width=True)
