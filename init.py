import commands
import os


def local(local_name):
	print "--------------------------initializing...-------------------------------"
	path = os.environ['HOME']+'/gitDFS'
        commands.getstatusoutput('mkdir '+path)  #--the root directory
	local_dir = path+'/'+local_name
	os.system('mkdir '+local_dir)  #--the local directory
	(sta,info) = commands.getstatusoutput('git init '+local_dir)
	print info
	#-- create an empty default file
	filePath = open(local_dir+'/default.empty','w')
	filePath.close()
	(s,i) = commands.getstatusoutput('git --git-dir=../gitDFS/'+local_name+'/.git --work-tree=../gitDFS/'+local_name+' add default.empty')
	(s1,i1) = commands.getstatusoutput('git --git-dir=../gitDFS/'+local_name+'/.git --work-tree=../gitDFS/'+local_name+' commit -a -m \'d\'')
	local_git = path+'/'+local_name+'.git'
	(sta1,info1) = commands.getstatusoutput('git clone --bare '+local_dir+' '+local_git) #--the local git
	print info1
	#--output local name
	infoPath = os.environ['HOME']+'/os_project/info/local_name'
	f = open(infoPath,'w')
	print >> f,local_name
	f.close()
	print "--------------------------initialization complete-----------------------"
	return (local_dir,local_git)

def connect():
	print '--------------------------init connecting...---------------------------------'
	#--create the remote copy directories
	path = os.environ['HOME']+'/gitDFS'
	#glb_path = '/home/modandan/os_project/source/info/'
	glb_path = os.environ['HOME']+'/os_project/info/'
	f = open(glb_path+'remote_list','r')
	remote_dir = []
	remote_git = []

	choose = -1
	for line in f:
		user_addr = str.split(line,'\t')
		user = user_addr[0]
		addr = user_addr[1]
		l = len(addr)
		addr = addr[0:l-1]
		user_addr[1] = addr
		assert len(user_addr)==2
		#--store the server's name & git-directory
		remote_dir.append(path+'/'+user+'_remote')
		remote_git.append(addr)
		#--clone the remote directories to local copy
		if not os.path.exists(path+'/'+user+'_remote'):
			(sta,info) = commands.getstatusoutput('git clone '+addr+' '+path+'/'+user+'_remote')
			print info
			choose = 1
		else:
			choose = 0		
	f.close()
	#--output information
	if choose == 1:
		print 'init connection has been set up, the connected servers are:'
		for name in remote_git:
			print name
		print '-------------------------init connection complete----------------------'
	elif choose == 0:
		print 'remote direcories already existe, no init connection is needed'
		print '-------------no need for init connection, go to next step---------------'

	#--output to the remote name
	fr = open(glb_path+'global_remote_name','w')
	for name in remote_dir:
		print >> fr, name
	fr.close()
	return (remote_dir,remote_git)

	

	
