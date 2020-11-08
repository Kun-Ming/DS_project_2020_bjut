import shutil
from PySide2.QtWidgets import QMessageBox


class read_course:
	def read(self, path='../data/course_private.txt'):
		self.target = []
		self.target_point = []
		self.base = []
		self.base_point = []
		self.pre = []
		with open(path, 'r') as f:
			if path != '../data/course_private.txt':
				shutil.copy(path, '../data/course_private.txt')
			for line in f:
				if line == '\n':
					continue
				if line[0] != '\t':  # target course or base course
					line = line.rstrip('\n')

					if line[-1] == ':' or line[-1] == '：':  # target course
						self.target.append(line.split(" ")[0])
						self.target_point.append(float(line.split(" ")[1][:-1]))
					else:  # base course
						# print(line)
						if len(line.split(" ")[1]) != []:
							self.base.append(line.split(" ")[0])
							self.base_point.append(float(line.split(" ")[1]))
						else:
							return [False, 'NO CREDIT IN COURSE:\n' + line.split(" ")[0]]

				else:  # prerequisite course
					line = line[1:-1]
					self.pre.append(line.split(" "))

		# verifying data
		# pre should all in base and target
		# target should totally different to base
		if len([i for i in self.target if i in self.base]):  # compare target to base
			res = [i for i in self.target if i in self.base]
			res = ' '.join([str(j) for j in res])
			return [False, 'WRONG in course ' + res + ': \nAPPEAR IN TARGET AND BASE']
		if len([j for j in [i for i in [x for y in self.pre for x in y] if i not in self.base]
				if j not in self.target]):  # compare pre to base and target
			res = [j for j in [i for i in [x for y in self.pre for x in y] if i not in self.base] if
				   j not in self.target]
			res = ' '.join([str(j) for j in res])
			return [False, 'WRONG in course ' + res + ': \nNOT FOUND IN TARGET OR BASE COURSE']
		else:
			return [True, True]

	def write(self, target, target_point, base, base_point, pre):
		with open('../data/course_private.txt', 'a') as f:
			if len(target):
				f.write('\n')
				string = target + ' ' + target_point + ':\n'
				print(string)
				f.write(string)
				string = '\t' + ' '.join([str(j) for j in pre]) + '\n'
				f.write(string)
			if len(base):
				f.write('\n')
				string = base + ' ' + base_point + '\n'
				f.write(string)

	def del_target(self):
		with open('../data/course_private.txt', 'r') as f:
			lines = f.readlines()
			del lines[-1]
			del lines[-1]
		with open('../data/course_private.txt', 'w') as f:
			for s in lines:
				f.write(s)

	def del_base(self):
		with open('../data/course_private.txt', 'r') as f:
			lines = f.readlines()
			del lines[-1]
		with open('../data/course_private.txt', 'w') as f:
			for s in lines:
				f.write(s)


def get_course_info():
	file_reader = read_course()
	if file_reader.read('../data/course_private.txt')[0]:
		res = file_reader.target + file_reader.base
		res_point = file_reader.target_point + file_reader.base_point
		data = dict()
		for i in range(0, len(res)):
			data[str(res[i])] = [0, res_point[i]]
		return data, file_reader.target, file_reader.target_point, \
			   file_reader.base, file_reader.base_point, file_reader.pre


if __name__ == "__main__":
	reader = read_course()
# reader.del_base()
