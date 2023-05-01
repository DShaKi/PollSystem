import sqlite3
import poll

conn = sqlite3.connect('PollDB.db')

def addPoll(poll: poll.Poll) -> None:
    options = ""
    votes = ""
    for i in poll.options:
        options += i
        votes += str(0)
        if i != poll.options[-1]:
            options += ','
            votes += ','
    conn.execute("INSERT INTO Poll VALUES(?, ?, ?, ?)", (poll.id, poll.title, options, votes, ))
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

def participate(pollid: int, option: int) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Poll")
    db_polls = cursor.fetchall()
    for p in db_polls:
        if p[0] == pollid:
            options: list[str] = p[3].split(',')
            votes = ""
            for i in range(len(options)):
                if i == option-1:
                    votes += str(int(options[i])+1)
                    if i != len(options)-1:
                        votes += ','
                else:
                    votes += options[i]
                    if i != len(options)-1:
                        votes += ','
            conn.execute("UPDATE Poll SET Votes = (?) WHERE ID = (?)", (votes, pollid, ))
            conn.commit()
            break

def addUser(user: poll.User) -> None:
    conn.execute("INSERT INTO User VALUES(?, ?, ?)", (user.id, user.email, user.password, ))
    conn.commit()

def getUsers() -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    db_users = cursor.fetchall()
    users = []
    for u in db_users:
        users.append(poll.User(u[0], u[1], u[2]))
    return users