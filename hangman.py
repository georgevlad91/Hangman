### python hangman game ###
import random
from datetime import date
import requests
from bs4 import BeautifulSoup
import unidecode

def random_date():
	year = random.randint(2014, date.today().year)
	month = random.randint(1, 12)
	day = random.randint(1, 28)
	ran_date = (date(year, month, day).strftime('%Y/%m/%d'))
	#date = str(year) + '/' + str(month) + '/' + str(day)
	return ran_date

def get_word():
	my_url = 'https://dexonline.ro/cuvantul-zilei/' + random_date()
	page = requests.get(my_url)
	soup = BeautifulSoup(page.text, 'html.parser')
	word = soup.find('b').text.strip(',')
	return word
	
### designs ###
	
def design1():
	des = """
	
	_________
	|/     | 
	|    (._.)     
	|               
	|                 
	|               
	|                   
	|___   
	"""
	print(des)

def design2():
	des = """
		
	_________
	|/     |        
	|    (._.)          
	|      |           
	|      |         
	| 
	|	 
	|___   
	"""
	print(des)

def design3():
	des = """
	
	_________
	|/     |        
	|    (._.)          
	|      |           
	|     /|         
	|  
	| 
	|___   
	"""
	print(des)

def design4():
	des = """
	
	_________
	/     |        
	|    (._.)          
	|      |           
	|     /|\         
	|  
	| 
	|___   
	"""
	print(des)

def design5():
	des = """
	
	_________
	|/     |        
	|    (._.)       
	|      |     
	|     /|\       
	|     /           
	|
	|___   
	"""
	print(des)

def design6():
	des = """
	
	_________
	|/     |        
	|    (o_o)       
	|      |     
	|     /|\       
	|     / \          
	|
	|___   
	"""
	print(des)


def design7():
	des = """	
	_________
	|/     |      
	|    (x_x)      
	|      |     
	|     /|\       
	|     / \          
	|
	|___   
	GAME OVER!
	"""
	print(des)

design = {1:design1, \
		2:design2, \
		3:design3, \
		4:design4, \
		5:design5, \
		6:design6, \
		7:design7
}
	
print ("Welcome to hangman!\n")

name = input("Type your name: \n")

print ("Hi {}, let's play hangman\n".format(name))
word =  unidecode.unidecode(get_word()).upper()
word_len = len(word)
word_to_guess = '*' * word_len

print("Next word is: " + word_to_guess)

guesses = 0
missed_guess = 0
new_guessed = ''

while (missed_guess < 7):
	guess = input("\nType a letter:\n").upper()
	if guess in word:
		print("Correct! '{}' is found in the word\n".format(guess))
		new_guessed = ''
		for index,i in enumerate(word):
			if guess == i:
				new_guessed += i
			else:
				new_guessed += word_to_guess[index]
		word_to_guess = new_guessed
		print(word_to_guess)
	else:
		print("Oups! Wrong letter.. Try again!")
		missed_guess += 1
		design[missed_guess]() 
		
	if '*' not in word_to_guess:
		print("\nYay! You won!\n")
		break
else:	
	print("Out of chances. You lost!")		
	print("The word was: " + word)