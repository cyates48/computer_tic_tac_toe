import random
import math 

def setupVariables(attributes, att_val, class_values):
	# creates a dictionary that has atrributes with its values in a set
	for name in attributes:
		att_val[name] = set()
		
	# creates a list of lines for the training data, creates a list with all of the classes
	for line in open("training_data.txt",'r'):
		line = line.split(',')
		if line[-1][-1] == '\n': 
			line[-1] = line[-1][:-1]
		training_data.append(line)
		class_values.add(line[class_index])

		# adds the possible values to an attribute
		for i in range(len(attributes)):
			name = attributes[i]
			outcome = line[i]
			att_val[name].add(outcome)

	# puts the training data in another list, shuffles lines, deletes content of training data
	lines = [ line for line in training_data ]

	# puts lines into three sets of data: training, test, and valid. 
	for i,line in enumerate(lines):
		test_data.append(line)

def findEntropy(training_data, class_values):
	total = len(training_data)
	entropy = 0

	# gives every class an int value
	for class_ in class_values:
		class_num[class_] = 0

	# counts the number of different classes
	for line in training_data:
		class_ = line[class_index]
		class_num[class_] += 1

	# calculates entropy from formula
	for num in class_num.values():
		if num != 0:
			fraction = float (num) / total
			entropy += (math.log(fraction,2) * fraction) * -1
	return entropy

def partitionData(training_data, attribute_value, index):
	# creates a subset of data for a particular value
	p_data = list()
	for line in training_data:
		if attribute_value == line[index]:
			p_data.append(line)
	return p_data

def findBestInfogain(training_data, r_entr, att_val, class_values, label):
	# calculates the best information gain using the formula, partitions the data 
	list_infogains = list()
	for attribute in att_val:
		if attribute != label:
			ave_child_entr = 0
			for attribute_value in att_val[attribute]:
				p_data =  partitionData(training_data,attribute_value, attributes.index(attribute))
				child_entr = findEntropy(p_data, class_values)
				weight_ave = float ( len(p_data) ) / len(training_data)
				ave_child_entr += weight_ave * child_entr
			
			current_infogain = r_entr - ave_child_entr
			list_infogains.append((current_infogain,attribute))
	
	best_infogain = max(list_infogains)
	if best_infogain[0] == 0:
		return (0, training_data[0][class_index])
	else:
		return best_infogain

def createTree(root):
	# creates the decision tree, calls the infogain function to find the next value, uses recursion for leaves
	if root.infogain != 0:
		for attribute_value in att_val[root.next_best_attribute]:
			p_data = partitionData(root.training_data, attribute_value, attributes.index(root.next_best_attribute))
			if len(p_data) != 0:
				child_entr = findEntropy(p_data, class_values)
				temp = findBestInfogain(p_data, child_entr, att_val, class_values, label)
				infogain = temp[0]
				next_best_attribute = temp[1]
				leaf = Node(attribute_value, infogain, next_best_attribute, p_data)
				root.children.append(leaf)

		for leaf in root.children:
			createTree(leaf)

def findValue(root, line):
	# returns the value associated with the attribute
	if len(root.children) == 0:
		return root.next_best_attribute
	for node in root.children:
		if node.value_of_attribute == line[attributes.index(root.next_best_attribute)]:
			return findValue(node, line)

def classifyData(root, test_data):
	# counts the amount of accurate classifications, calls a classify funciton
	correct,total = 0, 0
	for line in test_data:
		total += 1
		if line[class_index] == findValue(root, line):
			correct += 1
	return "Accuracy: " + str(float(correct)/total*100) + "%" 

def printDecisionTree(root,spacing=''):
	# prints the decision tree
	print spacing + root.value_of_attribute + ": " + root.next_best_attribute
	spacing += '   '
	for child in root.children:
		printDecisionTree(child,spacing)
	if root.children == list():
		spacing += '   '
		print spacing,root.next_best_attribute

def playerMove(board,turn):
	# lets player decide their position to put their mark
	yes = True
	while yes:
		position = int(raw_input("Enter the position: "))
		if board[position] == "o" or board[position] == "x":
			print "Position taken, try again."
		else:
			yes = False

	positions.append(position)
	return position

def findBestBranch(board,positions,position,root):
	# finds the best ratio of negative to positive outcomes, and chooses the child node for the next process
	position_found = True
	temp_branch = 0
	while position_found:
		pos_ratio, neg_ratio = dict(), dict()
		for i in range(0,len(root.children)):
			neg_ratio[i] = countNegatives(root.children[i])
			pos_ratio[i] = countPositives(root.children[i])

		for key in neg_ratio:
			neg_ratio[key] = float(neg_ratio[key])/(neg_ratio[key]+pos_ratio[key])
		v = list(neg_ratio.values())
		k = list(neg_ratio.keys())
		temp_branch = k[v.index(max(v))]
		position = int(root.children[temp_branch].next_best_attribute)

		if board[position] == "o" or board[position] == "x":
			print "Position taken, try again computer."
			# del root.children[position]
			for i in range(0,len(board)):
				if i not in positions:
					position = i
					break
			yes,position_found = False, False
			return [position, root, yes]
		else:
			yes,position_found = False, False
			next_node = root.children[temp_branch]
			return [position, next_node, yes]

