# Personalized Learning Tutor using Reinforcement Learning

This project is an AI-powered web application designed to deliver a truly personalized learning experience. It addresses the core challenge of traditional e-learning—its one-size-fits-all approach—by leveraging a Reinforcement Learning (RL) agent.

The application ingests a student's performance data in real-time and uses an intelligent backend to dynamically select the optimal next question, ensuring that learners are always appropriately challenged. This adaptive system aims to maximize engagement, improve knowledge retention, and provide actionable insights into a student's learning journey through an interactive dashboard.

---

## 🛠️ Technology Stack

* **Frontend:** React.js
* **Backend:** Python with Flask
* **Database:** MongoDB (via MongoDB Atlas)
* **AI/ML Libraries:** NumPy
* **Version Control:** Git & GitHub

---

## ⚙️ How to Run This Project

To run this project, you need to start both the frontend and backend servers simultaneously in two separate terminals.

### 1. Backend Server (Flask)

```bash
# Navigate to the backend project folder
cd learning-tutor-backend

# Activate the Python virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (if you haven't already)
pip install Flask Flask-Cors pymongo numpy

# Run the server
python app.py

# The backend will be running on http://localhost:5000
````

### 2\. Frontend Server (React)

```bash
# Navigate to the frontend project folder
cd learning-tutor

# Install dependencies (only needs to be done once)
npm install

# Run the development server
npm start

# The frontend will open automatically at http://localhost:3000
```

-----

## 📈 Project Progress

### Summary of Work (Week of 11 OCT 2025)

  * **Task 1 (System Architecture):** Designed and finalized the 3-tier application architecture (React Frontend -\> Flask Backend -\> MongoDB). Documented the complete user learning flow, from initial assessment to adaptive practice.
  * **Task 2 (Full-Stack Development):** Developed the foundational frontend components in React (`Quiz`, `Dashboard`, `Results`) and built the backend API endpoints in Flask to serve questions and receive user data.
  * **Task 3 (Database & Integration):** Successfully integrated the frontend and backend, established a connection to the MongoDB Atlas database, and implemented the logic to store user quiz performance.

### Proof of Work

<img width="1917" height="962" alt="image" src="https://github.com/user-attachments/assets/43c8585d-3f69-48d6-9c95-b2c1e783e716" />

<img width="1918" height="872" alt="image" src="https://github.com/user-attachments/assets/8430265c-3df8-445a-83fd-10df399b0946" />


### Individual Contributions

  * **@AasrithSairam**:
      * Authored the system architecture and defined the project workflow.
      * Developed the complete full-stack application, including all React components and Flask API endpoints.
      * Set up and connected the MongoDB database, implementing the data submission logic.
      * Established the project's version control system and managed all initial commits.

