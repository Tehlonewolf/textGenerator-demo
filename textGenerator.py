import openai
import streamlit as st

# Social Media Post Description Generator
# Uses OpenAI API to generate engaging, concise social media post text based on user-provided content.

# === Configuration ===
# Embed your API key directly here (or replace with environment variable retrieval)
openai.api_key = st.secrets["OPENAI_API_KEY"]  

# Default model choice; change to "gpt-4" if you have access and want higher-quality output
MODEL = "gpt-4"


def generate_description(content: str, model: str = MODEL) -> str:
    """
    Call the OpenAI Chat Completions API to generate a post description based on provided content.
    """
    system_prompt = (
        "You are an expert social media copywriter for a Property Management Company. "
        "Write an engaging, concise, and attention-grabbing description for a social media post. "
        "If the prompt given by the user is about administration (e.g. Rent Reminders) or anything else that's formal, keep the generated description formal and professional (no jokes, emojis, hashtags, etc.). "
        "If the prompt given by the user is about any festivals/holidays/events, feel free to make it more engaging. "
    ) 
    
    prompt = (
        f"The key points to include are: {content}."
    )
    # For openai>=1.0.0, use the chat completions endpoint
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def main():
    st.set_page_config(page_title="Post Description Bot", page_icon="✍️")
    st.title("✍️ Social Media Post Description Generator")

    # Main input for content
    content = st.text_area(
        "Enter the key points or text for your post:",
        height=200,
        help="Provide the main message, bullet points, or topic you want to convey."
    )

    # Generate button
    if st.button("Generate Description"):
        if not content.strip():
            st.error("Please enter some content or points for the post.")
        else:
            with st.spinner("Generating description..."):
                try:
                    description = generate_description(content)
                    st.subheader("Generated Description")
                    st.write(description)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()

# To run:
# 1. Install dependencies: pip install streamlit openai>=1.0.0
# 2. Replace "YOUR_OPENAI_API_KEY" with your actual key.
# 3. Run: streamlit run textGenerator.py
