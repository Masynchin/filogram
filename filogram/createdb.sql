CREATE TABLE IF NOT EXISTS files (
    unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_unique_id TEXT UNIQUE,
    file_id TEXT,
    owner_id INTEGER,
    category TEXT,
    file_name TEXT,
    extension TEXT
);
