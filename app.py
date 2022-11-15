import sys

from expnav.app import ExpNav

from rich import print


folder = str(sys.argv[-1].split(' ')[-1])
app = ExpNav(folder)
