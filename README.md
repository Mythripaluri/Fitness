# FitLens: Your AI-Powered Fitness Companion

[Watch the demo](assets/demo.mp4)

## Overview

FitLens is an innovative AI-powered fitness assistant that leverages computer vision to provide real-time feedback on your exercise form. Built using Python, Flask, and the robust Mediapipe framework, FitLens analyzes your movements through your webcam and guides you towards performing exercises correctly.

## Getting Started

### Prerequisites

**Backend (Python):**

* Python 3.9 or later
* Flask
* Mediapipe
* gTTS
* Pyglet
* OpenCV
* NumPy

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/Mythripaluri/Fitness.git](https://github.com/Mythripaluri/Fitness.git)
    cd Fitness
    ```

2.  **Backend Setup:**

    * Navigate to the `backend` directory:

        ```bash
        cd backend
        ```

    * Create a virtual environment (recommended):

        ```bash
        python3 -m venv my_env
        source my_env/bin/activate  # On macOS/Linux
        my_env\Scripts\activate # On Windows
        ```

    * Install dependencies:

        ```bash
        pip install -r requirements.txt
        ```
        * If there is no requirements.txt file, you can install the dependencies manually:
        ```bash
        pip install flask opencv-python mediapipe numpy gtts pyglet
        ```

3.  **Frontend Setup:**

    * Navigate to the `frontend` directory:

        ```bash
        cd ../frontend
        ```

    * Install Node.js dependencies:

        ```bash
        npm install
        ```

## Running the Application

1.  **Start the Backend:**

    * Navigate to the `backend` directory:

        ```bash
        cd ../backend
        ```

    * Activate the virtual environment (if not already active):

        ```bash
        source my_env/bin/activate # On macOS/Linux
        my_env\Scripts\activate # On windows
        ```

    * Run the Flask application:

        ```bash
        python app.py
        ```

2.  **Start the Frontend:**

    * Navigate to the `frontend` directory:

        ```bash
        cd ../frontend
        ```

    * Run the Vite development server:

        ```bash
        npm run dev
        ```

3.  **Access the Application:**

    * Open your web browser and navigate to `http://localhost:5173/`.

