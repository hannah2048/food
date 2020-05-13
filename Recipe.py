import json

def init_dict():
	a = {}
	a["name"] = ""
	a["link"] = ""
	a["cuisine"] = ""
	a["tags"] = []
	a["ingredients"] = []
	a["instructions"] = []
	a["servings"] = ""
	a["nutrition"] = ""
	return a

class Recipe:
	def __init__(self,obj):
		self.name = obj["name"]
		self.link = obj["link"]
		self.cuisine = obj["cuisine"]
		self.tags = obj["tags"]
		self.ingredients = obj["ingredients"]
		self.instructions = obj["instructions"]
		self.servings = obj["servings"]
		self.nutrition = obj["nutrition"]

	def dumps(self,filep):
		return json.dump(self.__dict__,filep, indent=4)

	def __str__(self):
		return json.dumps(self.name)

	def __repr__(self):
		return str(self)

	def query(self,val):
		for i in self.ingredients:
			if val in i.lower():
				return True

		if val in self.name.lower():
			return True

		for i in self.tags:
			if val in i.lower():
				return True

		return False

def all_recipes():
	recps = []
	import glob
	files = glob.glob("recipe/*.json")
	for j in files:
		print(j)
		try:
			k = Recipe(json.load(open(j)))
		except:
			continue
		print("Loaded:" + j)
		recps += [k]

	return recps

def query(recps, val):
	lopi = []
	for j in recps:
		if j.query(val) == True:
			lopi += [j]
	return lopi


def query_vals(args,style):
	include = "+"
	exclude = "-"

	recps = all_recipes()

	if style == include:
		cur_recps = []
	else:
		cur_recps = recps

	print(style == include)

	for jo in args:
		if style == include:
			cur_recps += query(recps,jo)
		else:
			cur_recps = query(cur_recps,jo)

	return cur_recps

if __name__ == "__main__":
	import pdb,sys
	from pprint import pprint as p

	cur_recps = query_vals(sys.argv[2:],sys.argv[1])



# a = Recipe()
