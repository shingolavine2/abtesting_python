from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import chi2

from abtesting_test import *

# You can comment out these lines! They are just here to help follow along to the tutorial.
'''
print(t_dist.cdf(-2, 20)) # should print .02963
print(t_dist.cdf(2, 20)) # positive t-score (bad), should print .97036 (= 1 - .2963)

print(chi2.cdf(23.6, 12)) # prints 0.976
print(1 - chi2.cdf(23.6, 12)) # prints 1 - 0.976 = 0.023 (yay!)
'''

# TODO: Fill in the following functions! Be sure to delete "pass" when you want to use/run a function!
# NOTE: You should not be using any outside libraries or functions other than the simple operators (+, **, etc)
# and the specifically mentioned functions (i.e. round, cdf functions...)

time_completion_data_a = """7462.00
8960.00
9442.00
11718.00
10093.00
9547.00
8059.00
8010.00
2652.00
6634.00
38259.00"""

time_completion_data_b = """3395.00
5749.00
4592.00
2689.00
6130.00
19172.00
207046.00
40336.00
408445.00
296873.00
9243.00
11597.00"""

return_rate_a = """4	7"""

return_rate_b = """5	7"""

def get_avg(nums):
	'''
	Helper function for calculating the average of a sample.
	:param nums: list of numbers
	:return: average of list
	'''
	avg = 0
	for num in nums:
		avg += num
	avg = avg/len(nums)
	return avg

def get_stdev(nums):
	'''
	Helper function for calculating the standard deviation of a sample.
	:param nums: list of numbers
	:return: standard deviation of list
	'''
	standard_dev = 0
	average = get_avg(nums)
	running = 0
	for num in nums:
		running += (num - average) ** 2
	running = running / (len(nums) - 1)
	standard_dev = running ** 0.5
	return standard_dev

def get_standard_error(a, b):
	'''
	Helper function for calculating the standard error, given two samples.
	:param a: list of numbers
	:param b: list of numbers
	:return: standard error of a and b (see studio 6 guide for this equation!)
	'''
	term1 = (get_stdev(a) ** 2)/len(a)
	term2 = (get_stdev(b) ** 2)/len(b)
	standard_err = (term1 + term2) ** 0.5
	return standard_err

def get_2_sample_df(a, b):
	'''
	Calculates the combined degrees of freedom between two samples.
	:param a: list of numbers
	:param b: list of numbers
	:return: integer representing the degrees of freedom between a and b (see studio 6 guide for this equation!)
	HINT: you can use Math.round() to help you round!
	'''
	#TODO: fill me in!
	se = get_standard_error(a, b) ** 4
	term1 = (((get_stdev(a)**2)/len(a))**2)/(len(a)-1)
	term2 = (((get_stdev(b)**2)/len(b))**2)/(len(b)-1)
	df = round(se/(term1 + term2))
	return df

def get_t_score(a, b):
	'''
	Calculates the t-score, given two samples.
	:param a: list of numbers
	:param b: list of numbers
	:return: number representing the t-score given lists a and b (see studio 6 guide for this equation!)
	'''
	topterm = get_avg(a) - get_avg(b)
	botterm = get_standard_error(a, b)
	tscore = topterm / botterm
	return tscore
	

def perform_2_sample_t_test(a, b):
	tscore = get_t_score(a, b)
	df = get_2_sample_df(a, b)
	pscore = t_dist.cdf(tscore, df)
	return pscore
	'''
	** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
	Calculates a p-value by performing a 2-sample t-test, given two lists of numbers.
	:param a: list of numbers
	:param b: list of numbers
	:return: calculated p-value
	HINT: the t_dist.cdf() function might come in handy!
	'''


# [OPTIONAL] Some helper functions that might be helpful in get_expected_grid().
# def row_sum(observed_grid, ele_row):
# def col_sum(observed_grid, ele_col):
# def total_sum(observed_grid):
# def calculate_expected(row_sum, col_sum, tot_sum):
# numrows = len(input)
# numcols = len(input[0])
#

