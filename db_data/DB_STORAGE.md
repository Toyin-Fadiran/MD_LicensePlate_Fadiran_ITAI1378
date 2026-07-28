# Database Storage

This directory serves as the local storage volume for the application's SQLite database file (`lpr.db`). 

## Architecture Note
This folder strictly contains **application state and data**. 
All database infrastructure code, connection logic, and SQL query executions are completely isolated from this data and are located in `src/database/`.

## Developer Rules

1. **Do Not Commit Data:** The `lpr.db` file generated in this folder is a binary file containing local state. It must not be committed to version control. Ensure `*.db` is included in your project's `.gitignore` file.
2. **Disposable Prototyping:** Because this SQLite database is used for local prototyping and testing, the `lpr.db` file can be safely deleted at any time to execute a hard reset.
3. **Database Seeding:** If the `lpr.db` file is deleted or missing, the Python application will dynamically generate a fresh database upon instantiation and automatically re-seed the authorized vehicles table from the root `authorized_list.csv` file.
