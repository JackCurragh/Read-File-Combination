CREATE TABLE Reads (
    read_id INTEGER PRIMARY KEY,
    sequence TEXT NOT NULL UNIQUE
);

CREATE TABLE Samples (
    sample_id INTEGER PRIMARY KEY,
    sample_name TEXT NOT NULL,
    metadata TEXT,  -- Add more fields for sample metadata as needed
    UNIQUE(sample_name)
);

CREATE TABLE ReadCounts (
    count_id INTEGER PRIMARY KEY,
    read_id INTEGER,
    sample_id INTEGER,
    count INTEGER,
    FOREIGN KEY (read_id) REFERENCES Reads(read_id),
    FOREIGN KEY (sample_id) REFERENCES Samples(sample_id),
    UNIQUE (read_id, sample_id)
);

