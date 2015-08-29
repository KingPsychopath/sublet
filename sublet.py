'''
	Sublet: Reddit movers
	Jathu Satkunarajah (@jathu), August 2015 - Toronto
'''
import praw
import getpass

# -----------------------------------------------------------------------------

def get_all_saved(RedditInstance):
	saved = []
	for item in RedditInstance.user.get_saved(sort="new", time="all", limit=None):
		saved.insert(0, item)
	return saved

def save_all_saved(RedditInstance, saved):
	for item in saved:
		try:
			item.save()
			print "Saving: %s" % item.permalink
		except:
			print "\tERROR -> Saving: %s" % item.permalink

def transfer_saves(RedditInstance, INI_USER, NEW_USER):
	print "\n\n Transferring Saves \n\n"
	RedditInstance.login(INI_USER[0], INI_USER[1], disable_warning=True)
	saved = get_all_saved(RedditInstance)

	RedditInstance.login(NEW_USER[0], NEW_USER[1], disable_warning=True)
	save_all_saved(RedditInstance, saved)

# -----------------------------------------------------------------------------

def get_all_subreddits(RedditInstance):
	subreddits = []
	for sub in RedditInstance.get_my_subreddits(limit=None):
		subreddits.append(sub)
	return subreddits

def unsubscribe_all_subreddits(RedditInstance):
	for sub in RedditInstance.get_my_subreddits(limit=None):
		try:
			sub.unsubscribe()
			print "Unsubscribed: %s" % str(sub)
		except:
			print "\tERROR -> Unsubscribing: %s" % str(sub)

def subscribe_all_subreddits(subreddits):
	for sub in subreddits:
		try:
			sub.subscribe()
			print "Subscribed: %s" % str(sub)
		except:
			print "\tERROR -> Subscribing: %s" % str(sub)

def transfer_subreddits(RedditInstance, INI_USER, NEW_USER):
	print "\n\n Transferring Subreddits \n\n"
	RedditInstance.login(INI_USER[0], INI_USER[1], disable_warning=True)
	subreddits = get_all_subreddits(RedditInstance)

	RedditInstance.login(NEW_USER[0], NEW_USER[1], disable_warning=True)
	unsubscribe_all_subreddits(RedditInstance)
	subscribe_all_subreddits(subreddits)

# -----------------------------------------------------------------------------

if __name__ == "__main__":
		R = praw.Reddit('PRAW')
		
		print "\nSublet: Reddit movers"

		INI_USER = ["", ""]
		print "\nOld username: "
		INI_USER[0] = raw_input()
		INI_USER[1] = getpass.getpass()

		NEW_USER = ["", ""]
		print "\nNew username: "
		NEW_USER[0] = raw_input()
		NEW_USER[1] = getpass.getpass()

		# Call methods

		transfer_subreddits(R, INI_USER, NEW_USER)
		transfer_saves(R, INI_USER, NEW_USER)

