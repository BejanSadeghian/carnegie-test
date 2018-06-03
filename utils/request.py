## Written by Bejan Lee Sadeghian
## Date: June 3rd, 2018

import requests

from gevent.pool import Pool
from gevent import monkey

def requestURL(source, target=r'.\data\default.jar', async='False', chunks=4, chunksize=2**20):
	"""
	Method to read in from the HTTP source and write to the local target on disk.

	Parameters:
		:source: {str} the HTTP URL to read from
		:target: {str} the local path to save to (default is ./data/default.jar)
		:async: {bool} to determine if we should download asynchronously (default is False)
		:chunks: {int} the number of chunks to read in (default is 4)
		:chunksize: {int} the number of MiB to read in per chunk (default is 1 MiB)
	Returns:
		None
	"""

	def _GETRequest(dataTuple):
		"""
		Local Method Only, This performs a GET request using a specified range header
		
		Parameters:
			:dataTuple: {tuple} index 0 contains the source URL; index 1 contains the byte range to download
		Returns:
			:output: {str} content of the returned request
			:byteRng: {str} byte range that was requested (for debugging purposes)
		"""
		source = dataTuple[0]
		byteRng = dataTuple[1]
		r = requests.get(source, headers={'range':byteRng})
		try:
			output = r.content
		finally:
			r.close()
		return (output, byteRng)

	# Validate input types first, if there is an issue then cancel the operation
	continueBool = True
	monkey.patch_socket() # Monkey patches the socket module to avoid serialization

	try:
		source = str(source)
		target = str(target)
		chunks = int(chunks) #Implicit Round Down
		chunksize = int(chunksize) #Implicit Round Down

		if async.lower() == 'true':
			async = True
		elif async.lower() == 'false':
			async = False
		else:
			raise TypeError('The Async Parameter is not a boolean')
	except Exception as e:
		print(e)
		continueBool = False
	# If no exception then begin reading in data and saving to disk 
	if continueBool:
		# Create the list of byte ranges
		byteRanges = [(source, 'bytes='+str(x*chunksize)+'-'+str(((x+1)*chunksize)-1)) for x in range(chunks)]
		try:
			if async:
				#First pool the GET requests and execute all at once
				print('Performing an asynchronous download')
				pool = Pool(chunks)
				response = pool.imap(_GETRequest,byteRanges)
				pool.join() 

				# Then wtite the results to the file
				handler = open(target, 'wb')
				for data in response:
					print('Saving',data[1])
					handler.write(data[0])
				handler.close()
			else:
				# If performing serially then write the results to the file as we GET from the source 
				print('Performing serial download')
				handler = open(target, 'wb')
				for i, chunk in enumerate(byteRanges):
					print('Getting Chunk',i,chunk[1])
					handler.write(_GETRequest(chunk)[0])
				handler.close()
		except Exception as e:
			print(e)
			if handler is not None: 
				handler.close() # Ensure that we close any interrupted connection to the file
	return None
