# -*- coding: utf-8 -*-
import re
import arff
pre_org_dict = []
pre_per_dict = []
sub_per_dict = []
common_dict = []

# Load dict #
with open('dict_pre_per.txt') as f:
	for line in f:
		pre_per_dict.append(line)
	f.close()
with open('dict_pre_org.txt') as f:
	for line in f:
		pre_org_dict.append(line)
	f.close()
with open('dict_sub_per.txt') as f:
	for line in f:
		sub_per_dict.append(line)
	f.close()
with open('dict_common.txt') as f:
	for line in f:
		common_dict.append(line)
	f.close()
	
# easy pattern #
filename = ['untagged.out']
data = []
for fn in filename:
	with open(fn) as f:
		for line in f:
			data.append(line)
		for i in range(len(data)):
			if(data[i] == 'บริษัท\n' or data[i] =='ธนาคาร\n' or data[i] == 'บรรษัท\n'):
				for j in range(10):
					if(data[i+j] == 'จำกัด\n'):
						count = j-3
						printed = 0
						for k in range(j-1):
							if(k==1):
								if(data[i+k] != ' \n'):
									data[i+k] = re.split('\n',data[i+k])[0]
									count += 1
									if(count==1):
										data[i+k] += '(org)\n'
									elif(printed == 0):
										data[i+k] += '(org_start)\n'
									printed += 1	
							if(k>1):
								data[i+k] = re.split('\n',data[i+k])[0]
								if(count==1):
									data[i+k] += '(org)\n'
								elif(printed == 0):
									data[i+k] += '(org_start)\n'
								elif(printed < count-1):
									data[i+k] += '(org_cont)\n'
								else:
									data[i+k] += '(org_end)\n'
								printed += 1	
			if(data[i] == 'สภา\n' or data[i] == 'องค์การ\n' or data[i] =='ธนาคาร\n' or data[i] == 'บรรษัท\n'):
				for j in range(10):
					if(data[i+j] == 'แห่ง\n'):
						if(data[i+j+1] == 'ประเทศ\n'):
							for k in range(j+3):
								if(k>0):
									data[i+k] = re.split('\n',data[i+k])[0]
									if(k==1):
										data[i+k] += '(org_start)\n'
									elif(k==j+2):
										data[i+k] += '(org_end)\n'
									else:
										data[i+k] += '(org_cont)\n'
						elif(data[i+j+1]=='ชาติ\n'):
							for k in range(j+2):
								if(k>0):
									data[i+k] = re.split('\n',data[i+k])[0]
									if(k==1):
										data[i+k] += '(org_start)\n'
									elif(k==j+1):
										data[i+k] += '(org_end)\n'
									else:
										data[i+k] += '(org_cont)\n'
						else:
							for k in range(j+10):
								if(data[i+k] == ' \n'):
									data[i+k-1] = re.split('\(',data[i+k-1])[0]
									data[i+k-1] += '(org_end)\n'
									break
								if(k>0):
									data[i+k] = re.split('\n',data[i+k])[0]
									if(k==1):
										data[i+k] += '(org_start)\n'
									else:
										data[i+k] += '(org_cont)\n'
			if(data[i] == 'นาย\n' or data[i] == 'นาง\n' or data[i] == 'นางสาว\n' or data[i] == 'เด็กชาย\n' or data[i] == 'เด็กหญิง\n' or data[i] == 'ด.ช.\n' or data[i] == 'ด.ญ.\n'):
				if(data[i+2] == ' \n' and (data[i+4] == ' \n' or data[i+4]== ',\n' or data[i+4] == 'และ\n')):
					for k in range(4):
						if(k>0):
							data[i+k] = re.split('\n',data[i+k])[0]
							if(k==1):
								data[i+k] += '(per_start)\n'
							elif(k==3):
								data[i+k] += '(per_end)\n'
							else:
								data[i+k] += '(per_cont)\n'
				else:
					data[i+1] = re.split('\n',data[i+1])[0]
					data[i+1] += '(per)\n'
			#print data[i],

# make word feature #
word_feature = []
for i in range(len(data)):
	test = re.search('(.*)(?=\(per|\(org)',data[i])
	if(test):
		word = test.group(0) + '\n'
	else :
		word = data[i]
	test = re.search('(?<=\()[po].*(?=\))',data[i])
	if(test):
		tagged = test.group(0)
	else :
		tagged = 'O'
	dict_pre_org = (word in pre_org_dict)
	dict_pre_per = (word in pre_per_dict)
	dict_sub_per = (word in sub_per_dict)
	dict_common = (word in common_dict)
	word_feature.append([tagged,dict_pre_org,dict_pre_per,dict_sub_per,dict_common])
	
useful_feature = []
useless_word = ['O',False,False,False,False]
for i in range(len(word_feature)):
	feature = []
	for j in range(13):
		if(i+j-6 < 0 or i+j-6 >= len(word_feature)):
			feature.extend(useless_word)
		else:
			feature.extend(word_feature[i+j-6])
	feature.append(word_feature[i])
	useful_feature.append(feature)
#names = []
#for j in range(13):
	#names.append('word'+str(j-2))
	#names.append('tagged'+str(j-6))
	#names.append('dict_pre_org'+str(j-6))
	#names.append('dict_pre_per'+str(j-6))
	#names.append('dict_sub_per'+str(j-6))
	#names.append('dict_common'+str(j-6))
#names.append('class')
#arff.dump(open('test.arff','w'),useful_feature,relation="eiei",names)
#arff.dump('result.arff', useful_feature, relation="eiei", names=names) 