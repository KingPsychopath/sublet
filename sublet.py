'''
	Sublet: Reddit movers
	Jathu Satkunarajah (@jathu), August 2015 - Toronto
'''
import praw
import getpass

# -----------------------------------------------------------------------------

def kill_all(RedditInstance):
	print "\n\n Deleting Comments & Submissions for %s \n\n" % str(RedditInstance.user)
	for item in RedditInstance.user.get_overview(sort="new", time="all", limit=None):
		try:
			item.delete()
			print "Deleting: %s" % item.permalink
		except:
			print "\tERROR -> Deleting: %s" % item.permalink

def kill_ini(RedditInstance, INI_USER):
	RedditInstance.login(INI_USER[0], INI_USER[1], disable_warning=True)
	kill_all(RedditInstance)

# -----------------------------------------------------------------------------

def get_all_saved(RedditInstance):
	saved = []
	for item in RedditInstance.user.get_saved(sort="new", time="all", limit=None):
		saved.append(item)
	return reversed(saved)

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
		subreddits.append(str(sub))
	return subreddits

def unsubscribe_all_subreddits(RedditInstance):
	for sub in RedditInstance.get_my_subreddits(limit=None):
		subName = str(sub)
		try:
			RedditInstance.get_subreddit(subName).unsubscribe()
			print "Unsubscribed: %s" % subName
		except:
			print "\tERROR -> Unsubscribing: %s" % subName

def subscribe_all_subreddits(RedditInstance, subreddits):
	for subName in subreddits:
		try:
			RedditInstance.get_subreddit(subName).subscribe()
			print "Subscribed: %s" % subName
		except:
			print "\tERROR -> Subscribing: %s" % subName

def transfer_subreddits(RedditInstance, INI_USER, NEW_USER):
	print "\n\n Transferring Subreddits \n\n"
	RedditInstance.login(INI_USER[0], INI_USER[1], disable_warning=True)
	subreddits = get_all_subreddits(RedditInstance)

	RedditInstance.login(NEW_USER[0], NEW_USER[1], disable_warning=True)
	unsubscribe_all_subreddits(RedditInstance)
	subscribe_all_subreddits(RedditInstance, subreddits)

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

		YES = set(['yes','y', 'ye', '', 't', 'true'])
		NO = set(['no','n', 'f', 'false'])
		print "\nDo you want to delete all the posts for the old user (y/n)?"
		ynAnswer = raw_input().lower()

		# Call methods

		transfer_subreddits(R, INI_USER, NEW_USER)
		transfer_saves(R, INI_USER, NEW_USER)
		if ynAnswer in YES:
			kill_ini(R, INI_USER)
