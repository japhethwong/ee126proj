Calculating the Ramchandran Number
==================================

Contributors:  Akshay Narayn, Nishanth Mohan, Japheth Wong
EE126 Fall 2014 Mini-Project

Overview
--------
When we thought of professor rankings, the first thought that came to mind was 
the Erdos numbers, a number which shows the collaboration distance from an 
individual to Erdos.  We thought it would be fun to bring this concept closer 
to home, so we wrote some functions to compute a professor's "Ramchandran 
number".

System Requirements
-------------------
-- Python 2.7
-- Beautiful Soup 4

Instructions
------------
Run our function by executing the following commands:
$ python ramchandranNumber.py

This will execute our code by starting at Professor Kannan Ramchandran, 
randomly picking a coauthor to visit, and continuing to visit professors' 
coauthors up to a counter.  At the end, we are able to display the professors 
ranked by their Ramchandran number.