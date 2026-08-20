# Studymate-Bot

Telegram bot for managing university subjects, assignments, deadlines and study progress.

Studymate-Bot is a Python-based productivity bot designed to help students keep track of their university workload directly in Telegram.

## Features

### Subjects
- Create subjects
- View existing subjects
- Delete subjects
- Prevent deleting a subject that still has associated tasks

### Tasks
- Create tasks for a subject
- Add task descriptions
- Set deadlines
- Set task priority
- Mark tasks as completed
- Update task title
- Update task description
- Update task deadline
- Update task priority
- Delete tasks
- Prevent duplicate task titles within the same subject

### Task filtering and tracking
- View all tasks belonging to the current user
- View upcoming tasks
- View overdue incomplete tasks
- View tasks without deadlines
- Count total tasks
- Count completed tasks
- Count tasks with deadlines
- Count tasks without deadlines
- Count overdue tasks

### Statistics
The bot provides an overview of study progress, including:
- total number of subjects
- total number of tasks
- completed and remaining tasks
- tasks with and without deadlines
- overdue tasks
- completion rate
- number of tasks grouped by subject

## Tech Stack

- **Python 3**
- **aiogram** — Telegram Bot API framework
- **SQLAlchemy** — ORM and database access
- **SQLite** — local database
- **pytest** — automated testing
- **python-dotenv** — environment variable management

## Project Structure

```text
Studymate-Bot/
│
├── src/
│   ├── main.py
│   ├── bot.py
│   ├── config.py
│   │
│   └── database/
│       ├── db.py
│       ├── models.py
│       ├── subjects.py
│       ├── tasks.py
│       └── statistics.py
│
├── tests/
│   ├── test_subjects.py
│   ├── test_tasks.py
│   └── test_statistics.py
│
├── docs/
│   └── Project_Specification.md
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Studymate-Bot
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

```text
BOT_TOKEN=your_telegram_bot_token
```

The Telegram bot token should be kept private and must not be committed to the repository.

## Running the Bot

After configuring the environment:

```bash
python -m src.main
```

The bot will start polling Telegram for updates.

## Running Tests

The project uses `pytest` for automated tests.

Run the complete test suite:

```bash
pytest
```

The test suite covers the main database operations and business rules, including:

- subject management
- task management
- user isolation
- duplicate task prevention
- task completion
- deadlines
- overdue and upcoming tasks
- task priorities
- statistics
- update operations

The tests use isolated in-memory SQLite databases, so they do not depend on the local development database.

## Database

Studymate-Bot currently uses SQLite with SQLAlchemy.

The local database is created automatically when the application is initialized.

The database file is intentionally excluded from Git:

```text
*.db
*.sqlite
*.sqlite3
```

This prevents local user data and development databases from being committed to the repository.

## User Data Isolation

Database operations are scoped by Telegram user ID.

A user can only access and modify their own subjects and tasks. This behavior is explicitly covered by the test suite, including checks that users cannot access or modify another user's tasks. fileciteturn16file0L133-L160

## Project Architecture

The project separates Telegram bot logic from database operations.

The main responsibilities are divided into:

- **bot / handlers** — Telegram interaction and user flow
- **database models** — SQLAlchemy data models
- **subjects.py** — subject-related database operations
- **tasks.py** — task-related database operations
- **statistics.py** — study statistics and aggregation
- **db.py** — database engine, session and SQLAlchemy base configuration

This separation keeps the database logic independent from Telegram handlers and makes the core functionality easier to test.

## Testing Philosophy

The project uses isolated test databases instead of the real application database.

Each test creates an in-memory SQLite database and replaces the production session factory with a test session factory. This allows database operations to be tested without modifying real local data. fileciteturn16file3L549-L569

The test suite also checks negative cases, such as:

- accessing another user's tasks
- modifying another user's tasks
- deleting missing tasks
- creating duplicate tasks
- completing an already completed task
- updating a missing task

This helps verify not only that the expected operations work, but also that invalid operations are rejected.

## Screenshots

Screenshots of the Telegram bot interface will be added here.

Recommended screenshots:

1. Main menu
2. Subject management
3. Task creation
4. Task list
5. Task details / update flow
6. Statistics

## What I Learned

While building Studymate-Bot, I worked with:

- Python project structure
- asynchronous programming
- Telegram Bot API
- aiogram
- finite-state machines for multi-step user input
- SQLAlchemy ORM
- SQLite
- database session management
- environment variables
- automated testing with pytest
- Git and GitHub workflow
- writing project documentation

The project was built as a practical way to strengthen my Python development skills and understand how a small application is structured from database layer to user interface.

## Future Improvements

Possible future improvements include:

- database migrations with Alembic
- more advanced task filtering and sorting
- recurring tasks
- reminders and Telegram notifications
- richer statistics
- improved error handling
- deployment to a cloud server
- CI pipeline for automatically running tests

## License

This project is currently intended as a personal portfolio project.
