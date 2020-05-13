from bs4 import BeautifulSoup
import sys
from Recipe import *

def get_url(url):
	from urllib.request import Request, urlopen
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(req)
	data = response.read()      # a `bytes` object
	text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
	return text

def javascript_parse(doc,site):
	if site == "minibaker":
		classname = 'yoast-schema-graph yoast-schema-graph--main'
	elif site == "simplyquinoa":
		classname = 'yoast-schema-graph'

	soup = BeautifulSoup(doc,features="html.parser")
	obj = init_dict()

	hit = soup.find(attrs={'class' : classname})
	hit = eval(hit.text)

	for c,i in enumerate(hit['@graph']):
		if 'recipeIngredient' in i.keys():
			j = hit['@graph'][c]

	name = j['name'].replace("/","")
	obj["name"] = name
	print(name)

	fp = "recipe/"+name+".json"
	filep = open(fp,"w+")

	print("ingredients: \n")
	ingredients = j['recipeIngredient']

	obj["ingredients"] = []
	for i in ingredients:
		print(i)
		obj["ingredients"] += [i]
	
	print("instructions: \n")
	instructions = j['recipeInstructions']

	obj["instructions"] = []
	for i in instructions:
		i = i['text']
		print(i)
		obj["instructions"] += [i]

	obj["tags"] = input("Enter tags in comma seperated list: ").split(",")
	a = Recipe(obj)
	a.dumps(filep)


def oldschool_parse(doc,site):
	if site == "fitfoodiefinds":
		ingredients_name = 'tasty-recipe-ingredients'
		instructions_name = 'tasty-recipe-instructions'
	elif site == "damndelicious":
		ingredients_name = 'ingredients'
		instructions_name = 'instructions'

	obj = init_dict()
	soup = BeautifulSoup(''.join(doc),features="html.parser")

	title = soup.title.text.replace("/","")
	obj["name"] = title
	print("\n\n"+obj["name"])

	fp = "recipe/"+title+".json"
	filep = open(fp,"w+")

	ingredients = ""
	hhh = soup.find(attrs={'class' : instructions_name})
	instructions = hhh.findAll('li')
	hhh = soup.find(attrs={'class' : ingredients_name})
	ingredients = hhh.findAll('li')

	print("instructions:")
	obj["instructions"] = []
	for i in instructions:
		i = i.text
		i = i.replace("<li>","")
		i =  i.replace("</li>","")
		print(i)
		obj["instructions"] += [i]

	print("ingredients:")
	obj["ingredients"] = []
	for i in ingredients:
		print(i.text)
		obj["ingredients"] += [i.text]

	obj["tags"] = input("Enter tags in comma seperated list: ").split(",")

	a = Recipe(obj)
	a.dumps(filep)

if __name__ == "__main__":

	ss = sys.argv[1]
	if "fitfoodiefinds" in ss:
		text = get_url(ss)
		oldschool_parse(text,"fitfoodiefinds")
	elif "minimalist" in ss:
		text = get_url(ss)
		javascript_parse(text,"minibaker")
	elif "simplyquinoa" in ss:
		text = get_url(ss)
		javascript_parse(text,"simplyquinoa")
	elif "damndelicious" in ss:
		text = get_url(ss)
		oldschool_parse(text,"damndelicious")
	else:
		text = open(ss).read()

	
