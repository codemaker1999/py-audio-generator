notes = [("c4",261.63),("d4",293.66),("e4",329.63)]
data = [.03, .233, .76]

def process(data):
	#...
#	notes = convert_data(data)
	result = []
	for num in data:
		# convert to freq between 0 and 10000 hz
		f = num*10000
		result.append( (f, 0.0) )
	# output [(freq, dB), ...]
	return result

print process(data)

	