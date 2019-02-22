import random, time, traceback

# Create your script here:
def likeFriends(InstaPy, username, password, proxy=None):
    try:
        session = InstaPy(username=username, password=password)
        session.login()

        mutualFollowing = session.pick_mutual_following(username=username, live_match=False, store_locally=True)

        # activity
        session.set_do_like(True, percentage=100)
        session.interact_by_users(mutualFollowing, amount=2, randomize=False)

        session.end()
    except:
        print(traceback.format_exc())

# !! Not delete the following code.
class Scripts:
    def __init__(self):
        functions = [f for fname, f in sorted(globals().items()) if callable(f)]
        self.scripts = {}
        for function in functions:
            name = str(function.__name__).lower()
            if name != "scripts":
                self.scripts[name] = function
