def bits_to_int(bytes):
	''' Convert an array of bits to an integer value '''
	res = 0
	for idx, bit in enumerate(bytes):
		res += (2 ** idx) * bit
	return res