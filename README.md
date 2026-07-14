# SmartTodo 🎯

SmartTodo is a complete, production-ready, and beautiful task management dashboard application built using **Python** and **Streamlit**. It features a modern translucent **glassmorphism user interface**, dynamic chart visualizations using **Plotly**, and robust local file caching via a **JSON database**.

---

## 🚀 Key Features

* **Professional Dashboard Layout**: Glassmorphic styling system supporting both Light and Dark modes.
* **Cohesive Sidebar Navigation**: Easily switch between pages and monitor high-level completion statistics, real-time date/time stamps, and progress indicators at a glance.
* **Complete Task CRUD Operations**:
  * **Create**: Full-featured task entry form with input validation (Title is mandatory).
  * **Read**: Interactive grid showing detailed cards. Expand to view full task information.
  * **Update**: Quick one-click status transitions (Pending ➔ Completed) and full inline form updates.
  * **Delete**: Secure deletion process requiring user confirmation.
* **Dynamic Search & Filters**: Filter tasks by category, priority, status, due date, or overdue metrics. Search keywords across Title, Description, and Category text.
* **Advanced Sort Options**: Order tasks by Priority level, Due Dates, Alphabetical sequence, Newest, or Oldest entries.
* **Plotly Visual Charts**: Graphical widgets displaying Task Status distribution (Pie Chart), Priority Breakdown (Bar Chart), and Task growth histories (Cumulative Line Chart).
* **Data Portability**: Easily download your tasks as structured CSV or JSON files. Restore/Import JSON backups dynamically.
* **Resilient Storage**: Utilizes a local `database.json` file. The application is designed to never crash if this file is empty, corrupted, or missing, and will automatically heal/reinitialize it when launched.

---

## 📁 Project Folder Structure

```text
SmartTodo/
│── app.py                   # Main entry point and Dashboard page
│── utils.py                 # Core business logic, DB handlers, and UI helper functions
│── database.json            # Local JSON storage file (auto-generated)
│── requirements.txt         # Project dependencies
│── .env                     # Environment settings (contains versioning, keys)
│── .env.example             # Example environment file template
│── README.md                # Comprehensive documentation
│── assets/
│     └── style.css          # Glassmorphism, animations, and badge stylesheets
│── pages/
│     ├── 1_Task_Manager.py  # Create new task form
│     ├── 2_History.py       # Task list cards, search/filter, and Plotly analytics
│     └── 3_Settings.py      # Import/export, purge databases, and theme tips
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8 or higher** installed on your system.

### 2. Clone/Copy Project
Ensure all project files are located inside your active directory.

### 3. Set Up Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Inside `.env`, you can customize properties if necessary:
* `APP_NAME`: Title of the application.
* `VERSION`: Current build version.
* `SECRET_KEY`: System keys (useful for production sessions).

### 4. Install Dependencies
Run pip to install the required libraries:
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run Locally

Start the Streamlit development server by running the following command in your terminal from the project root:

```bash
streamlit run app.py
```

A browser window should open automatically at `http://localhost:8501`. If it does not, copy and open the URL displayed in your terminal.

---

## 🚢 Deployment Instructions

### Deploying to Streamlit Community Cloud
1. Push your project code to a public GitHub repository.
2. Visit [Streamlit Share](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **New app**, select your repository, branch (`main`), and set the main file path to `app.py`.
4. Add environment variables listed in `.env` into the Streamlit App Settings -> Secrets panel:
   ```ini
   APP_NAME="SmartTodo"
   VERSION="1.0"
   SECRET_KEY="your-production-secret-key"
   ```
5. Click **Deploy!** Your app will be live with an SSL certificate.

### Containerization with Docker
1. Create a `Dockerfile` in the root:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . .
   RUN pip install --no-cache-dir -r requirements.txt
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```
2. Build and run your Docker container:
   ```bash
   docker build -t smarttodo:latest .
   docker run -p 8501:8501 smarttodo:latest
   ```

---

## 🔮 Future Improvements

1. **User Authentication**: Implement registration/login options to separate individual databases using secure JWT tokens.
2. **Subtask Management**: Add nested lists inside task items to track progress of smaller sub-goals.
3. **Task Reminders & Notifications**: Integrate browser push notifications or email alerts for items whose due dates are approaching.
4. **Calendar Syncing**: Enable downloading tasks as `.ics` calendars to sync with Google Calendar or Apple Calendar.
