import sqlite3
import poll

conn = sqlite3.connect('PollDB.db')

def addPoll(poll: poll.Poll, user: poll.User) -> None:
    options = ""
    votes = ""
    for i in poll.options:
        options += i
        votes += str(0)
        if i != poll.options[-1]:
            options += ','
            votes += ','
    conn.execute("INSERT INTO Poll VALUES(?, ?, ?, ?, ?)", (poll.id, 1, poll.title, options, votes, ))
    # Adding the created poll to user's profile
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE ID = (?)", (user.id, ))
    db_user = cursor.fetchall()
    updated_user_polls = db_user[0][3]+str(poll.id)+","
    conn.execute("UPDATE User SET CreatedPolls = (?) WHERE ID = (?)", (updated_user_polls, user.id))
    conn.commit()

def getPolls() -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Poll")
    db_polls = cursor.fetchall()
    polls = []
    for p in db_polls:
        options = p[2].split(',')
        polls.append(poll.Poll(p[0], p[1], p[2], options))
    return polls

def delPoll(user: poll.User, pollid: int) -> None:
    conn.execute("DELETE FROM Poll WHERE ID = (?)", (pollid, ))
    updated_user_polls = ""
    for i in range (len(user.created_polls)):
        updated_user_polls += user.created_polls[i] + ','
    conn.execute("UPDATE User SET createdPolls = (?) WHERE ID = (?)", (updated_user_polls, user.id))
    conn.commit()

def actiPoll(pollid: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Poll WHERE ID = (?)", (pollid, ))
    db_poll = cursor.fetchall()
    activation = int(db_poll[0][1])
    print(activation)
    if activation == 1:
        new_activation = 0
    elif activation == 0:
        new_activation = 1
    conn.execute("UPDATE Poll SET Activation = (?) WHERE ID = (?)", (new_activation, pollid, ))
    conn.commit()
    return new_activation

def getPollResults(pollid) -> dict:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Poll WHERE ID = (?)", (pollid, ))
    db_poll = cursor.fetchall()
    options = db_poll[0][3].split(',')
    votes = db_poll[0][4].split(',')
    res = {}
    for i in range(len(options)):
        res[options[i]] = votes[i]
    return res

def participate(pollid: int, option: int, user: poll.Poll) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Poll")
    db_polls = cursor.fetchall()
    for p in db_polls:
        if p[0] == pollid:
            options: list[str] = p[4].split(',')
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
            # Adding the participated poll to user's profile
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE ID = (?)", (user.id, ))
            db_user = cursor.fetchall()
            updated_user_polls = db_user[0][4]+str(pollid)+","
            conn.execute("UPDATE User SET ParticipatedPolls = (?) WHERE ID = (?)", (updated_user_polls, user.id))
            conn.commit()
            break

def addUser(user: poll.User) -> None:
    conn.execute("INSERT INTO User VALUES(?, ?, ?, ?, ?)", (user.id, user.email, user.password, "", "", ))
    conn.commit()

def getUsers() -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    db_users = cursor.fetchall()
    users = []
    for u in db_users:
        cp: list[str] = []
        pp: list[str] = []
        if u[3] != "":
            cp = u[3].split(',')
            cp.pop(-1)
        if u[4] != "":
            pp = u[4].split(',')
            pp.pop(-1)
        users.append(poll.User(u[0], u[1], u[2], cp, pp))
    return users