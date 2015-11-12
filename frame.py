''' Define a Frame Class '''

class Frame(object):

	def __init__(self, args):
		self.headers = args['headers']
		self.payload = args['payload']
		self.type = args['type']

	def __len__(self):
		''' Return the length of the frame '''
		return self.headers['length']

	def __str__(self):
		''' Return a string representation of the frame '''
		return self.__repr__()

	def __repr__(self):
		''' Return a string representation of the frame '''
		# TODO: Improve!
		return 'HTTP2 Frame of type %s' % str(self.type)