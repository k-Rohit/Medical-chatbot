# GEN AI: Developing a General Chatbot for Medical Knowledge

## Table of Contents

- [Project Overview](#project-overview)
  - [Problem Statement](#problem-statement)
  - [Objective](#objective)
  - [Expected Outcomes](#expected-outcomes)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Prototype Video](#prototype-video)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

### Problem Statement

Patients and healthcare providers need an intelligent assistant to provide accurate medical information, preliminary assessments, and support in healthcare management. There is a need for up-to-date information on medical conditions, treatments, and medications.

### Objective

Develop a general chatbot where patients can input symptoms and receive preliminary assessments and recommendations. Additionally, the system should assist patients in scheduling appointments with healthcare providers. Providing personalized health advice and reminders based on individual health data and preferences can improve patient outcomes.

### Expected Outcomes

- **Accuracy:** The chatbot should provide reliable and accurate information, avoiding false or misleading content.
- **Chat History:** Users should have access to their chat history for at least one week.

## Features

1. **Medical Information Retrieval:**
   - Utilizes a knowledge base containing a book of signs and symptoms of diseases.
   - Provides accurate responses to user queries about medical conditions, treatments, and medications.

2. **Voice Interaction:**
   - **Voice Input:** Users can speak their symptoms or queries.
   - **Text-to-Speech:** Responses can be listened to using Azure Speech services.

3. **Doctor Finder:**
   - Integrates HERE API to locate nearby doctors based on the user's address.

4. **Chat History Management:**
   - Stores all chat interactions in MongoDB, allowing users to access their chat history for up to a week.

## Technologies Used

- **Framework:** Streamlit, Crew AI
- **Language Models:** LangChain, GroQ Model
- **Database:** Pinecone (Vector Database), MongoDB
- **APIs:** HERE API, Azure Speech
- **Other Tools:** RAG (Retrieval-Augmented Generation)

## Architecture

1. **User Interface:** Built with Streamlit, providing an interactive chat interface.
2. **Natural Language Processing:** LangChain and GroQ model handle user queries.
3. **Knowledge Base:** Vector database in Pinecone stores and retrieves information from a comprehensive medical book.
4. **Voice Features:** Azure Speech services manage voice input and text-to-speech functionalities.
5. **Doctor Finder:** HERE API locates nearby healthcare providers based on user input.
6. **Data Storage:** MongoDB stores chat histories securely.

## Installation

### Prerequisites

- Python 3.10 or higher
- Git
- MongoDB account
- Pinecone account
- HERE API account
- Azure Speech account

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/medical-chatbot.git
   cd medical-chatbot
2. Create and Activate a Virtual Environment:

```bash
conda create -n myenv
conda activate myenv
```

3. Install requirements.txt
```bash
 pip install -r requirements.txt
```

4. Create a .env file

```
PINECONE_API_KEY=your_pinecone_key
MONGODB_URI=your_mongodb_uri
HERE_API_KEY=your_here_api_key
AZURE_SPEECH_KEY=your_azure_speech_key
```

5. Run the application
```bash
streamlit run app.py
```


