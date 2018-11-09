<h1> The Bot Management Folder </h1>

<h2> BM.py </h2>
  The file BM.py represents the control logic for the Bot Management. Each time a match is requested, the sandbox plays 2 matches, once with the current player as player1 and once otherwise. The code is run with 4 command line arguments:
  
  * Bot1 extension
  * Bot2 extension
  * Log filename suffix
  * Swap (True/False)
  
  An example of the third parameter is: 14v31, which results in a log file named `log14v31` as well as an error file named `error14v31`.
  
<h2> process.py </h2>
  Bot management makes extensive use of Popen objects, signal handling, and piping data to and from processes. This file defines a process class which abstracts away all lower level code, so as to ensure concise logic in the BM.py file.
  
<h2> BMLimits.py </h2>
  Stores user defined time limits, process limits and buffer limits for use in other files.
  
<h2> validate.py </h2>
  This file houses the code necessary to interface between BM.py and the validation.