def slice_2D(list_2D, start_row, end_row, start_col, end_col):
	'''
	Splices a the 2D list via start_row:end_row and start_col:end_col
	:param list: list of list of numbers
	:param nums: start_row, end_row, start_col, end_col
	:return: the spliced 2D list (ending indices are exclsive)
	'''
	to_append = []
	for l in range(start_row, end_row):
		to_append.append(list_2D[l][start_col:end_col])

	return to_append

def row_sum(observed_grid, ele_row):
	'''
	takes the observed_grid and sums up the row from ele_row
	:param observed_grid: list of list of numbers
	:param ele_row: number
	:return: number which is the sum of the row
	'''
	total = 0
	for i in range(len(observed_grid)): 
		for j in range(len(observed_grid[0])):  
			total += observed_grid[i][j] 
		if i == ele_row:
			return total
		total = 0


def col_sum(observed_grid, ele_col):
	'''
	takes the observed_grid and sums up the column from ele_col
	:param observed_grid: list of list of numbers
	:param ele_col: number
	:return: number which is the sum of the column
	'''
	total = 0
	for i in range(len(observed_grid[0])): 
		for j in range(len(observed_grid)): 
			total += observed_grid[j][i] 
		if i == ele_col:
			return total	
		total = 0

def total_sum(observed_grid):
	'''
	takes the observed_grid and sums every element in the grid
	:param observed_grid: list of list of numbers
	:return: number which is the sum of every element
	'''
	total = 0
	for row in range(len(observed_grid)):
		for col in range(len(observed_grid[0])):
			total += observed_grid[row][col]
	return total


def calculate_expected(row_sum, col_sum, tot_sum):
	'''
	takes three numbers (row_sum, col_sum, tot_sum) and does math to return expected
	:param row_sum: number
	:param col_sum: number
	:param tot_sum: number
	:return: number which is expected frequency
	'''
	topterm = row_sum * col_sum
	botterm = tot_sum
	frequency = topterm / botterm
	return frequency

def get_expected_grid(observed_grid):
	'''
	Calculates the expected counts, given the observed counts.
	** DO NOT modify the parameter, observed_grid. **
	:param observed_grid: 2D list of observed counts
	:return: 2D list of expected counts
	HINT: To clean up this calculation, consider filling in the optional helper functions below!
	'''
	#TODO: fill me in!
	newlist = [[0 for j in range(len(observed_grid[0]))] for i in range(len(observed_grid))]
	mytot_sum = total_sum(observed_grid)
	myrow_sum = 0
	mycol_sum = 0
	expected = 0
	for row in range(len(observed_grid)):
		for col in range(len(observed_grid[0])):
			myrow_sum = row_sum(observed_grid, row)
			mycol_sum = col_sum(observed_grid, col)
			expected = calculate_expected(myrow_sum, mycol_sum, mytot_sum)
			newlist[row][col] = expected
	return newlist

def df_chi2(observed_grid):
	'''
	Calculates the degrees of freedom of the expected counts.
	:param observed_grid: 2D list of observed counts
	:return: degrees of freedom of expected counts (see studio 6 guide for this equation!)
	'''
	#TODO: fill me in!
	df = (len(observed_grid) - 1) * (len(observed_grid[0]) - 1)
	return df

def chi2_value(observed_grid):
	'''
	Calculates the chi^2 value of the expected counts.
	:param observed_grid: 2D list of observed counts
	:return: associated chi^2 value of expected counts (see studio 6 guide for this equation!)
	'''
	#TODO: fill me in!
	total = 0
	newlist = get_expected_grid(observed_grid)
	for row in range(len(observed_grid)):
		for col in range(len(observed_grid[row])):
			topterm = (observed_grid[row][col] - newlist[row][col])**2
			botterm = newlist[row][col]
			total += topterm/botterm
	return total

