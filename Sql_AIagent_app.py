import os
from IPython.display import Markdown, HTML, display
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
# Load environment variables
load_dotenv()


# Streamlit UI Tittle
st.title("💡 PostgreSQL AI Assistant Agent")
st.markdown("""This is the **PostgresSQL Database AI-Agent** built using Open Source **Groq** and **LangChain**.  
🚀 Powered by the latest advancements in AI for efficient database interaction. 📈""")
st.divider()


#Creating a session state for messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = []
    
# Store inputs in session state to persist across reruns
if "DB_USER" not in st.session_state:
    st.session_state.DB_USER = ""
if "DB_PASSWORD" not in st.session_state:
    st.session_state.DB_PASSWORD = ""
if "DB_HOST" not in st.session_state:
    st.session_state.DB_HOST = ""
if "DB_PORT" not in st.session_state:
    st.session_state.DB_PORT = ""
if "DB_NAME" not in st.session_state:
    st.session_state.DB_NAME = ""
if "db_con" not in st.session_state:
    st.session_state.db_con = None    
    
def database_con(): 

    st.sidebar.title("Enter Postgres-DB Credentials")
    st.session_state.DB_USER = st.sidebar.text_input("**Enter Database Username:**", key="username")
    st.session_state.DB_PASSWORD = st.sidebar.text_input("**Enter Database Password:**", type="password")
    st.session_state.DB_HOST = st.sidebar.text_input("**Enter Host name:**", key="hostname")
    st.session_state.DB_PORT = st.sidebar.text_input("**Enter PORT number:**", key="port")
    st.session_state.DB_NAME = st.sidebar.text_input("**Enter Database Name:**", key="dbname")


    # Database URL


    connect_btt = st.sidebar.button("Connect")

    if connect_btt:
        if not st.session_state.DB_USER or not st.session_state.DB_PASSWORD or not st.session_state.DB_HOST or not st.session_state.DB_PORT or not st.session_state.DB_NAME:
            st.sidebar.error("Please fill in all required fields before proceeding.")
            st.stop()
        db_url = f"postgresql+psycopg2://{st.session_state.DB_USER}:{st.session_state.DB_PASSWORD}@{st.session_state.DB_HOST}:{st.session_state.DB_PORT}/{st.session_state.DB_NAME}"
        try:
            db = SQLDatabase.from_uri(db_url)
            st.sidebar.success("**Database connection successful.**")
            return db
        except Exception as e:
            st.sidebar.error(f"**Error connecting to database**: {e}")
            exit()
    




def main():

    

    if st.session_state.db_con is None:
        st.session_state.db_con = database_con()
        # st.sidebar.error("Please Enter credentials to connect to Database.")

    if st.session_state.db_con:

        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")


        # Define the agent instructions and format
        MSSQL_AGENT_PREFIX = """
        You are an agent designed to interact with a SQL database.
        ## Instructions:
        - Given an input question, create a syntactically correct {dialect} query
        to run, then look at the results of the query and return the answer.
        - Unless the user specifies a specific number of examples they wish to
        obtain, **ALWAYS** limit your query to at most {top_k} results.
        - You can order the results by a relevant column to return the most
        interesting examples in the database.
        - Never query for all the columns from a specific table, only ask for
        the relevant columns given the question.
        - You have access to tools for interacting with the database.
        - You MUST double check your query before executing it. If you get an error
        while executing a query, rewrite the query and try again.
        - You can also make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
        to the database.
        - You can also make any DDL statements (CREATE, ALTER, DROP etc.)
        to the database.
        - DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS
        OF THE CALCULATIONS YOU HAVE DONE.
        - Your response should be in Markdown. However, **when running a SQL Query
        in "Action Input", do not include the markdown backticks**.
        Those are only for formatting the response, not for executing the command.
        - ALWAYS, as part of your final answer, explain how you got to the answer
        on a section that starts with: "Explanation:". Include the SQL query as
        part of the explanation section.
        - If the question does not seem related to the database, just return
        "I don\'t know" as the answer.
        - Only use the below tools. Only use the information returned by the
        below tools to construct your query and final answer.
        - Do not make up table names, only use the tables returned by any of the
        tools below.

        ## Tools:
        """

        MSSQL_AGENT_FORMAT_INSTRUCTIONS = """
        ## Use the following format:

        Question: the input question you must answer.
        Thought: you should always think about what to do.
        Action: the action to take, should be one of [{tool_names}].
        Action Input: the input to the action.
        Observation: the result of the action.
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer.
        Final Answer: the final answer to the original input question.
        """

        toolkit=SQLDatabaseToolkit(db=st.session_state.db_con, llm=llm)

        # Create the SQL agent
        agent_executor_SQL = create_sql_agent(
            prefix=MSSQL_AGENT_PREFIX,
            format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,
            llm=llm,
            toolkit=toolkit,
            top_k=30,
            verbose=True
        )

        # Display previous chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Please Enter your query here!")
        
        if prompt:
        # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI response
            with st.spinner("Generation Response. Please Wait..."):
                response = agent_executor_SQL.invoke(prompt)

                # Extract AI response content
                ai_response = response if isinstance(response, str) else response.get("output", "No response generated.")

                # Display AI response
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # Clear chat history button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.experimental_rerun()  # Refresh the app


if __name__ == "__main__":
    main()