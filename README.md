# ZTLAB Backend

This is the backend for the ZTLAB project, a React Native-based wrapper app for ETLAB, designed to enhance student access to attendance tracking and timetables. The backend is built with **FastAPI** and powers the app’s functionalities by providing real-time data from ETLAB.

Checkout the Frontend at https://github.com/MZaFaRM/ZTLAB

## Features

- **Attendance Calculation**: Provides endpoints to calculate how many more classes students need to attend to meet the minimum attendance requirement.
- **Timetable Data**: Sends structured timetable information with an enhanced user experience in mind.
- **ETLAB Data Fetching**: Integrates with ETLAB’s backend to fetch and process real-time student data.

## Tech Stack

- **FastAPI**: A high-performance backend framework for building APIs quickly.
- **Python**: The core programming language used for logic and integration.
- **SQLAlchemy**: ORM for database interactions.
- **Render**: Free hosting platform used for this project’s backend.

## Performance Considerations

The backend is hosted on **Render**, a free hosting service. This leads to potential delays when the server spins down after inactivity for more than an hour. The first request after the server restarts may take up to 1-2 minutes, though performance is fast after this initial load.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/MZaFaRM/ZTLAB-Backend.git
   cd ZTLAB-Backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI app:
   ```bash
   uvicorn main:app --reload
   ```

## Motivation

This project was initially created to make it easier for students to track their attendance and manage their timetables with a more user-friendly interface. The backend ensures seamless interaction with the ETLAB platform.





