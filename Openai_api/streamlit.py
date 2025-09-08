import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# ---------------------------
# Load secrets from Streamlit
# ---------------------------
OPENAI_API_KEY = st.secrets["openai"]["api_key"]
PINECONE_API_KEY = st.secrets["pinecone"]["api_key"]
PINECONE_INDEX = st.secrets["pinecone"]["index_name"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(layout="wide")
st.title('OpenAI API Applications')

st.sidebar.title("Applications")
applications = ["Blog Generation", "Generate Image", "Movie Recommendation"]
application_choice = st.sidebar.radio("Choose an Application", applications)

# ---------------------------
# Blog Generation Function
# ---------------------------
def blog_genertion(topic, additional_pointers):
    prompt = f"""
    You are a copy writer with years of experience writing impactful blog that converge and help elevate brands.
    Your task is to write a blog on any topic system provides you with. Make sure to write in a format that works for Medium.
    Each blog should be separated into segments that have titles and subtitles. Each paragraph should be three sentences long.

    Topic: {topic}
    Additional pointers: {additional_pointers}
    """
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=700,
    )
    return response.choices[0].text.strip()

# ---------------------------
# Image Generation Function
# ---------------------------
def generate_image(prompt, number_of_images=1):
    response = client.images.generate(
        prompt=prompt,
        size="1024x1024",
        n=number_of_images,
    )
    return response

# ---------------------------
# Main App Logic
# ---------------------------
def main():
    if application_choice == "Blog Generation":
        st.header("Text Completion with GPT-3")
        st.write("Input some text and get a completion.")
        input_text = st.text_area("Enter text here:")
        additional_pointers = st.text_area("Enter additional pointers here:")
        
        if st.button("Complete Text"):
            with st.spinner('Generating...'):
                completion = blog_genertion(input_text, additional_pointers)
                st.text_area("Generated blog:", value=completion, height=200)

    elif application_choice == "Generate Image":
        st.header("Image Generation with DALL-E")
        st.write("Input some text and generate an image.")
        input_text = st.text_area("Enter text for image generation:")

        number_of_images = st.slider("Choose the number of images to generate", 1, 5, 1) 
        if st.button("Generate Image"):
            with st.spinner('Generating...'):
                outputs = generate_image(input_text, number_of_images)
                for output in outputs.data:
                    st.image(output.url)

    elif application_choice == "Movie Recommendation":
        st.header("Movie Recommendation with GPT")
        st.write("Input a movie description and get a recommendation.")

        input_text = st.text_area("Enter movie description:")

        if st.button("Get movies"):
            with st.spinner('Generating...'):
                # Generate embedding from OpenAI
                user_vector = client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=input_text
                ).data[0].embedding

                # Query Pinecone with keyword arguments
                response = index.query(
                    vector=user_vector,
                    top_k=10,
                    include_metadata=True
                )

                matches = response["matches"]  # Access matches list

                if matches:
                    for match in matches:
                        st.write(match["metadata"].get("title", "Untitled"))
                else:
                    st.write("No matching movies found.")

# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    main()
