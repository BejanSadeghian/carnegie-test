## Written by Bejan Lee Sadeghian
## Date: June 3nd, 2018

import time
import sys, os
import pandas as pd
from utils.request import requestURL

# # Test Parameters provide an array and a file size expectation
# ManualTests = {
# 	'001': {'params':	['http://f586e1a7.bwtest-aws.pravala.com/384MB.jar', #source
# 						'./data/test001.jar', #target
# 						'False', #asyn boolean
# 						'', #chunks
# 						''], #chunksize
# 			'sizeExp': #expected size
# 			},

# }

# Test Parameters 
source = 'http://f586e1a7.bwtest-aws.pravala.com/384MB.jar'
target = './data/testResult.jar'
chunk = [1,4,40]
chunksize = [2**2,2**20,(2**24)] # 4Bytes, 1MiB, 16MiB
async = ['False','True']

# Execute Test and Save results
results = pd.DataFrame()
savePath = './testResults.xlsx'
try:
	for a in async:
		for ch in chunk:
			for cs in chunksize:
				requestURL(source, target, a, ch, cs)
				expected = ch*cs
				actual = os.stat(target).st_size # Get the size of the file or maybe the size of the in memory object ... os.stat(filename).st_size
				if  actual == expected:
					print('Success',a,ch,cs)
					lineItem = {'Status':['Success'],'Source':[source],'Target':[target],'Async':[a],
								'Chunks':[ch],'Chunksize':[cs],'ActualSize':[actual],'ExpectedSize':[expected]}
				else:
					lineItem = {'Status':['Failure'],'Source':[source],'Target':[target],'Async':[a],
								'Chunks':[ch],'Chunksize':[cs],'ActualSize':[actual],'ExpectedSize':[expected]}
					print('Failure',a,ch,cs)
				newLine = pd.DataFrame(lineItem)
				results = pd.concat([results,newLine],axis=0)
				print(results)
				time.sleep(2) # Prevent our test from overloading the server

	results.to_excel(savePath, index=False)
except:
	results.to_excel(savePath, index=False)