def perform_chi2_homogeneity_test(observed_grid):
	'''
	** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
	Calculates the p-value by performing a chi^2 test, given a list of observed counts
	:param observed_grid: 2D list of observed counts
	:return: calculated p-value
	HINT: the chi2.cdf() function might come in handy!
	'''
	#TODO: fill me in!
	mychi2 = chi2_value(observed_grid)
	df = df_chi2(observed_grid)
	return (1 - (chi2.cdf(mychi2, df)))

# These commented out lines are for testing your main functions. 
# Please uncomment them when finished with your implementation and confirm you get the same values :)
def data_to_num_list(s):
  '''
	Takes a copy and pasted row/col from a spreadsheet and produces a usable list of nums. 
	This will be useful when you need to run your tests on your cleaned log data!
	:param str: string holding data
	:return: the spliced list of numbers
	'''
  return list(map(float, s.split()))

# t_test on completion data
a_completion_list = data_to_num_list(time_completion_data_a)
b_completion_list = data_to_num_list(time_completion_data_b)
print("T test data for completion time: ")
print("t_score: " + str(get_t_score(a_completion_list, b_completion_list)))
print("p value: " + str(perform_2_sample_t_test(a_completion_list, b_completion_list)))

# chi2_test on return rate data
a_return_list = data_to_num_list(return_rate_a)
b_return_list = data_to_num_list(return_rate_b)
return_observed_grid = [a_return_list, b_return_list]
print("Chi2_test : " + str(chi2_value(return_observed_grid)))
print("Chi2_homogeneity_test: " + str(perform_chi2_homogeneity_test(return_observed_grid)))

'''
# t_test 1:
a_t1_list = data_to_num_list(a1) 
b_t1_list = data_to_num_list(b1)
print("Should be -129.500: " + str(get_t_score(a_t1_list, b_t1_list))) # this should be -129.500
print("Should be 0.0000: " + str(perform_2_sample_t_test(a_t1_list, b_t1_list))) # this should be 0.0000
# why do you think this is? Take a peek at a1 and b1 in abtesting_test.py :)

# t_test 2:
a_t2_list = data_to_num_list(a2) 
b_t2_list = data_to_num_list(b2)
print("Should be -1.48834 " + str(get_t_score(a_t2_list, b_t2_list))) # this should be -1.48834
print("Should be .082379 " + str(perform_2_sample_t_test(a_t2_list, b_t2_list))) # this should be .082379

# t_test 3:
a_t3_list = data_to_num_list(a3) 
b_t3_list = data_to_num_list(b3)
print("Should be -2.88969: " + str(get_t_score(a_t3_list, b_t3_list))) # this should be -2.88969
print("Should be .005091 " + str(perform_2_sample_t_test(a_t3_list, b_t3_list))) # this should be .005091
"""

"""
# chi2_test 1:
a_c1_list = data_to_num_list(a_count_1) 
b_c1_list = data_to_num_list(b_count_1)
c1_observed_grid = [a_c1_list, b_c1_list]
print("Should be 4.103536: " + str(chi2_value(c1_observed_grid))) # this should be 4.103536
print("Should be .0427939: " + str(perform_chi2_homogeneity_test(c1_observed_grid))) # this should be .0427939

# chi2_test 2:
a_c2_list = data_to_num_list(a_count_2) 
b_c2_list = data_to_num_list(b_count_2)
c2_observed_grid = [a_c2_list, b_c2_list]
print("Should be 33.86444: " + str(chi2_value(c2_observed_grid))) # this should be 33.86444
print("Should be 0.0000: " + str(perform_chi2_homogeneity_test(c2_observed_grid))) # this should be 0.0000
# Again, why do you think this is? Take a peek at a_count_2 and b_count_2 in abtesting_test.py :)

# chi2_test 3:
a_c3_list = data_to_num_list(a_count_3) 
b_c3_list = data_to_num_list(b_count_3)
c3_observed_grid = [a_c3_list, b_c3_list]
print("Should be .3119402: " + str(chi2_value(c3_observed_grid))) # this should be .3119402
print("Should be .57649202: " + str(perform_chi2_homogeneity_test(c3_observed_grid))) # this should be .57649202
'''

