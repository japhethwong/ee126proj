import random
from collections import deque
from scrape import getCoAuthorsForAuthor

KANNAN_RAMCHANDRAN = "Kannan Ramchandran"
ramchandran_numbers = {KANNAN_RAMCHANDRAN : 0}

INTIAL_ALPHA = 5
MAX_INITIAL_DEPTH = 4

ALPHA = 5
MAX_TRIES = 10

random_author = KANNAN_RAMCHANDRAN

def get_random_article(author):
	pass

def get_random_author(article):
	pass

def get_coauthors(name, n):
	return getCoAuthorsForAuthor(name, n)

def is_stanfurd_professor(name):
	pass

# Return a random co-author
def get_random_coauthor(coauthors):
	if len(coauthors) == 0:
		return None
	else:
		return random.choice(coauthors)

# Runs a BFS to populate an initial database of 
# Ramchandran numbers 
def _bfs_(Q):
	global random_author
	author, depth = Q.popleft()

	if depth > MAX_INITIAL_DEPTH:
		return 

	# Use reservoir sampling
	random_int = random.randint(0, len(ramchandran_numbers) - 1)
	if random_int == 0:
		random_author = author

	if author in ramchandran_numbers:
		return 
	else:
		ramchandran_numbers[author] = depth

	coauthors = get_coauthors(author, INITIAL_ALPHA)
	for coauthor in coauthors:
		Q.append((coauthor, depth + 1))

	_bfs_(Q)

# Populates the initial databae of Ramchandran numbers
def _populate_initial_database_():
	Q = deque()
	Q.append((KANNAN_RAMCHANDRAN, 0))
	_bfs_(Q)

# Populates the database given a random author trying 
# MAX_TRIES tries
def _populate_randomly_(author):
	initial_number = ramchandran_numbers[author]
	max_number = ramchandran_numbers[author] + MAX_TRIES

	for rmchndrn_number in range(initial_number, max_number):
		coauthors = get_coauthors(author, ALPHA)
		coauthor = get_random_coauthor(coauthors)

		if coauthor is not None:
			if coauthor in ramchandran_numbers:
				prev_number = ramchandran_numbers[coauthor]
				if prev_number > rmchndrn_number:
					ramchandran_numbers[coauthor] = rmchndrn_number
			else:
				ramchandran_numbers[coauthor] = rmchndrn_number

		author = coauthor

def run():
	_populate_initial_database_()
	_populate_randomly_(random_author)

	entries = ramchandran_numbers.items()
	entries.sort(key=lambda(elem): elem[1])
	for entry in entries:
		print unicode(entry[0][1]).title() + ": " + str(entry[1])

if __name__ == "__main__":
	run()