###FIX FOR _tkinter.TclError: no display name and no $DISPLAY environment variable###
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from dbconnect import connection
import gc

def scoreboardMake():
	c, conn = connection()
	c.execute("SELECT points,teamname FROM teams WHERE hash_status = 0")
	conn.commit()
	Points, Teams = zip(*sorted(c.fetchall()))
	c.close()
	conn.close()
	gc.collect()

	teamsArranged = np.arange(len(Teams))

	plt.barh(teamsArranged, Points, align='center', alpha=0.5)

	plt.yticks(teamsArranged, Teams)
	plt.xlabel('Score')
	plt.title('')

	plt.savefig("/var/www/FlaskApp/FlaskApp/static/images/currentScoreboard.png", bbox_inches="tight")
	
	return None