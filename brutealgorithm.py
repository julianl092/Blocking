from cs50 import SQL
import itertools
import math

db = SQL("sqlite:///blocking.db")

#Defines function to return the total utility of any blocking group OR subgroup of users
def utility(combo):
    #Default utility is zero - will remain as such if none of the users in combo have ranked any of the others
    util = 0
    #For every member in the combo, loop iterates for every member in the combo.
    for i in combo:
        member = db.execute("SELECT * from responses WHERE id = :id", id = i)[0]
        for j in combo:
            for k in range(1, 8):
                #Key iterates through all the possible id columns of the "responses" table, from id1 to id7
                key = f"id{k}"
                #If the ID number found in id1 to id7 matches the ID number of user "j", adds the corresponding rating to total utility
                if str(j) == str(member[key]):
                    util += member[f"rating{k}"]
    return (util)

def main():
    persons = []
    responses = db.execute("SELECT * FROM responses WHERE id > 0")
    for response in responses:
        persons.append(response["id"])

    optimal = {"util": 0, "id1": None, "id2": None}
    n = math.ceil((len(persons))/2)
    combos = itertools.combinations(persons, n)
    for combo in combos:
        others = [x for x in persons if x not in combo]
        totalutil = utility(list(combo)) + utility(others)
        if totalutil > optimal["util"]:
            optimal["util"] = totalutil
            optimal["id1"] = list(combo)
            optimal["id2"] = others

    group1 = [db.execute("SELECT * FROM responses WHERE id = :id", id = person)[0] for person in optimal["id1"]]
    group2 = [db.execute("SELECT * FROM responses WHERE id = :id", id = person)[0] for person in optimal["id2"]]

    return ([group1, group2])