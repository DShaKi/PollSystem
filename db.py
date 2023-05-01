import sqlite3
import poll

conn = sqlite3.connect('PollDB.db')

def addPoll(poll: poll.Poll) -> None:
    options = ""
    for i in poll.options:
        options += i
        if i != poll.options[-1]:
            options += ','
    conn.execute("INSERT INTO Poll VALUES(?, ?, ?)", (poll.id, poll.title, options, ))
    conn.commit()
    
def getPolls() -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Poll")
    db_polls = cursor.fetchall()
    polls = []
    for p in db_polls:
        options = p[2].split(',')
        polls.append(poll.Poll(p[0], p[1], options))
    return polls

def participate(pollid: int, option: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Poll")
    db_polls = cursor.fetchall()
    for p in db_polls:
        if p[0] == pollid:
            try:
                conn.execute(f"ALTER TABLE Poll ADD COLUMN Option{option} 'INTEGER'")
                conn.commit()
            except:
                pass
            conn.execute(f"UPDATE Poll SET Option{option} = Option{option}+1 WHERE ID = (?)", (pollid, ))
            conn.commit()

def addUser(user: poll.User) -> None:
    conn.execute("INSERT INTO User VALUES(?, ?, ?)", (user.id, user.email, user.password))
    conn.commit()

def getUsers() -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    db_users = cursor.fetchall()
    users = []
    for u in db_users:
        users.append(poll.User(u[0], u[1], u[2]))
    return users