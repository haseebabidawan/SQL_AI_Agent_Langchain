# 💼 PostgreSQL Database AI-Agent

🚀 An intelligent AI-powered SQL agent that allows users to interact with a PostgreSQL database using natural language queries. Built using **LangChain, OpenAI/Groq LLMs, and Streamlit**, this AI-agent can generate, execute, and refine SQL queries dynamically while providing explanations for the results.

## ✨ Features

✅ **Natural Language to SQL** - Ask questions in plain English, and the AI converts them into SQL queries.  
✅ **Streaming Responses** - Get real-time streaming outputs for a seamless experience.  
✅ **SQL Query Optimization** - The agent refines queries to ensure efficiency.  
✅ **Data Modification Capabilities** - Perform `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and more.  
✅ **Interactive UI** - A user-friendly Streamlit interface for easy interaction.  
✅ **Error Handling** - Automatically detects and corrects SQL errors.  

## 📌 Tech Stack

- **Python** 🐍 - Core language.
- **Streamlit** 🎨 - UI for interaction.
- **LangChain** 🔗 - Manages LLM-powered SQL execution.
- **PostgreSQL** 🗄 - Database.
- **OpenAI/Groq LLMs** 🧠 - Powers the AI agent.

## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Postgres-SQL-AI-Agent.git
cd Postgres-SQL-AI-Agent
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file and add your database credentials:
```
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
GROQ_API_KEY=your_groq_api_key
```

### 5️⃣ Run the Application
```bash
streamlit run Sql_AIagent_app.py
```

## 🖥️ Usage
1️⃣ Enter your database credentials in the UI sidebar.
2️⃣ Type your query in natural language.
3️⃣ The AI agent converts it into SQL and fetches results.
4️⃣ Get real-time streaming responses with explanations.

## 🛠 Troubleshooting
- **Connection Issues?** Ensure your database credentials are correct.
- **Query Not Executing?** Check the SQL syntax in the output.
- **Streaming Not Working?** Restart the Streamlit server and verify dependencies.

## 🎯 Future Enhancements
- 🔹 Support for multiple databases (MySQL, MSSQL, etc.).
- 🔹 Advanced query optimization techniques.
- 🔹 Integration with visualization tools like Power BI.

## 🤝 Contributing
PRs are welcome! Feel free to submit issues or feature requests.

## 📜 License
MIT License. See `LICENSE` for details.

## 🌟 Show Your Support
Give a ⭐ on [GitHub](https://github.com/yourusername/Postgres-SQL-AI-Agent) if you like this project!

