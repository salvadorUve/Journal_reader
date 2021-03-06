"""This module contains code from
a small Student project by Salvador Vigo

Copyright 2017 Salvador Vigo

"""

# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys
import re
import os #we use os to open a txt file and show the results

def list_maker(soup):
	"""Read the HTML file and leak the keywords making a list
	of tuples
	"""
	pattern = re.compile(r'>((([a-zA-Z]{2,})\s){2,}(\w{2,}){2,})<')
	word_list = pattern.findall(str(soup))
	return(word_list)

def unpacking_tuples(soup):
	word_list = list_maker(soup)
	keys = []
	for item in word_list:
		a, b, c, d = item
		keys.append(a)
	return keys

def packing_words(soup):
	"""Paking words from tuples in a new list of words, ready
	to make a dictionary"""
	list_from_tuples = unpacking_tuples(soup)
	final_list = list()
	for i in range(len(list_from_tuples)):
		res = list(list_from_tuples[i].split())
		for i in range(len(res)):
			if len(res[i]) > 3:
				final_list.append(res[i])
	return final_list

def invert_dict(d):
	"""invert a dictionary
	"""
	reverse = dict()
	for key in d:
		val = d[key]
		if val not in reverse:
			reverse[val] = [key]
		else:
			reverse[val].append(key)
	return reverse

def dict_maker(soup):
	"""Make a histogram
	"""
	d = dict()
	for c in packing_words(soup):
		d[c] = 1 + d.get(c, 0)
	return d

def most_frequent(soup):
	"""Start a dictionary and sort the words for frequency"""
	histo_dict = dict_maker(soup)
	invert_dicti = sorted(invert_dict(histo_dict).items())
	list_mfreq = []
	for key, value in invert_dicti:
		list_mfreq.append(sorted(value))
	return list_mfreq

def printer(list_mfreq):
	"""Prepare all elements to be printed"""
	text1 = ", ".join(list_mfreq[0])
	text2 = ", ".join(list_mfreq[1])
	try:		
		text3 = ", ".join(list_mfreq[2])
	except:
		making_text = ("Common words #1: \n %s " % text1 + "\n\n" + 
		"Common words #2: \n %s " % text2 + "\n\n")
	else:
		making_text = ("Common words #1: \n %s " % text1 + "\n\n" + 
		"Common words #2: \n %s " % text2 + "\n\n" + "Common words #3: \n %s"
		 % text3)

	return making_text

def start(soup):
	"""Introduce a input variable and use the options. It also open a 
	.txt file to show the results"""
	cwd = os.getcwd()
	intro = input("Hi! this is a Headline reader which analyze the most "+
		"common words in 4 different Newspaper. If you want all keywords"+
		" together press 'y'. Otherwise you prefer keywords one by one,"  + 
		" press '1' for El Mundo, '2' for El pais, '3' for Publico or '4'"+
		" for Abc:")
	if intro == "y":
		data = printer(most_frequent(soup))
		fout = open(cwd + '\Key_words.txt', 'w')
		fout.write("ALL KEYWORDS \n\n" + data)
		fout.close()
		os.startfile('Key_words.txt')
	if intro == "1":
		data = printer(most_frequent(soup[0]))
		fout = open(cwd + '\Key_words.txt', 'w')
		fout.write("EL MUNDO KEYWORDS \n\n" + data)
		fout.close()
		os.startfile('Key_words.txt')
	if intro == "2":
		data = printer(most_frequent(soup[1]))
		fout = open(cwd + '\Key_words.txt', 'w')
		fout.write("EL PAIS KEYWORDS \n\n" + data)
		fout.close()
		os.startfile('Key_words.txt')
	if intro == "3":
		data = printer(most_frequent(soup[2]))
		fout = open(cwd + '\Key_words.txt', 'w')
		fout.write("PUBLICO KEYWORDS \n\n" + data)
		fout.close()
		os.startfile('Key_words.txt')
	if intro == "4":
		data = printer(most_frequent(soup[3]))
		fout = open(cwd + '\Key_words.txt', 'w')
		fout.write("ABC KEYWORDS \n\n" + data)
		fout.close()
		os.startfile('Key_words.txt')
	
def main(name, webname1="http://www.elmundo.es/", 
	webname2="http://elpais.com/", webname3="http://www.publico.es/", 
	webname4="http://www.abc.es/"):
	
	cwd = os.getcwd()

	req1 = requests.get(webname1)
	req2 = requests.get(webname2)
	req3 = requests.get(webname3)
	req4 = requests.get(webname4)

	statusCode = req1.status_code

	# check Status Code = 200
	status_code = req1.status_code

	if status_code == 200:
		soup = (BeautifulSoup(req1.text, "html.parser"), 
			BeautifulSoup(req2.text, "html.parser"), 
			BeautifulSoup(req3.text, "html.parser"), 
			BeautifulSoup(req4.text, "html.parser"))

		start(soup)

	else:
		print("Status Code %d" % status_code)


if __name__ == '__main__':
	main(*sys.argv)