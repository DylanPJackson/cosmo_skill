"""
	filename
		prioritization_function_test.py

	description
		Currently just testing grounds to implement the prioritization function
		and the accompanying knapsack algorithm.

	author
		Dylan P. Jackson (original contributor)
"""
import numpy as np

class Reminder:
	"""
		Basic class to encapsulate the data for a Reminder as it is stored 
		in the universe database
	"""
	def __init__(self, r_id, description, expiration, complete_time, creation_date):
		self.r_id = r_id
		self.description = description
		self.expiration = expiration
		self.complete_time = complete_time
		self.creation_date = creation_date

	def __repr__(self):
		return "Reminder(r_id : {}, description : {}, expiration : {}, complete_time : {}, creation_date : {})".format(
				self.r_id, self.description, self.expiration,
				self.complete_time, self.creation_date)
	
def prioritize(reminders):
	"""
		Generates value for each reminder based off of their expiration and
		creation dates

		Parameters
		----------
		reminders : list<Reminder>
		
		Returns
		-------
		dict<int (r_id) : int (priority)>
			Dictionary mapping reminder_id to their priority
	"""

	# Dictionary mapping reminder_id's to their priorities
	priorities = {}
	# 2d list of reminder_id and expiration date 
	expirations = []
	# 2d list of reminder_id and creation date 
	creations = []
	
	# Initialize each data structure
	for reminder in reminders:
		r_id = reminder.r_id
		exp = reminder.expiration
		cre = reminder.creation_date

		priorities[r_id] = 0
		expirations += [[r_id, exp]]
		creations += [[r_id, cre]]

	# Sort expiration and creation lists by their exp and cre dates 
	expirations.sort(key = lambda x:x[1], reverse = True)
	#print("Expirations : " + str(expirations))
	creations.sort(key = lambda x:x[1])
	#print("Creations: " + str(creations))
	
	# Calculate priorities
	num_priorities = len(expirations)
	for i in range(1, num_priorities + 1):
		# Get expiration / creation ID's
		exp_id = expirations[i-1][0]
		cre_id = creations[i-1][0]
		# Calculate weight for each
		exp_value = .8 * i
		cre_value = .2 * i
		# Update weight for that ReminderID
		priorities[exp_id] = round(priorities[exp_id] + exp_value, 2)
		priorities[cre_id] = round(priorities[cre_id] + cre_value, 2)
	
	return priorities

def knapsack_indv(n, c, w, W):
	"""
		Performs knapsack algorithm to determine which Reminders can / should
		be done 

		Parameters
		----------
		n : int
			The number of Reminders considered
		c : list<float> 
			vector of values associated with Reminders (From prioritize())
			Sorted by w
		w : list<int>
			vector of complete_time (weights) associated with Reminders	
			Assumed that this is sorted in ascending order
		W : int
			The total available time (total weight) at the time 
		
		Returns
		-------
		list<int>
			List of indices essentially, which are mapped to r_id's at index
			specified by sorted r_id's by complete_time
	"""
	# Initialize solution matrix
	S = [[0 for i in range(W + 1)] for i in range(n + 1)]

	# Iterate through possible times / weights 
	for v in range(1,(W + 1)):
		# Iterate through each Reminder 
		for j in range(1, (n + 1)):
			S[j][v] = S[j - 1][v]
			w_j = int(w[j - 1])
			c_j = c[j - 1]
			new_val = (S[j - 1][v - w_j]  + c_j) 
			cur_val = S[j][v]
			# If weight of new item less than current weight and
			# added value greater than current, include it
			if (w_j <= v) and (new_val > cur_val):
				S[j][v] = round(new_val,2)

	# Display the Solution matrix
	for i in range(0, (n + 1)):
		print(S[i])

	# List of indices to be returned
	inds = []
	# Vars for traversing back through S 
	rev_W = W
	# Traverse back through S to find included Reminders 
	for i in range(n,-1,-1):
		# Get weight and value of given Reminder
		w_n = int(w[i - 1])
		c_n = int(c[i - 1])
		# If weight of given item is greater than alloted, cant have neg weight
		if (rev_W - w_n) < 0:
			continue
		prev_cost = S[i - 1][rev_W - w_n] + c_n
		if prev_cost >= S[i - 1][rev_W]:
			inds = [i] + inds	
			rev_W -= w_n

	return inds 
		

def main():
	# Lets create some reminders
	reminder_1 = Reminder(1, "dog", 3, 3, 8)
	reminder_2 = Reminder(2, "cat", 6, 4, 2)
	reminder_3 = Reminder(3, "fish", 4, 2, 10)
	reminder_4 = Reminder(4, "towel", 8, 6, 7)
	reminder_5 = Reminder(5, "york", 2, 1, 5)
	reminders = [reminder_1, reminder_2, reminder_3, reminder_4, reminder_5]
	for reminder in reminders:
		#print(reminder)
		pass

	# And generate their priorities 
	priorities = prioritize(reminders)
	print("priorities : " + str(priorities))

	# And reverse_priorities dict to map value back to r_id
	rev_prior = {}
	for r_id in priorities.keys():
		val = priorities[r_id]
		rev_prior[val] = r_id 
	print("rev_prior : " + str(rev_prior))

	# Time to generate the value and weight lists
	r_ids = list(priorities.keys())
	r_ids.sort()
	c_w = []
	comp_ids = {} 
	for r_id in r_ids:
		c_w += [[priorities[r_id], reminders[r_id - 1].complete_time, r_id]]	
		
	c_w.sort(key = lambda x:x[1])
	n_c_w = np.array(c_w)
	c = list(n_c_w[:,0])
	w = list(n_c_w[:,1])
	print("c: " + str(c))
	print("w: " + str(w))

	# Establish other knapsack paramters
	W = 5 
	n = len(reminders)

	inds = knapsack_indv(n, c, w, W)
	print("inds: " + str(inds))
	# Included Reminder ID's
	inc_ids = []
	for ind in inds:
		inc_ids.append(rev_prior[c[ind - 1]])
	print("Included Reminder ID's : " + str(inc_ids))


main()
