#This file is created to get around the circular import between outSB.py & SButils.py, the problem was -
#outSB.py wants to import the 2 functions form SButils whereas SButils wants to import globals from outSB.py
#This gives the error - ImportError: cannot import name sandbox_log_path

import os
from .__init__ import path

# volume_path = path + "sandbox/volume"
# sandbox_log_path = path + "views/SBlogs"
# sandbox_log_name  = sandbox_log_path + "/sandbox_match_log"
# current_path = path + "views"

#current_path = os.getcwd()		#doesn't work when called from django, it gives the directory of manage.py
current_path = os.path.dirname(os.path.abspath(__file__))
volume_path = current_path + "/../sandbox/volume"
sandbox_log_path = current_path + "/SBlogs"
#cidfile_name = sandbox_log_path + '/cont'+logfile_name		#logfile is passed as argument, this won't work
sandbox_log_name  = sandbox_log_path + "/sandbox_match_log"
