# GEN AI: Developing a General Chatbot for Medical Knowledge

![Project Logo](path_to_logo_image) <!-- Optional: Add your project logo -->

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

- **Framework:** Streamlit
- **Language Models:** LangChain, GroQ Model
- **Database:** Pinecone (Vector Database), MongoDB
- **APIs:** HERE API, Azure Speech
- **Other Tools:** RAG (Retrieval-Augmented Generation)

## Architecture

![Architecture Diagram](path_to_architecture_diagram) <!-- Optional: Add architecture diagram -->

1. **User Interface:** Built with Streamlit, providing an interactive chat interface.
2. **Natural Language Processing:** LangChain and GroQ model handle user queries.
3. **Knowledge Base:** Vector database in Pinecone stores and retrieves information from a comprehensive medical book.
4. **Voice Features:** Azure Speech services manage voice input and text-to-speech functionalities.
5. **Doctor Finder:** HERE API locates nearby healthcare providers based on user input.
6. **Data Storage:** MongoDB stores chat histories securely.

## Installation

### Prerequisites

- Python 3.7 or higher
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


<img width="1417" alt="Screenshot 2024-09-14 at 9 45 48 PM" src="https://github.com/user-attachments/assets/fc32d095-722f-4bc1-9a52-895db4afb856">
