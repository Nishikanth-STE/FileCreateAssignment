from __future__ import division

import subprocess
import os
import shutil
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

"""
checks if v is int
"""
def isInt(v):
	try:     i = int(v)
	except:  return False
	return True

"""
Validates inputs and returns input
input is a tuple of (size ,blocksize, permission)
checks if size is int
checks if free space to create file is present
checks if blocksize is int
"""

def Userinput():

	size = input("enter size: ")
	if(not isInt(size)):
		logging.error( "Invalid File size" )
		

	cwd=os.getcwd()
	stat = shutil.disk_usage( cwd ) 
	if ( stat[2] < 10000 ):
		logging.error( "No Free Space" )

	logging.debug( "File Size is Valid" )

	block_size = input( "enter blocksize: " )
	if( not isInt( block_size) ):
		logging.error( "Invalid BlockSize" )

 	#if( block_size > size):
	#	logging.error( "bs cannot be more than file size" )


	logging.debug( "BlockSize is Valid" )

	permission = input( "enter permission: " )

	if(not isInt(permission)):
		logging.error("Invalid permission")

	
	logging.info( "Valid Inputs" )

	return ( int(size), int(block_size), permission )


"""
returns ceil of n
"""
def ceil( n ):

	res = int(n)
	return res if res == n or n < 0 else res + 1

"""
input is a parameter with size,blocksize,permissions
creates a file with given data

"""

def createFile(input):

	size = input[0]
	block_size = "bs=" + str(input[1])
	permissions = input[2]

	count = "count=" + str(ceil(size / input[1]))
	inputfile = "if=/dev/random"

	outputfile_name = "filesize_" + str( size ) + "_blocksize_" + str( input[1] )
	outputfile = "of=" + outputfile_name



	returnValue_dd = subprocess.run(['dd' , inputfile , outputfile,block_size ,count ],stderr=subprocess.STDOUT)
	if(returnValue_dd.returncode != 0 ):
		logging.error("File Not Created")
	
	logging.info("	File Created")

	returnValue_chmod=subprocess.run(['chmod' , str(permissions) ,  outputfile_name  ])
	if(returnValue_chmod.returncode != 0 ):
		logging.error("permissions not set")
	
	logging.info("Permissions set")
	logging.info("Done")








def main():

	input = Userinput()
	createFile( input )


main()
