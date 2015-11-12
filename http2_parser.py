import struct

FRAME_TYPES = {
	0x0 : 'DATA',
	0x1 : 'HEADERS',
	0x2 : 'PRIORITY',
	0x3 : 'RST_STREAM',
	0x4 : 'SETTINGS',
	0x5 : 'PUSH_PROMISE',
	0x6 : 'PING',
	0x7 : 'GOAWAY',
	0x8 : 'WINDOW_UPDATE',
	0x9 : 'CONTINUATION'
}

response_data = dict()

def bits_to_int(bytes):
	''' Convert an array of bits to an integer value '''
	res = 0
	for idx, bit in enumerate(bytes):
		res += (2 ** idx) * bit
	return res


def get_bytes(length):
	''' Chop the first length-bytes from data and return 'em '''
	global data
	res = data[:length]
	data = data[length:]
	return res

def parse_stream(stream_data):
	''' Parse the Stream ID '''
	bits = []
	for byte in stream_data:
		for i in xrange(8):
			bits.append((ord(byte) >> i) & 1)
	# Get rid of the reserved bit
	bits.pop(-1)
	return bits_to_int(bits)


def parse_header(header, should_print=True):
	''' Parse the header of the packet '''
	frame_length = sum(struct.unpack('hB', header[:3]))
	if frame_length == 1702:
		print struct.unpack('hb', header[:3])
	header = header[3:]
	frame_type = FRAME_TYPES.get(
		struct.unpack('b', header[:1])[0],
		'ERROR'
	)
	header = header[1:]
	frame_flags = struct.unpack('b', header[:1])[0]
	header = header[1:]
	frame_stream = struct.unpack('cccc', header[:4])[::-1]
	stream_id = parse_stream(frame_stream)
	if should_print:
		print 'Frame Length: %s' % str(frame_length)
		print 'Frame Type: %s' % str(frame_type)
		print 'Flags: %s' % format(frame_flags, '#010b')
		print 'Stream ID: %i' % stream_id
	return frame_type, frame_length, stream_id

def parse_frame(should_print=True):
	''' Parse an HTTP/2 frame '''
	header = get_bytes(9)
	frame_type, body_length, stream_id = parse_header(header, should_print)
	body = struct.unpack('c' * body_length, get_bytes(body_length))
	if frame_type == 'DATA':
		response_data[stream_id] = response_data.get(stream_id, '') + ''.join(body)


def parse_data():
	''' Parse raw http packets '''
	idx = 0
	while len(data) > 0:
		if idx == 1:
			magic = get_bytes(24)
		else:
			parse_frame()
			print ''
		idx += 1

def main(filename):
	global data
	with open(filename, 'r') as file:
		data = file.read()

	parse_data()

if __name__ == '__main__':
	main('http2_raw.txt')