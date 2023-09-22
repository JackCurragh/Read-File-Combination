import sqlite3 
from Bio import SeqIO

def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def create_table(conn, table_name):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, seq_id TEXT, seq TEXT)'''.format(table_name))
    conn.commit()
    c.close()


def insert_data(conn, table_name, seq_id, seq):
    c = conn.cursor()
    c.execute('''INSERT INTO {} (seq_id, seq) VALUES (?, ?)'''.format(table_name), (seq_id, seq))
    conn.commit()
    c.close()


def get_data(conn, table_name):
    c = conn.cursor()
    c.execute('''SELECT * FROM {}'''.format(table_name))
    data = c.fetchall()
    conn.commit()
    c.close()
    return data


def main():
    conn = connect_db('test.db')
    create_table(conn, 'test')
    for record in SeqIO.parse('test.fasta', 'fasta'):
        insert_data(conn, 'test', record.id, str(record.seq))
    data = get_data(conn, 'test')
    print(data)


if __name__ == '__main__':
    main()

    