#!/usr/bin/python

import commands
import init
import os
import auxi

def shell():
	
	#--meta variable
	remote_dir = []
	remote_git = []
	
	local_dir = 'none'
	local_git = 'none'
	root_dir = os.environ['HOME']+'/gitDFS'
	pit = root_dir
	last = root_dir

	#--initialization
	print "Welcome to gitDFS~~~"
	local_name = raw_input('please type in the name of the local machine, skip this, type \'s \':')
	if local_name!='s':
		(local_dir,local_git) = init.local(local_name)
	else: 
		f = open(os.environ['HOME']+'/os_project/info/local_name','r')
		name = f.read()
		name = str.split(name,'\n')
		name = name[0]
		local_name = name
		print 'local_name is:'+local_name
		local_dir = root_dir+'/'+local_name
		local_git = root_dir+'/'+local_name+'.git'
		print 'local_dir is:'+local_dir+', local_git is:'+local_git
		print '==============================================================================='

	#--cmd execution
	cmd = raw_input('gitDFS >>')
	while(cmd!='exit()'):
		if cmd == 'connect':
			(remote_dir,remote_git) = init.connect()
		elif cmd == 'ls -r':
			cur_dir = auxi.getCurrentDir(pit)
			if (pit.find('_remote')!=-1): #-- remote ls
				#print 'remote ls'
				if auxi.check_remote(remote_git,remote_dir):
					git_r = auxi.getRemoteGit(remote_git,remote_dir,pit)
					#(sta,info) = commands.getstatusoutput('git pull '+git_r)
					refresh(cur_dir,git_r)
					os.system('ls '+pit)
				else:
					print 'error occurred in '+cmd
			elif (pit.find('.git')!=-1): #-- git ls
				#print 'git ls'
				os.system('ls '+pit)
			else: #-- local ls
				#print 'local ls'
				if auxi.check_local(local_git,local_dir):
					#(sta,info) = commands.getstatusoutput('git pull '+local_git)
					refresh_local(local_name,local_git)
					os.system('ls '+pit)
				else:
					print 'error occurred in '+cmd
		elif cmd == 'ls':
			os.system('ls '+pit)
		elif cmd.find('cd')!=-1:
			dest = str.split(cmd,' ')
			dest = dest[-1]
			(sta,next) = commands.getstatusoutput('ls '+pit)
			if not (dest in next) and (dest != '..'):
				print dest+' does not exisit'
				
			elif not os.path.exists(pit+'/'+dest):
				print dest+' is not a directory'
				
			elif dest == '..':
				(pit,last) = auxi.cd_back(dest,pit,last)
			else:
				(pit,last) = auxi.cd_forward(dest,pit,last)
		elif cmd == 'pwd':
			print pit

		elif cmd.count('read -r')==1:
			objFile = str.split(cmd,' ')
			objFile = objFile[-1]
			objFile_whole = pit+'/'+objFile
			if not os.path.isfile(objFile_whole):
				print 'file '+objFile+' does not exist'
				
			else:
				cur_dir = auxi.getCurrentDir(pit)
				if pit.find('_remote')!=-1: #-- remote read
					print 'remote read'
					git_r = auxi.getRemoteGit(remote_git,remote_dir,pit)
					#exe_fetch = 'git --git-dir=../gitDFS/'+cur_dir+'/.git fetch'
					#print 'fetch:'+exe_fetch
					#(sta,info) = commands.getstatusoutput(exe_fetch)
					#print info
					#exe_merge = 'git --git-dir=../gitDFS/'+cur_dir+'/.git --work-tree=../gitDFS/'+cur_dir+' merge origin/master'
					#print 'merge:'+exe_merge
					#(sta1,info1) = commands.getstatusoutput(exe_merge)
					#print info1
					refresh(cur_dir,git_r)
					os.system('chmod a+r '+objFile_whole)
					os.system('vim '+objFile_whole)
				elif pit.find('.git')!=-1:  #-- git read
					os.system('chmod a+r '+ objFile_whole)
					os.system('vim '+objFile_whole)
				else: #-- local read
					#(sta,info) = commands.getstatusoutput('git pull '+local_git)
					refresh_local(local_name,local_git)
					os.system('chmod a+r '+ objFile_whole)
					os.system('vim '+objFile_whole)

		elif cmd.count('read')==1 and cmd.count('read -r')==0:
			objFile = str.split(cmd,' ')
			objFile = objFile[-1]
			objFile_whole = pit+'/'+objFile
			os.system('chmod a+r '+objFile_whole)
			os.system('vim '+objFile_whole)

			
		elif cmd.find('write')!=-1:
			objFile = str.split(cmd,' ')
			objFile = objFile[-1]
			objFile_whole = pit+'/'+objFile
			existed = 'T'
			newFile = 'OFF'
			if not os.path.isfile(objFile_whole):
				existed = 'F'
				print 'file '+objFile+' does not exist,do you want to create a new one? (y/n)'
				choose = raw_input()
				if choose == 'y':
					newFile = 'ON'
				elif choose == 'n':
					newFile = 'OFF'
				else:
					print 'neither y nor n, invalid input.'

			if existed == 'F' and newFile == 'OFF':
				print 'no file is created.'
			else:
				cur_dir = auxi.getCurrentDir(pit)
				if pit.find('_remote')!=-1:  #-- remote write
					print 'remote write'
					if cmd.count('write -r')==1:
						if existed == 'T':
							refresh(cur_dir)
						else:
							print 'the file '+objFile+' does not exist, you can\'t use command:'+cmd
							return

					os.system('chmod a+w+r '+objFile_whole)
					auxi.write(objFile_whole)
					msg = raw_input('please type in the modify message:')
					git_r = auxi.getRemoteGit(remote_git,remote_dir,pit)
					update(msg,cur_dir,objFile,git_r)
				elif pit.find('.git')!=-1:  #-- git write, forbidden
					print 'you cannot modiy .git directory'
				else:  #-- local write
					print 'local write'
					if cmd.count('write -r')==1:
						if existed == 'T':
							refresh_local(local_name,local_git)
						else:
							print 'the file '+objFile+' does not exist, you can\'t use command:'+cmd
							return

					os.system('chmod a+w+r '+objFile_whole)
					os.system('vim '+objFile_whole)
					msg = raw_input('please type in the modify message:')
					update_local(msg,local_name,objFile,local_git)
			
		cmd = raw_input('gitDFS >> ')
	print "exit the gitDFS shell"

