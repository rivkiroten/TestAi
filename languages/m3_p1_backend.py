# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


# create model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

SYSTEM_TEMPLATE = """
    You are an experienced language teacher. Your student speaks {lang_speak} and wants to learn {lang_teach}.
    The student's level is {level}. Focus on teaching {topic} in {lang_teach}.
    
    Instructions:
    - Adapt your teaching to the {level} level
    - Provide clear explanations in {lang_speak} when needed
    - Give practical examples and exercises appropriate for {level} learners
    - Be patient and encouraging
    - Correct mistakes gently and explain why
    - Use language complexity suitable for {level} students
    - Include pronunciation tips when helpful
"""

template = ChatPromptTemplate(
    [
        ("system", SYSTEM_TEMPLATE),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_input}"),
    ]
)


# Building langchain chain
chain = template | llm | StrOutputParser()

def call_llm(user_input: str, lang_speak: str, lang_teach: str, level: str, topic: str, history: list):
    response = chain.invoke(
        {
            "lang_speak": lang_speak,
            "lang_teach": lang_teach,
            "level": level,
            "user_input": user_input,
            "topic": topic,
            "history": history
        }
    )
    return response