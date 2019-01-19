from cs50 import SQL
import itertools
import math

#https://networkx.github.io/
#NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
import networkx as nx

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

#Defines function to create a graph from an iterable and then return the optimal matching of that graph
def match(inlist, G, b):
    for j in inlist:
        #Adds a graph node for every element of the input list
        G.add_node(j)

        #Subsequent code manages the edge creation between the nodes of the graph.
        #Ultimately, we must create a list of ints called "combo" to pass into the utility function.

        #If on matching Level1, then input elements are single ID numbers and temp1 can be a list with 1 int
        if isinstance(j, int):
            temp1 = [j]
        elif isinstance(j, tuple):
            #If on matching Level3, input elements are tuples of two tuples - generate list of 4 ints from input.
            if b:
                temp1 = [item for sublist in j for item in sublist]
            #If on matching Level2, input elements are tuples - generate list of 2 ints from tuple.
            else:
                temp1 = list(j)
        for k in inlist:
            #Edge creation code runs for every element EXCEPT for the current element.
            if j == k:
                continue
            else:
                #Same idea as the loop with j.
                if isinstance(k, int):
                    temp2 = [k]
                elif isinstance(k, tuple):
                    if b:
                        temp2 = [item for sublist in k for item in sublist]
                    else:
                        temp2 = list(k)
                #Concatenates temp1 and temp2.
                combo = temp1 + temp2
                #Creates edge between j & k, determines weight by calling the utility function on combo.
                G.add_edge(j, k, weight = utility(combo))

    #After weighted graph is created, calls NetworkX max_weight_matching function, which divides the nodes into pairs such that the total
    #weight of the matched edges is optimal.
    matching = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True)
    return (matching)

def main():
    #Initializes empty list and three NetworkX graphs
    persons = []
    G = nx.Graph()
    F = nx.Graph()
    H = nx.Graph()
    b = False

    #Generates list of ID numbers all persons that have filled out the form
    responses = db.execute("SELECT * FROM responses WHERE id > 0")
    for response in responses:
        persons.append(response["id"])

    #Level 1 - matches all individuals into optimal PAIRS
    Level1 = match(persons,G, b)
    print(Level1)
    #Level 2 - matches the pairs to form optimal QUARTETS
    Level2 = match(Level1, F, b)
    #Sets b to true to inform Level3 about the structure of the input list
    b = True
    #Level 3 - matches the quartets to form optimal OCTETS
    Level3 = match(Level2, H, b)

    #Breaks down all matched individuals using list comprehension, generates a list of all individuals that were NOT matched
    matched = [item for sublist1 in Level3 for sublist2 in sublist1 for sublist3 in sublist2 for item in sublist3]
    others = [x for x in persons if x not in matched]
    #Passes list containing two elements - firstly, the octet matching, and a list of up to 7 "other" individuals not matched by algorithm.
    return [Level3, others]

if __name__ == "__main__":
    main()






