# A-B-Testing-Python-SQLite-
A/B testing to investigate personal loan data.
using Python and SQLite

This software demos Evan Miller's A/B testing algorithm using Lending Club Loan Data.  An overview for each file is given, followed by some project notes including a getting started and installation guide.  The A/B testing algorithm is validated by confirming that personal loans with lower credit grades have a statistically higher charge off rate.  A letter grade, "A" - "G", is associated with each loans credit worthiness.  An 11% difference in total number of charged offs, between one letter grade and loans given at two letter grades below the first (e.g. "A" vs "C" grades), was the effect size that was tested for.  (There weren't enough samples to provide enough statistical power to detect a 10% difference.)  The algorithm was able to detect a statistically significant difference between loans of different letter grades, and did not detect a statistically significant difference between loans of the same letter grades. 



### ABtest_loan_data_example.py

This script is used to validate my A/B testing algorithm, by showing that personal loans with a lower credit grade have a significantly higher loan charge off rate than personal loans of a higher credit rating.  This is an A/A/B/B test, which confirms that there is no significant A/A or B/B variation while also checking for any significant A/B difference.

### lendingClubLoanDataLite.sqlite

This is an abridged SQLite3 database, which contains personal loan data.  With +800,000 personal loans, with letter grades "A" - "G", this dataset is robust.  Each loan's status is examined, with particular interest given to loans that have moved beyond default and that have now been "Charged Off".  This dataset was obtained through Kaggle, and originated a the Lending Club, which offers personal loans at: https://www.lendingclub.com/

### Summary: 
This module implements an algorithm used to calculate the needed sample size to run an A/B test.  This calculator uses Evan Miller's algorithm.
          
          
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

**Python 2.7**

(Written in Python 2.7.12)

Ablility to run Python script from command line.

### Installing

A step by step series of examples that tell you have to get a development env running

Download and save all files to the same local directory.

Change $PWD ($PathWorkingDirectory) to that directory. Then run this script, then run the script.  The test results will print to the output screen..

```
python -V
python ABtest_loan_data_example.py
```


## Running the tests

To be added.

## Versioning

v 0.1

## Authors

* **Scott Czopek** - *Initial work* - 08/20/18 - [A/B Testing](https://github.com/sczopek/A-B-Testing-Python-SQLite-)

## License

This project is free to copy and distribute.

## Acknowledgments

* I would like to thank my Evan Miller for his excellent A/B tutorial and sample size calculator.
