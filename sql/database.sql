CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    category_id INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    UNIQUE(month, category_id),
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

INSERT INTO categories(name) VALUES ('Alimentari');
INSERT INTO categories(name) VALUES ('Trasporti');