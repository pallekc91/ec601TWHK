import sys


'''
Available Departments
General
Finance [fee,rate,costly,refund,pricy,pricing,]
Police [safety,threatned, distress, help, police, unsafe, security]
Parking [parking]
Maintanance [cleanliness, dirty, ugly, maintanance, ]
'''

def identifyDepartment(tweetsJson):
	for key in tweetsJson.keys():
		Department = idDepartment(tweetsJson[key]['text'])
		tweetsJson[key]['Department'] = Department
	return tweetsJson

def idDepartment(text):
	Finance = ['fee','rate','costly','refund','pricy','pricing']
	Police = ['safety','threatned', 'distress', 'help', 'police', 'unsafe', 'security']
	Parking = ['parking']
	Maintanance = ['cleanliness', 'dirty', 'ugly', 'maintanance']

	departments = []
	for word in text.split():
		if(word in Finance):
			departments.append('Finance')
		if(word in Police):
			departments.append('Police')
		if(word in Parking):
			departments.append('Parking')
		if(word in Maintanance):
			departments.append('Maintanance')
	if len(departments) == 0:
		departments.append("General");
	return departments
