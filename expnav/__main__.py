import sys

from expnav.app import ExpNav

folder = str(sys.argv[-1].split(' ')[-1])
app = ExpNav(folder)
app.run()

