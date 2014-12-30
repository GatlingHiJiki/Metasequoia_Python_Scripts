class PairValue:
	def __init__(self,face,line):
		self.face = face
		self.line = line

class EdgeTree:
	def __init__(self):
		self.pair = PairValue(-1,-1)
		self.next = -1

class EdgePair:
	def __init__(self,obj):
		self.obj = obj

		vert_count = obj.numVertex
		face_count = obj.numFace

		self.pair = []
		tree_size = vert_count
		for cf in range(face_count):
			self.pair.append([])
			cfc = obj.face[cf].numVertex
			if cfc >= 3:
				for k in range(cfc):
					self.pair[cf].append(PairValue(-1,-1))
				tree_size = tree_size + cfc

		tree = []
		for cf in range(tree_size):
			tree.append(EdgeTree())

		regvc = vert_count;
		for cf in range(face_count):
			cfc = obj.face[cf].numVertex
			if cfc < 3:
				continue

			for k in range(cfc):
				self.pair[cf].append(-1)

			cvi = obj.face[cf].index
			cfc = cfc-1
			for j in range(cfc+1):
				v1 = cvi[j];
				if j < cfc:
					v2 = cvi[j+1]
				else:
					v2 = cvi[0]
				done = 0
				drel = tree[v2]
				while True:
					if drel.pair.face < 0:
						break

					df = drel.pair.face
					dfc = obj.face[df].numVertex
					dvi = obj.face[df].index
					if self.pair[df][drel.pair.line].face < 0:
						if drel.pair.line<dfc-1:
							l = drel.pair.line+1
						else:
							l = 0
						if v1 == dvi[l]:
							self.pair[df][drel.pair.line] = PairValue(cf,j)
							self.pair[cf][j] = drel.pair
							done = 1
							break
					if drel.next < 0:
						break

					drel = tree[drel.next]

				if done == 0:
					ctr = tree[v1]
					while True:
						if ctr.pair.face < 0:
							break
						if ctr.next < 0:
							ctr.next = regvc
							ctr = tree[regvc]
							regvc = regvc + 1
							break
						ctr = tree[ctr.next]

					ctr.pair = PairValue(cf,j)

	def getPair(self, face_index, line_index):
		if face_index >= len(self.pair):
			return None
		if self.pair[face_index][line_index].face < 0:
			return None
		return PairValue(self.pair[face_index][line_index].face, self.pair[face_index][line_index].line)


def isLineSelected(doc, pair, obj_idx, face, line):
	if doc.isSelectLine(obj_idx, face, line):
		return True
	p = pair.getPair(face, line)
	if p is None:
		return False
	else:
		return doc.isSelectLine(obj_idx, p.face, p.line)


doc = MQSystem.getDocument()
num = doc.numObject
for oi in range(0,num):
	obj = doc.object[oi]
	if obj is None: continue

	pair = EdgePair(obj)
	numFace = obj.numFace
	numVert = obj.numVertex

	delarray = []
	for fi in range(numFace):
		num = obj.face[fi].numVertex
		delf = 0
		if num >= 3:
			if doc.isSelectFace(oi, fi):
				for j in range(num):
					p = pair.getPair(fi, j)
					if p is None:
						fvi = [obj.face[fi].index[j], obj.face[fi].index[(j+1)%num]]
						nfi = obj.addFace(fvi)
						doc.addSelectLine(oi, nfi, 0)
						delf = 1
			else:
				for j in range(num):
					p = pair.getPair(fi, j)
					if doc.isSelectLine(oi, fi, j) or (p is not None and doc.isSelectLine(oi, p.face, p.line)):
						fvi = [obj.face[fi].index[j], obj.face[fi].index[(j+1)%num]]
						delf = 1
						overlap = 0
						for k in obj.vertex[fvi[0]].faces:
							if obj.face[k].numVertex == 2:
								if (obj.face[k].index[0] == fvi[0] and obj.face[k].index[1] == fvi[1]):
									overlap = 1
								if (obj.face[k].index[0] == fvi[1] and obj.face[k].index[1] == fvi[0]):
									overlap = 1
						if overlap == 0:
							nfi = obj.addFace(fvi)
							doc.addSelectLine(oi, nfi, 0)
		delarray.append(delf)
	for fi in range(numFace):
		if delarray[fi]:
			obj.deleteFace(fi, 1)
