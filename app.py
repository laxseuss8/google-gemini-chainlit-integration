import chainlit as cl 
import google.generativeai as genai  
import os


os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"  # Replace with your actual API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = "gemini-2.0-flash"  # Use the model name directly as a string
system_prompt = "You are a helpful assistant that provides information about the Gemini 2.0 model. You can answer questions and provide examples of how to use the model effectively."

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("system_prompt", system_prompt)
    await cl.Message(content=f"System prompt set: {system_prompt}").send()

@cl.on_message
async def handle_message(message):
    system_prompt = cl.user_session.get("system_prompt")
    prompt_with_system = f"You are instructed to do accordingly : {system_prompt} \n\n User: {message.content}"
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 5000,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARRASMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SELF_HARM",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_VIOLENCE",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_ACTS",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_SUBSTANCE",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_WEAPONS",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_ORGANIZATIONS",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONSPIRACY",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]
 
    response = genai.generate_content(
            prompt_with_system,
            generation_config=generation_config,
            safety_settings=safety_settings,
    )
    await cl.Message(content=response.text).send()


if __name__ == "__main__":
    cl.run()