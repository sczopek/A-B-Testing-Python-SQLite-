import random
import sqlite3


def createCursor(dbFilePath):
	conn = sqlite3.connect(dbFilePath)
	conn.text_factory = str
	c = conn.cursor()
	
	#return cursor
	return c, conn
	
def getTestSamples(cursor, loanGrade, statPower, sampleSize):
	if loanGrade=="A":
		cursor.execute("SELECT loan_status FROM gradeA_Loans;")
	else:
		cursor.execute("SELECT loan_status FROM gradeC_Loans;")
	doubleTestSample = cursor.fetchall()
	doubleTestSample = [singleTuple[0] for singleTuple in doubleTestSample]
	
	doubleRandIndex = random.sample(xrange(sampleSize), sampleSize)
	randIndex1 = random.sample(doubleRandIndex, int(sampleSize/2))
	sample1 = map(doubleTestSample.__getitem__, randIndex1)

	randIndex2 = set(doubleRandIndex) - set(randIndex1)
	# convert from set to list
	randIndex2 = list(randIndex2)
	# randomize sample order
	randIndex2 = random.sample(randIndex2,len(randIndex2))
	sample2 = map(doubleTestSample.__getitem__, randIndex2)
	#return testSample
	return sample1, sample2
		
def run_A_B_Test(treatmentSample, controlSample, N, testSuccessVal):
	i=0
	d=0
	testSuccessCount=0
	sampleSize = min(len(treatmentSample), len(controlSample))
	while testSuccessCount<N and i<sampleSize:
		#deal with the treatment group first
		#if loan_status = "Charged Off":
		if treatmentSample[i] == testSuccessVal:
			testSuccessCount+=1
			d+=1
	
		#now deal with the control group	
		#if loan_status = "Charged Off":
		if controlSample[i] == testSuccessVal:
			testSuccessCount+=1
			d-=1
		i+=1
	
	return d, testSuccessCount 	
	
def main():
	sampleSize=148202
	N = 2441
	statPower = 2441
	sigDiffThreshold = 96
	dbFilePath = "/Users/scottczopek/loanData.db"
	c, conn = createCursor(dbFilePath)

	sampleA1, sampleA2 = getTestSamples(c, "A", N, sampleSize)	
	sampleB1, sampleB2 = getTestSamples(c, "C", N, sampleSize)

	d_A1A2, coCountA1A2 = run_A_B_Test(sampleA1, sampleA2, N, "Charged Off")
	d_B1B2, coCountB1B2 = run_A_B_Test(sampleB1, sampleB2, N, "Charged Off")
	d_A1B1, coCountA1B1 = run_A_B_Test(sampleB1, sampleA1, N, "Charged Off")
	d_A2B2, coCountA2B2 = run_A_B_Test(sampleB2, sampleA2, N, "Charged Off")
	
	print("A1/A2", d_A1A2, coCountA1A2, sigDiffThreshold)
	print("B1/B2", d_B1B2, coCountB1B2, sigDiffThreshold)
	print("A1/B1", d_A1B1, coCountA1B1, sigDiffThreshold)
	print("A2/B2", d_A2B2, coCountA2B2, sigDiffThreshold)
	
	conn.close()
	
if __name__== "__main__":
	main()
  
  	
#largest possible
#sampleSize=254435
sampleSize=148202
# N is the number of charged off loan included in this test
N = 2441
doubleRandIndexA = random.sample(xrange(sampleSize), sampleSize)
randIndexA1 = random.sample(doubleRandIndexA, int(sampleSize/2))

randIndexA2 = set(doubleRandIndexA) - set(randIndexA1)

#duplicate = False
#for elem in randIndexA1:
#	if elem in randIndexA2:
#		duplicate = True
#		break

# convert from set to list
randIndexA2 = list(randIndexA2)
# randomize sample order
randIndexA2 = random.sample(randIndexA2,len(randIndexA2))

#print("doubleRandIndexA", doubleRandIndexA[:100])
#print("randIndexA1", randIndexA1[:100])
#print("randIndexA2", randIndexA2[:100])

print("len(doubleRandIndexA)", len(doubleRandIndexA))		
print("len(randIndexA1)", len(randIndexA1))
print("len(randIndexA2)", len(randIndexA2))

		
#print("duplicate", duplicate)

conn = sqlite3.connect("/Users/scottczopek/loanData.db")
conn.text_factory = str
c = conn.cursor()
c.execute("SELECT loan_status FROM gradeA_Loans;")
dataDoubleA = c.fetchall()
dataDoubleA = [singleTuple[0] for singleTuple in dataDoubleA]
print(dataDoubleA[:100])
print("len(dataDoubleA)", len(dataDoubleA))
#print(dataDoubleA[15][0])




