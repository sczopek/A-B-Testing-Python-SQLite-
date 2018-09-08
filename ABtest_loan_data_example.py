import random
import sqlite3
import os


def createCursor(dbFilePath):
	conn = sqlite3.connect(dbFilePath)
	conn.text_factory = str
	c = conn.cursor()
	
	#return cursor
	return c, conn
	
def getTestSamples(cursor, loanGrade, statPower, sampleSize):
	#cursor.execute("SELECT loan_status FROM loanData WHERE grade==\""+loanGrade+"\";")
	cursor.execute("SELECT loan_status FROM lendingClubLoanDataLite WHERE grade==\""+loanGrade+"\";")

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
	# Determined by by the grade of personal loans with the fewest samples.
	sampleSize=139542
	
	# A/B Test Sample Size, # of "charged off loans" needed before the test indicates
	# if one of the samples has a significantly higher "charge off rate" than the 
	# other sample.
	N = 2441
	statPower = 2441
	sigDiffThreshold = 96
	pwd = os.path.dirname(os.path.abspath(__file__))
	#dbFilePath = pwd+"/database.sqlite"
	dbFilePath = pwd+"/lendingClubLoanDataLite.sqlite"
	c, conn = createCursor(dbFilePath)

	#compare grade A and grade C personal loans.  First test.
	sampleA1, sampleA2 = getTestSamples(c, "A", N, sampleSize)	
	sampleC1, sampleC2 = getTestSamples(c, "C", N, sampleSize)

	d_A1A2, coCountA1A2 = run_A_B_Test(sampleA1, sampleA2, N, "Charged Off")
	d_C1C2, coCountC1C2 = run_A_B_Test(sampleC1, sampleC2, N, "Charged Off")
	d_A1C1, coCountA1C1 = run_A_B_Test(sampleC1, sampleA1, N, "Charged Off")
	d_A2C2, coCountA2C2 = run_A_B_Test(sampleC2, sampleA2, N, "Charged Off")
	
	
	print "First Column:    Sample/Sample"
	print "Second Column:   Difference in # of Charge Offs"
	print "Third Column:    Difference Threshold for Significance"
	print ""
	
	print("\"A\" Grade vs \"C\" Grade Personal Loans")
	print("A1/A2", d_A1A2, sigDiffThreshold)
	print("C1/C2", d_C1C2, sigDiffThreshold)
	print("A1/C1", d_A1C1, sigDiffThreshold)
	print("A2/C2", d_A2C2, sigDiffThreshold)


	## Run second test comparing B and D grade personal loans.
	N = 2441
	statPower = 2441
	sigDiffThreshold = 96

	sampleB1, sampleB2 = getTestSamples(c, "B", N, sampleSize)	
	sampleD1, sampleD2 = getTestSamples(c, "D", N, sampleSize)

	d_B1B2, coCountB1B2 = run_A_B_Test(sampleB1, sampleB2, N, "Charged Off")
	d_D1D2, coCountD1D2 = run_A_B_Test(sampleD1, sampleD2, N, "Charged Off")
	d_B1D1, coCountB1D1 = run_A_B_Test(sampleD1, sampleB1, N, "Charged Off")
	d_B2D2, coCountB2D2 = run_A_B_Test(sampleD2, sampleB2, N, "Charged Off")
	
	print""
	print""
	
	print("\"B\" Grade vs \"D\" Grade Personal Loans")
	print("B1/B2", d_B1B2, sigDiffThreshold)
	print("D1/D2", d_D1D2, sigDiffThreshold)
	print("B1/D1", d_B1D1, sigDiffThreshold)
	print("B2/D2", d_B2D2, sigDiffThreshold)
	
	conn.close()
	
if __name__== "__main__":
	main()