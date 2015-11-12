import struct

from frame import Frame
from stream import Stream

class HTTP2Parser(object):
	''' Defines the Parser object '''
	def __init__(self, data):
		self.data = data
		self.streams = dict()

	def get_bytes(self, length):
		res = self.data[:length]
		self.data = self.data[length:]
		return res

	def parse_frame(self):
		''' Parse an HTTP/2 frame '''
		bin_frame_header = self.get_bytes(9)
		frame_header = Frame.parse_header(bin_frame_header)
		frame_body = struct.unpack(
			'c' * frame_header['length'],
			self.get_bytes(frame_header['length'])
		)

		# Create the frame object
		frame = Frame(frame_header, frame_body)

		# Create (and) or get the Stream object
		if not self.streams.has_key(frame_header['stream']):
			self.streams[frame_header['stream']] = Stream(frame_header['stream'])
		stream = self.streams[frame_header['stream']]

		stream.add_frame(frame)

		frame.print_info()

	def parse_data(self):
		''' Parse raw http packets '''
		idx = 0
		while len(self.data) > 0:
			if idx == 1:
				magic = self.get_bytes(24)
			else:
				self.parse_frame()
				print ''
			idx += 1