def computerMove(board,positions,training_data,root,turn):
	# computer makes a decision to put their mark
	yes = True
	position = 0
	next_node = root
	while yes:
		if turn == 1:
			position = int(root.next_best_attribute)
			yes = False
		elif turn == 3:
			win_loss = checkBoard(board)
			if win_loss[0]:
				position = win_loss[1]
				yes = False
			else:
				results = findBestBranch(board,positions,position,next_node)
				position = results[0]
				next_node = results[1]
				yes = results[2]
		elif turn == 5:
			win_loss = checkBoard(board)
			if win_loss[0]:
				position = win_loss[1]
				yes = False
			else:
				results = findBestBranch(board,positions,position,next_node)
				position = results[0]
				next_node = results[1]
				yes = results[2]
		elif turn == 7:
			win_loss = checkBoard(board)
			if win_loss[0]:
				position = win_loss[1]
				yes = False
			else:
			 	results = findBestBranch(board,positions,position,next_node)
				position = results[0]
				next_node = results[1]
				yes = results[2]
		else:
		 	for i in range(0,len(board)):
				if i not in positions:
					position = i
					yes = False
		
	positions.append(position)
	return position

def countNegatives(root):
	# recursively counts on the amount of negatives in a branch
	if root.next_best_attribute == "negative":	
		return 1
	elif root.next_best_attribute == "positive":
		return 0
	temp = 0
	for node in root.children:
		temp += countNegatives(node)
	return temp

def countPositives(root):
	# recursively counts all the positive outcomes in a branch
	if root.next_best_attribute == "negative":	
		return 0
	elif root.next_best_attribute == "positive":
		return 1
	temp = 0
	for node in root.children:
		temp += countPositives(node)
	return temp

def printBoard(board):
	# prints the positions, 0-9
	for i in range(0,9):
		if (i+1)%3==0:
			print i
		else: 
			print i,
	print

	# prints the presentation of the game board
	for i in range(0,9):
		if (i+1)%3==0:
			print board[i]
		else: 
			print board[i],
	print
	print "----------------"

def gameContinues(board):
	# checks to see if the game is won or loss
	if board[0] == board[1] and board[1] == board[2] and board[0]!="-":
		print "Player " + str(board[0]) + " wins"
		return False
	elif board[0] == board[3] and board[3] == board[6] and board[0]!="-":
		print "Player " + str(board[0]) + " wins"
		return False
	elif board[0] == board[4] and board[4] == board[8] and board[0]!="-":
		print "Player " + str(board[0]) + " wins"
		return False
	elif board[6] == board[7] and board[7] == board[8] and board[8]!="-":
		print "Player " + str(board[8]) + " wins"
		return False
	elif board[2] == board[5] and board[5] == board[8] and board[8]!="-":
		print "Player " + str(board[8]) + " wins"
		return False
	elif board[1] == board[4] and board[4] == board[7] and board[4]!="-":
		print "Player " + str(board[4]) + " wins"
		return False
	elif board[3] == board[4] and board[4] == board[5] and board[4]!="-":
		print "Player " + str(board[4]) + " wins"
		return False	

	return True

def checkBoard(board):
	end_game = [[0,4,8],[0,1,2],[0,3,6],[2,5,8],[6,7,8],[2,4,6],[3,4,5],[1,4,7]]
	method = dict()
	for path in end_game:
		if board[path[0]] == board[path[1]] and board[path[2]] == '-':
			method[board[path[0]]] = path[2]
		elif board[path[0]] == board[path[2]] and board[path[1]] == '-':
			method[board[path[0]]] = path[1]
		elif board[path[1]] == board[path[2]] and board[path[0]] == '-':
			method[board[path[1]]] = path[0]

	rand = random.randint(0,10)
	if 'x' in method and rand < 3:
		return [True, method['x']]
	elif 'o' in method and rand < 3:
		return [True, method['o']]
	else:
		return [False, 0]


class Node:
    def __init__(self, value_of_attribute, infogain, next_best_attribute, training_data):
    	self.training_data = training_data
        self.infogain = infogain
        self.value_of_attribute = value_of_attribute
        self.next_best_attribute = next_best_attribute
        self.training_data = training_data
        self.children = list()

if __name__== "__main__":

	# objects for class index, the class label, the attribute and value dict, and the infogain list
	training_data, validation_data, test_data, temp_training_data, all_infogain  = list(), list(), list(), list(), list()
	attributes = ["0","1","2","3","4","5","6","7","8","class"]
	class_index = -1
	label = attributes[class_index]
	att_val,class_num = dict(), dict()
	class_values = set()

	#set up root node, create the root, create the tree
	setupVariables(attributes, att_val, class_values)
	r_entr = findEntropy(training_data, class_values)
	infogain = findBestInfogain(training_data, r_entr, att_val, class_values, label)
	root = Node('Root', infogain[0], infogain[1], training_data)
	createTree(root)
	printDecisionTree(root)

	# set up game of chess. While loop for turns
	turn = 1
	board = ["-" for i in range(0,9)]
	positions = []
	printBoard(board)
	while turn < 10:
		if turn%2==0:
			board[playerMove(board,turn)] = "o"
			printBoard(board)
		else:
			board[computerMove(board,positions,training_data,root,turn)] = "x"
			printBoard(board)
		if gameContinues(board) == False:
			break
		turn += 1
		if turn == 10:
			print "Tied game."
