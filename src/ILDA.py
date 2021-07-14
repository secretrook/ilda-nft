import struct

"""
ILDA Header Format:
  1-4:  "ILDA"
  5-7: 	Reserved
	  8: 	Format Code
 9-16: 	Frame or Color Palette Name
17-24:  Company Name
25-26: 	Number of Records
27-28: 	Frame or Color Palette Number
29-30:  Total Frames or 0
	 31:	Projector Number
	 32:	Reserved
"""
FORMAT_HEADER = struct.Struct('>7sB8s8s3H2B')

"""
Format 0: 3D Coordinates with Indexed Color
1-2:	X Coordinate 		7:	Status
3-4:	Y Coordinate 		8:	Color Index
5-6:	Z Coordinate
"""
FORMAT_0 = struct.Struct('>HHHbb')

"""
Format 1: 2D Coordinates with Indexed Color
1-2:	X Coordinate 		5:	Status Code
3-4: 	Y Coordinate 		6: 	Color Index
"""
FORMAT_1 = struct.Struct('>HHbb')

"""
Format 2: Color Palette
  1:	Red
  2:	Green
  3:	Blue
"""
FORMAT_2 = struct.Struct('>bbb')

"""
Format 4: 3D Coordinates with True Color
1-2: 	X Coordinate 			8: 	Blue
3-4:	Y Coordinate 			9:	Green
5-6:	Z Coordinate 		 10:	Red
  7:	Status Code
"""
FORMAT_4 = struct.Struct('>HHHbbbb')

"""
Format 5: 2D Coordinates with True Color
1-2:	X Coordinate 			6:	Blue
3-4:	Y Coordinate 			7:	Green
  5:	Status Code
"""
FORMAT_5 = struct.Struct('>HHbbbb')

# data record field names by format code
RECORD_FIELD_NAMES = {
	'0': ['x', 'y', 'z', 'status_code', 'color_index'],
	'1': ['x', 'y', 'status_code', 'color_index'],
	'2': ['r', 'g', 'b'],
	'4': ['x', 'y', 'z', 'status_code', 'b', 'g', 'r'],
	'5': ['x', 'y', 'status_code', 'b', 'g', 'r']
}

class ILDA_FILE:
	
	data_records = []
	
	def __init__(self, file_src):
		f = open(file_src, 'rb')
		
		while chunk := f.read(32):
			# unpack header information (first 32 bytes)
			data = FORMAT_HEADER.unpack(chunk)
			self.format_code = str(data[1])
			self.instance_name = data[2].decode('ascii')
			self.company_name = data[3].decode('ascii')
			self.n_records = data[4]
			self.instance_number = data[5]
			self.total_frames = data[6]
			self.projector_number = data[7]

			self.formatter = globals()['FORMAT_'+self.format_code]

			# get all data records
			field_names = RECORD_FIELD_NAMES[self.format_code]
			for _ in range(0, self.n_records):
				data = f.read(self.formatter.size)
				record = self.getRecord(data)
				self.data_records.append(record)
				
		f.close()

	def getRecord(self, data):
		return dict(zip(RECORD_FIELD_NAMES[self.format_code], self.formatter.unpack(data)))