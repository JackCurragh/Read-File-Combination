import sqlite3
import gzip
import argparse
import os
from Bio import SeqIO

def connect_db(db_name):
    """
    Connect to the SQLite database.

    Args:
        db_name (str): Name of the SQLite database file.

    Returns:
        sqlite3.Connection: SQLite database connection.
    """
    conn = sqlite3.connect(db_name)
    return conn


def create_tables(conn):
    """
    Create the necessary tables in the database from a schema file if the database doesn't exist.

    Args:
        conn (sqlite3.Connection): SQLite database connection.
    """
    c = conn.cursor()

    with open('reads.sql', 'r') as schema_file:
        schema_sql = schema_file.read()
        c.executescript(schema_sql)
    conn.commit()

    c.close()


def insert_read_sequence(conn, sequence, check=False):
    """
    Insert a read sequence into the Reads table. If the sequence already exists, do nothing.

    Args:
        conn (sqlite3.Connection): SQLite database connection.
        sequence (str): Read sequence to insert.

    Returns:
        int: ID of the inserted read sequence.
    """
    c = conn.cursor()

    if check:
        c.execute(f"SELECT read_id FROM Reads WHERE sequence = '{sequence}'")
        data = c.fetchone()
        if data:
            c.close()
            return data[0]
    c.execute(f"INSERT OR IGNORE INTO Reads (sequence) VALUES ('{sequence}')")
    conn.commit()
    read_id = c.lastrowid
    c.close()
    return read_id


def insert_sample(conn, sample_name, metadata=None, check=False):
    """
    Insert sample information into the Samples table.

    Args:
        conn (sqlite3.Connection): SQLite database connection.
        sample_name (str): Name of the sample.
        metadata (str, optional): Additional metadata for the sample.

    Returns:
        int: ID of the inserted sample.
    """
    c = conn.cursor()
    if check:
        c.execute(f"SELECT sample_id FROM Samples WHERE sample_name = '{sample_name}'")
        data = c.fetchone()
        if data:
            c.close()
            return data[0]
    c.execute(f"INSERT INTO Samples (sample_name, metadata) VALUES ('{sample_name}', '{metadata}')")
    conn.commit()
    sample_id = c.lastrowid
    c.close()
    return sample_id


def insert_read_count(conn, read_id, sample_id, count, check=False):
    """
    Insert read count information into the ReadCounts table.

    Args:
        conn (sqlite3.Connection): SQLite database connection.
        read_id (int): ID of the read sequence.
        sample_id (int): ID of the sample.
        count (int): Count of the read in the sample.
    """
    c = conn.cursor()

    if check:
        c.execute(f"SELECT * FROM ReadCounts WHERE read_id = {read_id} AND sample_id = {sample_id}")
        data = c.fetchone()
        if data:
            c.close()
            return
    
    c.execute(f"INSERT INTO ReadCounts (read_id, sample_id, count) VALUES ({read_id}, {sample_id}, {count})")
    conn.commit()
    c.close()


def check_gzipped(file_name):
    """
    Check if a file is gzipped by examining its header.

    Args:
        file_name (str): Name of the file to check.

    Returns:
        bool: True if the file is gzipped, False otherwise.
    """
    with open(file_name, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'
    

def write_fasta(conn, fasta_file):
    """
    write all reads into a fasta file
    
    Args:
        conn (sqlite3.Connection): SQLite database connection.
        fasta_file (str): Name of the fasta file to write to.
    """
    c = conn.cursor()
    c.execute('''SELECT read_id, sequence FROM Reads''')
    data = c.fetchall()
    c.close()
    with open(fasta_file, 'w') as f:
        for row in data:
            f.write(f'>{row[0]}\n')
            f.write(f'{row[1]}\n')


def main(args):

    if not os.path.exists(args.database):
        conn = connect_db(args.database)
        create_tables(conn)

    else:
        conn = connect_db(args.database)

    sample_name =  args.fasta.split('/')[-1].split('.')[0]
    sample_id = insert_sample(conn, sample_name)

    if check_gzipped(args.fasta):
        with gzip.open(args.fasta, 'rt') as handle:
            for record in SeqIO.parse(handle, 'fasta'):
                read_id = insert_read_sequence(conn, str(record.seq))
                count = int(record.id.split('_x')[-1])
                insert_read_count(conn, read_id, sample_id, count)  

    else:
        for record in SeqIO.parse(args.fasta, 'fasta'):
            read_id = insert_read_sequence(conn, str(record.seq))
            count = int(record.id.split('_x')[-1])
            insert_read_count(conn, read_id, sample_id, count)  

    write_fasta(conn, 'combined.fasta')  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine fasta files into a single SQLite3 database')
    parser.add_argument('-f', '--fasta', help='Input fasta file', required=True)
    parser.add_argument('-d', '--database', help='Output database name', required=True)
    args = parser.parse_args()
    main(args)
