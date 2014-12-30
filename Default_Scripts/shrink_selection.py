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

	# Shrink vertex selection.
	selarray = []
	for vi in range(numVert):
		if obj.vertex[vi].ref > 0:
			selarray.append(doc.isSelectVertex(oi, vi))
		else:
			selarray.append(0)
	for fi in range(numFace):
		num = obj.face[fi].numVertex
		if num >= 3:
			for j in range(num):
				if selarray[obj.face[fi].index[j]] != 0:
					nvi1 = obj.face[fi].index[(j+1)%num]
					nvi2 = obj.face[fi].index[(j+num-1)%num]
					if selarray[nvi1] == 0 or selarray[nvi2] == 0:
						doc.deleteSelectVertex(oi, obj.face[fi].index[j])

	# Shrink face selection.
	selarray = []
	for fi in range(numFace):
		num = obj.face[fi].numVertex
		if num >= 3:
			selarray.append(doc.isSelectFace(oi, fi))
		else:
			selarray.append(0)
	
	for fi in range(numFace):
		if selarray[fi] != 0:
			num = obj.face[fi].numVertex
			for j in range(num):
				p = pair.getPair(fi, j)
				if p is not None and selarray[p.face] == 0:
					doc.deleteSelectFace(oi, fi)
					break

