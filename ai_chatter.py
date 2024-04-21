import google.generativeai as genai
import config

def connect_gemini():
    genai.configure(api_key=config.get_gemini_key())

def gemini_setup():
    safety_settings = [ {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }, {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }, {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }, {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    global convo
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                safety_settings=safety_settings)
    convo = model.start_chat()

def get_response(content: str) -> str:
    convo.send_message(content=content)
    return convo.last.text