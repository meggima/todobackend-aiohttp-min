CREATE TABLE tasks(
    'task_id' INTEGER PRIMARY KEY,
    'title' TEXT NOT NULL,
    'completed' BIT NOT NULL,
    'order' INTEGER NOT NULL
);

CREATE TABLE tags(
    'tag_id' INTEGER PRIMARY KEY,
    'title' TEXT NOT NULL
);

CREATE TABLE task_tags(
    'task_id' INTEGER NOT NULL,
    'tag_id' INTEGER NOT NULL,
    PRIMARY KEY (task_id, tag_id)
);