# SpamShield - Intelligent Chat Spam Detection

SpamShield is a Python-based chat application featuring real-time spam message filtering powered by machine learning. It uses a client-server architecture over sockets to provide a lightweight messaging platform with built-in security against spam.

## Project Overview

The project consists of a socket server that intercepts messages and validates them against a pre-trained `RandomForestClassifier` model. If a message is flagged as spam, it is blocked from being broadcast to other connected clients.

### Main Technologies
- **Python 3.12.8**: Primary programming language.
- **Scikit-learn**: Used for the machine learning model (Random Forest).
- **Joblib**: Used for model serialization.
- **SQLite**: `users.db` is present, likely intended for user management and authentication.
- **Sockets & Threading**: Core technologies for real-time, multi-client chat communication.

## Project Structure

- `Chat_Server.py`: The multi-threaded socket server that handles message routing and real-time numerical feature extraction for spam filtering.
- `Client.py`: A command-line client for users to connect and chat.
- `Train_spam_model.py`: A script for training the spam detection model using numerical datasets.
- `spam_detection_dataset.csv`: The base dataset for training.
- `output/`: Contains enhanced and modified versions of the spam dataset.
- `templates/`: HTML templates (`index.html`, `login.html`, `register.html`), indicating a planned or secondary web interface.
- `users.db`: SQLite database for user data.

## Building and Running

### Prerequisites
- Python 3.12.8
- Required packages: `scikit-learn`, `pandas`, `joblib`

### Steps
1. **Train the Model**:
   Run the training script to generate `spam_model.pkl`.
   ```bash
   ./venv/bin/python Train_spam_model.py
   ```

2. **Start the Chat Server**:
   ```bash
   ./venv/bin/python Chat_Server.py
   ```

3. **Run the Client**:
   ```bash
   ./venv/bin/python Client.py
   ```

## Development Conventions & Notes

- **Numerical Features**: The model is trained on specific features extracted from messages: `num_links`, `num_words`, `has_offer`, `sender_score`, `all_caps`, and `links_per_word`.
- **Feature Extraction**: `Chat_Server.py` handles the extraction of these features in real-time for each incoming message.
- **Web Interface**: The templates suggest a Flask or Django component that is currently not fully integrated with the socket server.
- **Persistence**: User authentication using `users.db` should be integrated into the server-side logic.
