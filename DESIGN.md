# Design Document

## Project Title:

BLOCKED (STRESS FREE HOUSING SOLUTIONS: A CS50 2018 PROJECT)

## Project Summary:

BLOCKED is a web application and algorithm that outputs optimal blocking group arrangements based on user input and rating of their
preferred blockmates.

## Algorithm
I will start by discussing my algorithm, since that was the biggest challenge presented to me in this project. In total, I would say I spent
approximately 18 hours working on the algorithm, but at least 12 of those were on entirely the wrong track. Initially, I attempted to use
itertools.combinations to generate ALL possible arrangements of all the users that had submitted the form. Then, I would iterate through
those arrangements and calculate the total utility, thus guaranteeing that I would find the absolute optimal output. However, I soon ran
into several issues. Firstly, I wanted to make my algorithm work for any unknown number of inputs, whether that was 8, 13, 20, or so on.
Therefore, I used recursion instead of hard-coding a set number of for loops. This meant that I couldn't keep track of what group number
I was on, and led to problems with iterating through all the combinations.

The morning after the hackathon, I decided to throw out the old algorithm because it would be ridiculously slow anyway - generating all
combinations is O(n!). My new algorithm is O(n^3), which is not ideal but still significantly faster. The way the algorithm works is
through graph matching. First, I generate a graph, using the NetworkX package, with nodes representing all the users who have completed
the form. I then connect each node to every other node with an edge. The edge weight is equal to the sum of the rating points that the
users allocated to each other - if neither user ranked each other on their form, the weight would then be zero. I then use the NetworkX
max_weight_matching function to generate an optimal matching of the graph. That means, it divides the graph into pairs of nodes such that
the sum of the weights of the edges between the connected pairs is optimized.

*Note - I set maxcardinality = True on this function, meaning that all nodes must be matched even if the edge weight is zero. For this
reason it is possible to be matched with people that you did not rate and who did not rate you. This was a conscious design choice
as I thought it would be more preferable to meet new friends than go in the lottery alone.

Now, I have a list of optimal pairs. I repeat the exact same process, except that now every node in the graph represents a pair of people.
The edges between nodes thus connect a total of four people - as you will see in algorithm.py, I had to do some fiddling so that I could
generate that list of four people and apply the utility function. The utility function sums the rating points given by every person in the
potential group of four to EVERY OTHER person. The matching of this graph returns a list of optimal quartets.

Finally, I run the matching process for a third time, with every node representing a group of four. Algorithm.py calculates the utility
for every possible merging of groups of four - which represents a blocking group of 8 - and weights the edges accordingly. Note again that
the utility for an edge is derived by taking all eight people in the connected nodes and summing each person's rating for every other person.
Matching this graph, ultimately, outputs the list of optimal blocking groups of 8.

My algorithm has several faults, but also several benefits. Firstly, the fact that it runs in O(n^3) makes it a lot faster than my
previous algorithm. Furthermore, the method of generating pairs, quartets, then octets makes it applicable no matter how many users
(within realistic bounds) complete the form. One fault, however, is that the algorithm is greedy. That is, the pair-generating step
only cares about generating the best pairs, and the quartet-generating step only cares about generating the best quartet. It is
fully feasible that the best quartet might not be formed by merging two of the optimal pairs; similarly, the best octet might
not be formed by merging two of the optimal quartets. The algorithm disregards these cases and therefore probably does not output
the absolute best arrangement. Nevertheless, I thought the convenience, speed, and flexibility outweighed this flaw.

## Website & Database
- Aesthetics & CSS
I'm quite proud of how my website looks aesthetically, particularly the background image and centered navbar. I drew inspiration from
the HSA website, but I actually did the background image and title by myself, without using a template. I thought that designing the UI was
definitely one of the most enjoyable aspects of this project, though not the most challenging. In particular, I'm proud of the
linear-gradient CSS tool that allowed me to darken the top of my Harvard Yard image enough for the navbar to be visible.

-JavaScript
One of the key aspects of my proposal was to incorporate extensive use of JavaScript into my page. I don't think I was able to do as much
with JavaScript as I had intended to. However, I was able to prevent submission if there was no username, if there was not at least
one blockmate, and if more than 100 rating points were used. The JavaScript function that I spent the most time on was the appearance
of the Points Remaining counter which displays the user's remaining points as they enter ratings for each of their blockmates. I did
this by using the JQuery val() function, which returns the value in a text area. Every time there is an input into one of the seven
text areas, the JQuery recalculates the sum of the inputted points and subtracts from 100. I understand that it is very bad design
to copy and paste the same code for all seven text areas, as I did in form.html. I endeavored for several hours to do this using a
for loop (let i = 1; i < 8; i ++). However, I repeatedly encountered an error: Uncaught TypeError: Cannot set property 'onkeyup' of null.
I posted on Discourse and Prof. Malan said the code looked like it was fine, so after a while I just gave up and resorted to copy-paste.
Sorry about that.

-SQL & application.py
SQL plays an important role in my application.py. In particular, the "users" table of the database stores all the names of first-years
as well as their corresponding ID numbers. Therefore, in the /results route, I access that table to translate the groups of ID numbers
output by the algorithm main() function into names. Application.py is fairly straightforward. The only interesting part is the /results
route, which strips the list of ID numbers from the slightly convoluted data returned from the algorithm. The specifics can be found
in the comments of application.py.

-Macros
The rendered HTML of my form.html has over 33,000 lines, since there are eight select menus of over 4,000 lines each. Obviously it was
terrible design to copy-paste these eight times, so I made use of Jinja macros. In macros.html, I defined a block called selectmenu()
which encompassed all 4,000+ <option>s of the select menu. Then, every time I needed it, I imported the block from macros and called it.