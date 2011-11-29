import commands
import os


def getCurrentPath(pit):
	return pit
	
def getCurrentDir(pit):
	path = getCurrentPath(pit)
	path_temp = str.split(path,'/')
	return path_temp[-1]

def check_remote(remote_git,remote_dir):
	if len(remote_git)==0 or len(remote_dir)==0:
		print "connection has not been completed or error occurred in connection"
		return 0
	else:
		return 1

def check_local(local_git,local_dir):
	if len(local_git)==0 or len(local_dir)==0:
		print "initialization has not been completed or error occurred in initialization"
		return 0
	else:
		return 1


def getRemoteGit(remote_git,remote_dir,pit):
	pos = remote_dir.index(pit)
	return remote_git[pos]
	
def cd_forward(dest,pit,last):
	last = pit
	pit = pit+'/'+dest
	return (pit,last)

def cd_back(dest,pit,last):
	cur_dir = getCurrentDir(pit)
	pit = last
	pos = last.find(cur_dir)
	last = last[0:pos-1]
	return(pit,last)

def write(objFile_whole):
	os.system('vim '+objFile_whole)

