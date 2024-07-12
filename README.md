## SaifAI: Your Multipurpose LLM Assistant

SaifAI is a versatile LLM assistant designed to empower your productivity and keep you informed. It leverages the power of Gemini, a large language model, and various APIs to provide a suite of intelligent agents that assist you with tasks, deliver real-time information, and more.

**Demo Video:**

A demo video showcasing SaifAI in action is available. You can find the link to the video in the project repository (or provide a separate link if hosted elsewhere).


https://github.com/user-attachments/assets/df0a5823-e2e3-4c24-80a9-06285b2ed45c



### Features

- **Enhanced Interaction:** The DirectionAgent analyzes your prompts, ensuring they reach the most appropriate agent for optimal results.
- **Screen Reader:** Accesses your screen text to answer your questions based on context and generate text-based responses.
- **Chatter:** Engages in text-based conversations powered by Gemini's LLM capabilities.
- **Note Taker:** Analyzes context and creates files with important notes.
- **Task Agent:** Manages your tasks efficiently with functionalities to add, delete, and list them, incorporating your routine to guide you through your schedule.
- **Real-time Agent:** Provides up-to-date information on time, weather, news, and more.
- **Exit Agent:** Offers a graceful exit from the conversation.

**Please note:** SaifAI is currently optimized for macOS and hasn't been thoroughly tested on Windows systems.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/akhtarmdsaad/SaifAI/
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   This command installs all the necessary libraries listed in the `requirements.txt` file.

**Important Note:**

SaifAI utilizes external APIs that require separate API keys. These keys are not included in the repository for security reasons. You'll need to obtain your own API keys from the following services:

- **Gemini** (API Key)
- **Todoist** ([https://todoist.com/](https://todoist.com/)) (API Key)
- **News API** ([https://newsapi.org/](https://newsapi.org/)) (API Key)
- **OpenWeatherMap** ([https://openweathermap.org/](https://openweathermap.org/)) (API Key)

**Configuration:**

1. Find the file named `private.py` within the project directory.

2. Paste the following code snippet into `private.py`, replacing the placeholders with your obtained API keys:

   ```python
   GEMINI_API_KEY = ["YOUR_GEMINI_API_KEY"]
   TODOIST_API_KEY = "YOUR_TODOIST_API_KEY"
   NEWS_API_KEY = "YOUR_NEWS_API_KEY"
   OPEN_WEATHER_API_KEY = "YOUR_OPEN_WEATHER_API_KEY"
   MY_CITY = "YOUR_CITY"  # Replace with your city name for weather information
   ...
   ```

**Usage:**

1. **Run the Application:**

   Locate the script that initiates SaifAI (e.g., `main.py`). Execute this script using the appropriate command (e.g., `python main.py`).

2. **Interact with Agents:**

   SaifAI's interface will provide instructions on interacting with the various agents. Utilize natural language commands to get assistance from the Screen Reader, Chatter, Note Taker, Task Agent, Real-time Agent, or Exit Agent.


**Development and Contribution:**

We welcome contributions to SaifAI! Please create pull requests adhering to the existing coding style and conventions. Thorough testing of your changes is crucial to ensure functionality and quality.

**Authors:**
- Md Saad Akhtar
