import csv
from collections import Counter
import numpy as np
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

def main():
	# Read all mails and create a word dictionary with the count of each word
	filename = 'spam_ham.csv'
	data = csv.reader(open(filename, "rb"))
	ham_count = 0
	spam_count = 0
	all_words = []
	all_ham_words = []
	all_spam_words = []
	for line in data:
		mail = line[1].lower()
		words = mail.split()
		all_words += words 
		if line[0] == 'ham':
			all_ham_words += words
			ham_count += 1
		elif line[0] == 'spam':
			all_spam_words += words
			spam_count += 1

	full_dict = Counter(all_words)

	# Remove all non-alphabet words and all single letter 
	list_to_remove = full_dict.keys()
	for item in list_to_remove:
		if item.isalpha() == False: 
			del full_dict[item]
		elif len(item) == 1:
			del full_dict[item]

	# taking 5000 most frequently used words to reduce computation time
	full_dict = dict(full_dict.most_common(5000))
	
	total_mails = ham_count + spam_count

	# creating feature space and corresponding labels
	feature_matrix = np.zeros((total_mails,5000))
	train_labels = np.zeros(total_mails)

	mail_ID = 0
	data = csv.reader(open(filename, "rb"))
	loop = 0;
	for mails in data:
		if loop != 0:
			line = mails[1].lower()
			if mails[0] == 'ham':
				train_labels[mail_ID] = 0 
			elif mails[0] == 'spam':
				train_labels[mail_ID] = 1
			words = line.split()
			for word in words:
				word_ID = 0
				for i,d in enumerate(full_dict):
					if d == word:
						word_ID = i
						feature_matrix[mail_ID,word_ID] = words.count(word)
			mail_ID += 1
		else:
			loop = 1

	train_matrix = feature_matrix

	# using MultinomialNB for classification  
	model1 = BernoulliNB()
	# Different Naive Bayesian Classifiers that can be used as well. 
	# model2 = GaussianNB()
	# model3 = MultinomialNB()

	# fitting the training data
	model1.fit(train_matrix,train_labels)

	# extracting features from test data
	mail_ID = 0
	test_matrix = np.zeros((2,5000))
	with open('text.txt',"r") as file1:
		for line in file1:
			words = line.split()
			for word in words:
				word_ID = 0
				for i,d in enumerate(full_dict):
					if d == word:
						word_ID = i
						test_matrix[mail_ID,word_ID] = words.count(word)
			mail_ID += 1

	test_labels = np.zeros(2)
	test_labels[1] = 1

	# predicting spam/ham using the trained classifier 
	result = model1.predict(test_matrix)
	
	# printing the results
	i = 0
	with open('text.txt',"r") as file1:
		for line in file1:
			if result[i] == 0:
				prediction = 'ham'
			else:	
				prediction = 'spam'

			print line
			print "\nThe above message is " + prediction + "\n"
			i += 1
main()