def refresh(cur_dir,git_r):
	exe_fetch = 'git --git-dir=../gitDFS/'+cur_dir+'/.git fetch'
	print 'fetch:'+exe_fetch
	(sta,info) = commands.getstatusoutput(exe_fetch)
	print info
	exe_merge = 'git --git-dir=../gitDFS/'+cur_dir+'/.git --work-tree=../gitDFS/'+cur_dir+' merge origin/master'
	print 'merge:'+exe_merge
	(sta1,info1) = commands.getstatusoutput(exe_merge)
	print info1

def refresh_local(local_name,local_git):
	exe_fetch = 'git --git-dir=../gitDFS/'+local_name+'/.git fetch '+local_git
	print 'local fetch:'+exe_fetch
	(sta,info) = commands.getstatusoutput(exe_fetch)
	print info
	exe_merge = 'git --git-dir=../gitDFS/'+local_name+'/.git --work-tree=../gitDFS/'+local_name+' merge FETCH_HEAD'
	print 'local merge:'+exe_merge
	(sta1,info1) = commands.getstatusoutput(exe_merge)
	print info1

def update(msg,cur_dir,objFile,git_r):
	exe_add = 'git --git-dir=../gitDFS/'+cur_dir+'/.git --work-tree=../gitDFS/'+cur_dir+' add '+objFile
	print 'update exe_add:'+exe_add
	(sta,info) = commands.getstatusoutput(exe_add)
	print info
	exe_commit = 'git --git-dir=../gitDFS/'+cur_dir+'/.git --work-tree=../gitDFS/'+cur_dir+' commit -a -m '+'\''+msg+'\''
	print 'update exe_commit:'+exe_commit
	(sta1,info1) = commands.getstatusoutput(exe_commit)
	print info1
	exe_push = 'git --git-dir=../gitDFS/'+cur_dir+'/.git --work-tree=../gitDFS/'+cur_dir+' push '+git_r
	print 'update exe_push:'+exe_push
	(sta2,info2) = commands.getstatusoutput(exe_push)
	print info2

def update_local(msg,local_name,objFile,local_git):
	exe_add = 'git --git-dir=../gitDFS/'+local_name+'/.git --work-tree=../gitDFS/'+local_name+' add '+objFile
	print 'local update exe_add:'+exe_add
	(sta,info) = commands.getstatusoutput(exe_add)
	exe_commit = 'git --git-dir=../gitDFS/'+local_name+'/.git --work-tree=../gitDFS/'+local_name+' commit -a -m '+'\''+msg+'\''
	print 'local update exe_commit:'+exe_commit
	(sta1,info1) = commands.getstatusoutput(exe_commit)
	print info1
	exe_push = 'git --git-dir=../gitDFS/'+local_name+'/.git --work-tree=../gitDFS/'+local_name+' push '+local_git+' HEAD'
	print 'local update exe_push:'+exe_push
	(sta2,info2) = commands.getstatusoutput(exe_push)
	print info2

if __name__ == '__main__':
	shell()
