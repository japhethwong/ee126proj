import random
from collections import deque
from scrape import getCoAuthorsForAuthor, RAMCHANDRAN_NAME, RAMCHANDRAN_ID
import sys

PADDING = " " * 4
ramchandran_numbers = {(RAMCHANDRAN_ID, RAMCHANDRAN_NAME) : 0}

INTIAL_ALPHA = 5
MAX_INITIAL_DEPTH = 4

ALPHA = 10
MAX_TRIES = 50

random_author = RAMCHANDRAN_NAME

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

	while len(Q) != 0:
		author, depth = Q.popleft()

		if depth > MAX_INITIAL_DEPTH:
			continue 

		# Use reservoir sampling
		random_int = random.randint(0, len(ramchandran_numbers) - 1)
		if random_int == 0:
			random_author = author

		if not author in ramchandran_numbers:
			ramchandran_numbers[author] = depth

		coauthors = get_coauthors(author, INTIAL_ALPHA)
		for coauthor in coauthors:
			Q.append((coauthor, depth + 1))


# Populates the initial databae of Ramchandran numbers
def _populate_initial_database_():
	Q = deque()
	Q.append(((RAMCHANDRAN_ID, RAMCHANDRAN_NAME), 0))
	_bfs_(Q)

# Populates the database given a random author trying 
# MAX_TRIES tries
def _populate_randomly_(author):
	initial_number = ramchandran_numbers[author] + 1
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
	longest_author = len(max(entries, key=lambda(elem): len(elem[0][1]))[0][1])

	print("\nAUTHOR" + PADDING + " " * max(0, longest_author - 6) + "RAMCHANDRAN NUMBER")
	print("")
	for entry in entries:
		author = unicode(entry[0][1]).title()
		spaces = " " * max(longest_author - len(author), 0)
		number = str(entry[1])
		print(author + spaces + PADDING + number)
	print("")

if __name__ == "__main__":
	print("== Computing Ramchandran numbers ==")
	try:
		if (len(sys.argv) >= 2):
			INITIAL_ALPHA = int(sys.argv[1])
		if (len(sys.argv) >= 3):
			MAX_INITIAL_DEPTH = int(sys.argv[2])
		if (len(sys.argv) >= 4):
			ALPHA = int(sys.argv[3])
		if (len(sys.argv) >= 5):
			MAX_TRIES = int(sys.argv[4])

	except ValueError as err:
		print err

	print("Using Parameters:\n\tINITIAL_ALPHA: %d\n\tMAX_INITIAL_DEPTH: %d\n\tALPHA: %d\n\tMAX_TRIES: %d" % (INITIAL_ALPHA, MAX_INITIAL_DEPTH, ALPHA, MAX_TRIES))
	run()