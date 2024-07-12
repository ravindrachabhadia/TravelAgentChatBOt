
# Travel Agent Chatbot

Welcome to the Travel Agent Chatbot project! This repository contains the code for a travel-related chatbot that can answer general travel inquiries using OpenAI's GPT-4 and provide specific travel package details from a proprietary database.

## Features

- **FastAPI Backend**: Handles incoming queries and processes them based on the type (proprietary or general).
- **Database Integration**: Stores and retrieves travel package details using SQLite and SQLAlchemy.
- **NLP with SpaCy**: Extracts locations from user queries to match travel packages.
- **OpenAI GPT-4 Integration**: Handles general travel-related questions.
- **Streamlit Frontend**: Simple and interactive user interface for submitting queries.

## Project Structure

- `backend.py`: FastAPI application to handle incoming queries and interact with the database and OpenAI API.
- `frontend.py`: Streamlit application to provide a user interface for interacting with the chatbot.
- `populate_db.py`: Script to populate the SQLite database with sample travel packages.
- `requirements.txt`: List of Python dependencies required for the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- SQLite

### Installation

1. Clone the repository:

   \`\`\`sh
   git clone https://github.com/yourusername/travel-agent-chatbot.git
   cd travel-agent-chatbot
   \`\`\`

2. Create and activate a virtual environment:

   \`\`\`sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   \`\`\`

3. Install the required dependencies:

   \`\`\`sh
   pip install -r requirements.txt
   \`\`\`

4. Set your OpenAI API key as an environment variable:

   \`\`\`sh
   export OPENAI_API_KEY="your_openai_api_key"  # On Windows use `set OPENAI_API_KEY=your_openai_api_key`
   \`\`\`

### Setting Up the Database

1. Run the `populate_db.py` script to create the database and populate it with sample data:

   \`\`\`sh
   python populate_db.py
   \`\`\`

### Running the Backend

1. Start the FastAPI application:

   \`\`\`sh
   uvicorn backend:app --reload
   \`\`\`

   The backend will be running at `http://127.0.0.1:8000`.

### Running the Frontend

1. Start the Streamlit application:

   \`\`\`sh
   streamlit run frontend.py
   \`\`\`

   The frontend will be running at `http://localhost:8501`.

## Usage

1. Open your web browser and go to `http://localhost:8501`.
2. Enter your travel-related question in the text input field and click "Submit".
3. The chatbot will respond with either specific travel package details (if matched) or a general travel-related answer.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For any questions or feedback, please contact [chabhadia.ra@northeastern.edu](mailto:chabhadia.ra@northeastern.edu).
