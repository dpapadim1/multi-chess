CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    score NUMERIC NOT NULL DEFAULT 1000.00
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,
    joiner_id INTEGER,
    status TEXT NOT NULL DEFAULT 'waiting',
    turn TEXT NOT NULL DEFAULT 'white',
    board TEXT NOT NULL,
    state INTEGER NOT NULL DEFAULT 1, -- 1 for ongoing, 2 for creator win, 3 for joiner win, 4 for draw 
    move_index INTEGER NOT NULL DEFAULT 0, -- 0 for no move, 1 for first move, etc.
    FOREIGN KEY (creator_id) REFERENCES users(id),
    FOREIGN KEY (joiner_id) REFERENCES users(id)
);