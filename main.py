from parser import HTTP2Parser

def main(filename):
	with open(filename, 'r') as file:
		data = file.read()

	h2_parser = HTTP2Parser(data)
	h2_parser.parse_data()

if __name__ == '__main__':
	main('http2_raw.txt')