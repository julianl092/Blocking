#This Python file is not used in the algorithm. The Cabot Library RoomBook HTML page has a <select> menu of every firstyear in Harvard College.
#I used insert.py to take the names of every first year from the <option> elements of that menu and insert those names into the "users" table
#of my database. The HTML that I used as argv[1] when I ran this file can be found in names.txt.


from cs50 import get_string
from sys import argv, exit
from cs50 import SQL

db = SQL("sqlite:///blocking.db")

def main():
    # Rejects attempt to run program with more or less than one command-line argument
    if len(argv) != 2:
        print("Usage: insert.py namefile")
        exit(1)

    # Initalizes an empty list to store users
    users = []
    txt = argv[1]

    # Opens txt file from Harvard HTML menu
    with open(txt) as f:
        for line in f:
            # Strips the name and ID from the HTML <option>
            nametemp = str(line).split(">")[1]
            name = nametemp.split("</")[0]
            id = str(line).split('"')[1]

            # Creates a dict with the person's name and ID
            person = {"name": name, "id": id,}

            # Appends dict to list of users
            users.append(person)

    for user in users:
        # Inserts person's name and ID into "users" table of blocking database
        db.execute("INSERT INTO users(name, ID) VALUES(:name, :ID)", name=user["name"], ID=user["id"])

if __name__ == "__main__":
    main()

