# User's Manual

## Project Title:

BLOCKED (STRESS FREE HOUSING SOLUTIONS: A CS50 2018 PROJECT)

## Project Summary:

BLOCKED is a web application and algorithm that outputs optimal blocking group arrangements based on user input and rating of their
preferred blockmates.

## Structure:

Just like C$50 Finance, BLOCKED is built using Python, Flask, and Jinja. To get it up and running, simply navigate to the highest level
of the directory in the terminal and use "flask run."

## Usage:
The index or base page of the website includes a welcome message and a "Submit Your Preferences" button at the bottom. Hit that button,
which will take you to the form. The form has eight select menus, one for your name and one each for up to seven preferred blockmates.
The options in that select menu were taken from the Harvard RoomBook software and, to the best of my knowledge, include every Harvard
first-year student. However, if you are testing and are not a first-year, your name may not be an option. In this event, please select
a random first-year name and up to seven random first-year blockmates to test the form.

You have 100 rating points to allocate between up to seven blockmates. The number of rating points you allocate to a blockmate will be
their weighting in the algorithm, so obviously the more points you allocate to an individual, the higher the likelihood you will be
blocked together by the algorithm. You do not NEED to choose the full seven blockmates, but JavaScript mandates that you fill in
at least one of the seven, as well as your own username. If you do not put in at least one blockmate and your own name, the
form submission will be prevented with an alert box. As you rate your blockmates, a counter, enabled by JavaScript, will appear
on the right side of the screen to inform you of how many rating points you have left. If the counter is below zero when you click submit,
JavaScript again will prevent submission of the form with an alert box.

Provided none of these cases occur, you can then click submit at your leisure. You will be redirected to a page thanking you for
your submission, which has a brief summary and then a red button saying "Continue to Results." After you hit that button,
you will be redirected to the results page. Every time the results page is loaded, application.py assumes that there is a new form entry
and re-runs the matching algorithm, so it may take a few seconds to load. The results page displays the current arrangement of blocking
groups in a table.

## Important Notes:
- The algorithm intentionally only matches people who have completed the form. Therefore, if you input and rate seven blockmates, but
none of them have completed the form, you will be the only one showing up in results.html.

- You cannot edit your form responses. This is not only because I do not know how to let someone edit their form responses, but also
because the app allows you to view the groups after you submit - users might play the system if they were able to repeatedly use trial
and error.

- The IDs of the users are NOT their HUIDs. They are an arbitrary set of IDs used by the Cabot Library RoomBook system. For lack of
a better system, I decided to use this set. Blocking.db, table "users," matches every user with their ID - I reference this table
when generating results.html to output real names instead of ID numbers.

- It is possible that you will be matched with people whom you did not rank and who did not rank you. This will be elaborated upon in
DESIGN.md.

- On every page there is a navbar with three elements: FORM, the Harvard logo, and RESULTS. Clicking FORM will take you to the form,
RESULTS to the results page, and the Harvard logo will redirect you to the welcome page, index.html.

- All form responses are stored in blocking.db, table "responses." Note that the ID of the user is stored in the final column.