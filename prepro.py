# -*- coding: utf-8 -*-
import re
filename = ['untagged.out']
for fn in filename:
	with open(fn) as f:
		data = []
		for line in f:
			data.append(line)
		for i in range(len(data)):
			if(data[i] == 'บริษัท\n'):
				for j in range(7):
					if(data[i+j] == 'จำกัด\n'):
						count = j-3
						printed = 0
						for k in range(j-1):
							if(k>1):
								data[i+k] = re.split('\n',data[i+k])[0]
								if(count==1):
									data[i+k] += '(org)\n'
								elif(printed == 0):
									data[i+k] += '(org_begin)\n'
								elif(printed < count-1):
									data[i+k] += '(org_cont)\n'
								else:
									data[i+k] += '(org_end)\n'
								printed += 1	
			elif(data[i] == 'สภา\n'):
				for j in range(7):
					if(data[i+j] == 'แห่ง\n'):
						if(data[i+j+1] == 'ชาติ\n'):
							for k in range(j+2):
								if(k>0):
									data[i+k] = re.split('\n',data[i+k])[0]
									if(k==1):
										data[i+k] += '(org_begin)\n'
									elif(k==j+1):
										data[i+k] += '(org_end)\n'
									else:
										data[i+k] += '(org_cont)\n'
						if(data[i+j+1] == 'ประเทศ\n'):
							for k in range(j+3):
								if(k>0):
									data[i+k] = re.split('\n',data[i+k])[0]
									if(k==1):
										data[i+k] += '(org_begin)\n'
									elif(k==j+2):
										data[i+k] += '(org_end)\n'
									else:
										data[i+k] += '(org_cont)\n'
			print data[i],