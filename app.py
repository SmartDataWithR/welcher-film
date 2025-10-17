import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel


class MyMovieOutput(BaseModel):
    title: str
    director: str
    main_actors: list[str]
    release_year: str

st.title("Welcher Film ist gemeint?")

description = st.chat_input(placeholder="Bitte beschreibe den Film")
year_range = st.select_slider(
    "Veröffentlichungsjahr",
    options=range(1900, 2025),
    value=(1990, 2020)
)

print(year_range[0])
  
if description is not None:
    messages = [
    ("system", "Du bist ein Filmexperte. Gib mir den am besten passenden Film basierend auf der Beschreibung und ihrem kommerziellen Erfolg in absteigender Reihenfolge. Verwende strikt das vorgebene Schema {format_instructions}. Die Veröffentlichungsjahre des Filmes sollte zwischen {year_min} und {year_max} liegen. {year_min} und {year_max} sind die minimale und maximale Jahreszahl in der Liste der Veröffentlichungsjahre."),
    ("user", "Handlung: {plot}")
    ]

    parser = PydanticOutputParser(pydantic_object=MyMovieOutput)

    prompt_template = ChatPromptTemplate.from_messages(messages).partial(format_instructions=parser.get_format_instructions())

    MODEL_NAME = "openai/gpt-oss-120b"
    model = ChatGroq(model=MODEL_NAME, api_key=os.getenv("GROQ_API_KEY"))

    chain = prompt_template | model | parser
    res = chain.invoke({"plot": description, "year_min": year_range[0], "year_max": year_range[1]})
    st.markdown(f"**Titel**: {res.title}")
    st.markdown(f"**Regisseur**: {res.director}")
    st.markdown(f"**Hauptdarsteller**: {'; '.join(res.main_actors)}")
    st.markdown(f"**Erscheinungsjahr**: {res.release_year}")