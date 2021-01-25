from __future__ import division

import subprocess
import os
import shutil
import logging
import sys

logging.basicConfig( filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG )

"""
checks if v is int
"""
def isInt( v ):
	try:     i = int( v )
	except:  return False
	return True

def isOctal( v ):
	if( int( v[0] ) >= 0 and int( v[0] ) <= 7 and
	    int( v[1] ) >= 0 and int( v[1] ) <= 7 and
	    int( v[1] ) >= 0 and int( v[1] ) <= 7 ):
		return True
	return False

class InvalidFileSize( Exception ):
	def __init__( self ,filesize , message = "file size invalid "):
		self.filesize = filesize
		self.message = message
		super().__init__( self.message )

class InvalidBlockSize( Exception ):
	def __init__( self ,blocksize , message = "block size invalid "):
		self.blocksize = blocksize
		self.message = message
		super().__init__( self.message )

class NoFreeSpace( Exception ):
	def __init__( self , freespace , message = "disk space low" ):
		self.freespace = freespace
		self.message = message
		super().__init__( self.message )

class InvalidPermission( Exception ):
	def __init__( self , permission , message = "invalid permission" ):
		self.permission = permission
		self.message = message
		super().__init__( self.message )

"""

Validates inputs and returns input
input is a tuple of (size ,blocksize, permission)
checks if size is int
checks if free space is available to create file(space < 10kb )
checks if blocksize is int

"""

def Userinput():

	size = input("enter size: ")
	if ( not isInt( size ) ):
		logging.error( "Invalid File size" )
		raise InvalidFileSize( size )	
	
	if ( int ( size ) < 0 ):
		logging.info( "Invalid File size < 0" )
		raise InvalidFileSize( size )

	cwd=os.getcwd()
	stat = shutil.disk_usage( cwd ) 
	#a lower limit on free space I have put as 10kb
	if ( stat[2] < 10000 ):
		logging.error( "No Free Space" )
		raise NoFreeSpace( stat[2] )

	logging.debug( "File Size is Valid" )

	block_size = input( "enter blocksize: " )
	if ( not isInt( block_size) ):
		logging.error( "Invalid BlockSize" )
		raise InvalidBlockSize( block_size )
	
	if( int( block_size ) <= 0 ):
		logging.error( "Invalid BlockSize" )
		raise InvalidBlockSize( block_size )


 	#if( block_size > size):
	#	logging.error( "bs cannot be more than file size" )


	logging.debug( "BlockSize is Valid" )

	permission = input( "enter permission: " )

	if( not isInt( permission ) ):
		logging.error( "Invalid permission" )
		raise InvalidPermission( permission )

	if( int(permission) < 0 ):
		logging.error( "Invalid permission" )
		raise InvalidPermission( permission )

	if( not isOctal( permission ) ):
		logging.error( "Invalid permission" )
		raise InvalidPermission( permission )
	
	logging.info( "Valid Inputs" )

	return ( int( size ), int( block_size ), permission )


"""
returns ceil of n
"""
def ceil( n ):

	res = int( n )
	return res if res == n or n < 0 else res + 1

"""
input is a tuple with size,blocksize,permissions
creates a file with given data

"""

def createFile( input ):

	size = input[0]
	block_size = "bs=" + str(input[1])
	permissions = input[2]

	count = "count=" + str(ceil(size / input[1]))
	inputfile = "if=/dev/random"

	outputfile_name = "filesize_" + str( size ) + "_blocksize_" + str( input[1] )
	outputfile = "of=" + outputfile_name


	"""
	name of the output file written is outputfile_name for eg filesize_8192_blocksize_4096
	"""



	returnValue_dd = subprocess.run(['dd' , inputfile , outputfile,block_size ,count ] ,stderr=subprocess.PIPE )
	if( returnValue_dd.returncode != 0 ):
		logging.error("File Not Created")
		sys.exit( "File could not be created" )
			
	logging.info( "File Created" )

	returnValue_chmod = subprocess.run( ['chmod' , str(permissions) ,  outputfile_name  ] , stderr=subprocess.PIPE )
	if( returnValue_chmod.returncode != 0 ):
		logging.error( "permissions not set" )
		logging.error( "deleting file" )
		os.remove( outputfile_name )
		sys.exit( "permission could not be set" )
	
	logging.info( "Permissions set" )
	logging.info( "Done" )
	print( "file created" )








def main():

	input = Userinput()
	createFile( input )


main()
