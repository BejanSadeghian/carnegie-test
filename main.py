## Written by Bejan Lee Sadeghian
## Date: June 3rd, 2018

import sys
from utils.request import requestURL

# Execute the request
if __name__ == '__main__':
	requestURL(*sys.argv[1:]) # Ignoring the first parameter which is the filename