#SELECT column_1 FROM table_1 WHERE column_1 = (
#    SELECT column_1 FROM table_2);

# d = T-C
# T are the treatment charge offs
# C are the control charge offs
i=0
d=0
coCount=0
while coCount < N and i<len(randIndexA1) and i<len(randIndexA2):
	#deal with the treatment group first
	#if loan_status = "Charged Off":
	if dataDoubleA[randIndexA1[i]] == "Charged Off":
		coCount+=1
		d+=1
	
	#now deal with the control group	
	#if loan_status = "Charged Off":
	if dataDoubleA[randIndexA2[i]] == "Charged Off":
		coCount+=1
		d-=1
	i+=1

print("N", N)
print("d", d)

print()
print()
print()
print("Starting to Analyze C Grade Loans")
doubleRandIndexC = random.sample(xrange(sampleSize), sampleSize)
randIndexC1 = random.sample(doubleRandIndexC, int(sampleSize/2))
randIndexC2 = set(doubleRandIndexC) - set(randIndexC1)
randIndexC2 = list(randIndexC2)
randIndexC2 = random.sample(randIndexC2, len(randIndexC2))

c.execute("SELECT loan_status FROM gradeC_Loans;")
dataDoubleC = c.fetchall()
dataDoubleC = [singleTuple[0] for singleTuple in dataDoubleC]
#SELECT column_1 FROM table_1 WHERE column_1 = (
#    SELECT column_1 FROM table_2);

# d = T-C
# T are the treatment charge offs
# C are the control charge offs
i=0
d=0
coCount=0
while coCount < N and i<len(randIndexC1) and i<len(randIndexC2):
	#deal with the treatment group first
	#if loan_status = "Charged Off":
	if dataDoubleC[randIndexC1[i]] == "Charged Off":
		coCount+=1
		d+=1
	
	#now deal with the control group	
	#if loan_status = "Charged Off":
	if dataDoubleC[randIndexC2[i]] == "Charged Off":
		coCount+=1
		d-=1
	i+=1

print("N", N)
print("d", d)


print()
print()
print("A1/B1")
# d = T-C
# T are the treatment charge offs
# C are the control charge offs
i=0
d=0
coCount=0
while coCount < N and i<len(randIndexA1) and i<len(randIndexC1):
	#deal with the treatment group first
	#if loan_status = "Charged Off":
	if dataDoubleC[randIndexC1[i]] == "Charged Off":
		coCount+=1
		d+=1
	
	#now deal with the control group	
	#if loan_status = "Charged Off":
	if dataDoubleA[randIndexA1[i]] == "Charged Off":
		coCount+=1
		d-=1
	i+=1

print("N", N)
print("d", d)

print()
print()
print("A2/B2")
# d = T-C
# T are the treatment charge offs
# C are the control charge offs
i=0
d=0
coCount=0
while coCount < N and i<len(randIndexA2) and i<len(randIndexC2):
	#deal with the treatment group first
	#if loan_status = "Charged Off":
	if dataDoubleC[randIndexC2[i]] == "Charged Off":
		coCount+=1
		d+=1
	
	#now deal with the control group	
	#if loan_status = "Charged Off":
	if dataDoubleA[randIndexA2[i]] == "Charged Off":
		coCount+=1
		d-=1
	i+=1

print("N", N)
print("d", d)

print()
print()
print("A1/B2")
# d = T-C
# T are the treatment charge offs
# C are the control charge offs
i=0
d=0
coCount=0
while coCount < N and i<len(randIndexA1) and i<len(randIndexC2):
	#deal with the treatment group first
	#if loan_status = "Charged Off":
	if dataDoubleC[randIndexC2[i]] == "Charged Off":
		coCount+=1
		d+=1
	
	#now deal with the control group	
	#if loan_status = "Charged Off":
	if dataDoubleA[randIndexA1[i]] == "Charged Off":
		coCount+=1
		d-=1
	i+=1

print("N", N)
print("d", d)

print()
print()
print("A2/B1")
# d = T-C
# T are the treatment charge offs
# C are the control charge offs
i=0
d=0
coCount=0
while coCount < N and i<len(randIndexA2) and i<len(randIndexC1):
	#deal with the treatment group first
	#if loan_status = "Charged Off":
	if dataDoubleC[randIndexC1[i]] == "Charged Off":
		coCount+=1
		d+=1
	
	#now deal with the control group	
	#if loan_status = "Charged Off":
	if dataDoubleA[randIndexA2[i]] == "Charged Off":
		coCount+=1
		d-=1
	i+=1

print("N", N)
print("d", d)