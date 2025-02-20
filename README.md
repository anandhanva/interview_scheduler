# Interview Scheduler

A web-based application developed using Django REST framework for registering and scheduling interview times for candidates and interviewers. Based on the provided times, the available slots are calculated and shared.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/anandhanva/interview_scheduler.git

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv <name_of_env>
   source <name_of_env>/bin/activate

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt

4. Navigate to the project directory:
   ```bash
   cd interview_scheduler

## Prerequisites

    Ensure you have the following installed:

        Python 3.x
        Django
        Django REST Framework
        SQLite (default with Django)
    Also, verify that the virtual environment is activated and running.

## Setup

Database Migration

    To apply database migrations, run the following command:
        python3 manage.py migrate

Start the Development Server

    To start the development server, use:
        python3 manage.py runserver
    The default host will be http://localhost:8000.

## API Usage
    1. Register User (Candidate or Interviewer)

        Endpoint: /api/interview/register_time_slot/

        Request 1 (For Interviewer):
            {
            "name": "InterTest",
            "type": "interviewer",
            "email": "intertest@gmail.com",
            "date": "2025-02-21",
            "hrs_from": "10:00 AM",
            "hrs_to": "01:00 PM"
            }
        
        Request 2 (For Candidate):
            {
            "name": "InterTest",
            "type": "candidate",
            "email": "candidate@gmail.com",
            "date": "2025-02-21",
            "hrs_from": "10:00 AM",
            "hrs_to": "05:00 PM"
            }
        This will register the users date and time slots.

    2. Fetch Available Time Slots
        Endpoint: /api/interview/fetch_time_slot/

        Request:
            {
                "candidate_id": "C2502034386",
                "interviewer_id": "I2502064079"
            }
        This will return the available time slots based on the interviewer and candidate's availability.

## Summary
    To register users (interviewers or candidates), use the /api/interview/register_time_slot/ endpoint.

    To fetch available time slots, use the /api/interview/fetch_time_slot/ endpoint by providing candidate and interviewer IDs.