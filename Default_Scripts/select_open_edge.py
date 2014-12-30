class EdgeTypeDialog(MQWidget.Dialog):
	def radioCallback(self,sender):
		self.radio1.checked = (sender == self.radio1)
		self.radio2.checked = (sender == self.radio2)
		self.radio3.checked = (sender == self.radio3)
		self.okbtn.enabled = True

	def __init__(self, parent):
		MQWidget.Dialog.__init__(self, parent)
		self.title = "Select open edge"

		self.radio1 = MQWidget.RadioButton(self)
		self.radio1.text = "Edge"
		self.radio1.addChangedEvent(self.radioCallback)
		self.radio2 = MQWidget.RadioButton(self)
		self.radio2.text = "UV edge"
		self.radio2.addChangedEvent(self.radioCallback)
		self.radio3 = MQWidget.RadioButton(self)
		self.radio3.text = "Material"
		self.radio3.addChangedEvent(self.radioCallback)
		self.frame2 = self.createHorizontalFrame(self)
		self.frame2.uniformSize = True
		self.okbtn = MQWidget.Button(self.frame2)
		self.okbtn.text = "OK"
		self.okbtn.modalResult = "ok"
		self.okbtn.default = 1
		self.okbtn.fillBeforeRate = 1
		self.okbtn.enabled = False
		self.cancelbtn = MQWidget.Button(self.frame2)
		self.cancelbtn.text = "Cancel"
		self.cancelbtn.modalResult = "cancel"
		self.cancelbtn.default = 1
		self.cancelbtn.fillAfterRate = 1


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

dlg = EdgeTypeDialog(MQWidget.getMainWindow())
if dlg.execute() == "ok":
	type = 0
	if dlg.radio1.checked: type = 1
	if dlg.radio2.checked: type = 2
	if dlg.radio3.checked: type = 3

	num = doc.numObject
	for oi in range(0,num):
		obj = doc.object[oi]
		if obj is None: continue

		pair = EdgePair(obj)
		numFace = obj.numFace

		for fi in range(numFace):
			num = obj.face[fi].numVertex
			if num < 3: continue
			for li in range(num):
				p = pair.getPair(fi, li)
				if p is None:
					if type == 1:
						doc.addSelectLine(oi, fi, li)
				else:
					if type == 2 and obj.face[fi].coord[li] != obj.face[p.face].coord[(p.line+1)%obj.face[p.face].numVertex]:
						doc.addSelectLine(oi, fi, li)
					elif type == 3 and obj.face[fi].material != obj.face[p.face].material:
						doc.addSelectLine(oi, fi, li)
