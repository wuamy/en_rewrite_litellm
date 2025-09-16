import streamlit as st
import os
from litellm import completion
from dotenv import load_dotenv

# --- Step 1: Securely Load API Keys ---
load_dotenv()

# --- Step 2: Configure Environment Variables for LiteLLM ---
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

# --- Step 3: Streamlit UI Components ---
st.title("AI Text Rewriter")
st.markdown("Enter text, select a tone, and choose an AI provider to rewrite your content.")

api_provider = st.selectbox(
    "Select AI Provider:",
    ("Gemini", "Groq", "OpenRouter"),
    index=0
)

# Dictionary mapping UI selections to the correct LiteLLM model string.
models = {
    "Gemini": "gemini/gemini-1.5-flash-latest",
    "Groq": "groq/llama-3.1-8b-instant",
    "OpenRouter": "openrouter/openai/gpt-4o-mini",
}

tone = st.selectbox(
    "Select Tone:",
    ("Standard", "Professional", "Casual", "Formal", "Friendly", "Concise"),
    index=0
)

# Add a slider to control the temperature
temperature = st.slider(
    "Set Creativity (Temperature):",
    min_value=0.0,
    max_value=2.0,
    value=0.7, # A good default for a balance of creativity and predictability
    step=0.1,
    help="Lower values make the output more focused and deterministic. Higher values make it more random and creative."
)

user_input = st.text_area(
    "Enter the text you want to rewrite:",
    height=200,
    placeholder="Type or paste your text here..."
)

output_container = st.empty()

# --- Step 4: The Core Logic ---
if st.button("Rewrite"):
    if not user_input:
        st.warning("Please enter some text to rewrite.")
    else:
        with st.spinner("Rewriting..."):
            try:
                system_prompt = f"""
You are a highly efficient and concise text rewriter.
Your sole task is to rewrite the user's input.
You must not provide any additional explanations, introductions, or conversational text.
Your output must be the rewritten text and nothing else.
Rewrite the following text with improved grammar and in a {tone} tone.
"""
                selected_model = models.get(api_provider)
                
                # Pass the temperature parameter here
                response = completion(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=temperature # Pass the value from the slider
                )
                
                rewritten_text = response.choices[0].message.content
                
                output_container.text_area("Rewritten Text:", value=rewritten_text, height=200)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Please check your API keys and the model's availability.")