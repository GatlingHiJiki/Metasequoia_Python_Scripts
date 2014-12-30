# Subdivide faces uniformly.

def getVerticesOnEdge(obj, fi, li, edge_hash):
	apex = obj.face[fi].numVertex
	vi1 = min([obj.face[fi].index[li], obj.face[fi].index[(li+1)%apex]])
	vi2 = max([obj.face[fi].index[li], obj.face[fi].index[(li+1)%apex]])
	for i, vi in enumerate(edge_hash[vi1]):
		if vi[0] == vi2:
			e = []
			e.extend(edge_hash[vi1][i][1:])
			if vi2 == obj.face[fi].index[li]:
				e.reverse()
			return e
	return None

def createVerticesOnEdge(obj, fi, li, edge_hash):
	apex = obj.face[fi].numVertex
	vi1 = min([obj.face[fi].index[li], obj.face[fi].index[(li+1)%apex]])
	vi2 = max([obj.face[fi].index[li], obj.face[fi].index[(li+1)%apex]])
	for i, vi in enumerate(edge_hash[vi1]):
		if vi[0] == vi2:
			e = []
			e.extend(edge_hash[vi1][i][1:])
			if vi2 == obj.face[fi].index[li]:
				e.reverse()
			return e

	p1 = obj.vertex[vi1].getPos()
	p2 = obj.vertex[vi2].getPos()
	e = []
	e.append(vi2)
	for i in range(1,division):
		t = float(i) / float(division)
		nvi = obj.addVertex(p1 * (1-t) + p2 * t)
		e.append(nvi)
	edge_hash[vi1].append(e)
	e = e[1:]
	if vi2 == obj.face[fi].index[li]:
		e.reverse()
	return e


class NumberDialog(MQWidget.Dialog):
	def __init__(self, parent):
		MQWidget.Dialog.__init__(self, parent)
		self.title = MQSystem.getResourceString("MenuUniformDivide")
		self.frame1 = self.createHorizontalFrame(self)
		self.label = MQWidget.Label(self.frame1)
		self.label.text = MQSystem.getResourceString("MenuUniformDivide.Number")
		self.spin = MQWidget.SpinBox(self.frame1)
		self.spin.min = 2
		self.spin.max = 20
		self.spin.position = 2
		self.frame2 = self.createHorizontalFrame(self)
		self.frame2.uniformSize = True
		self.okbtn = MQWidget.Button(self.frame2)
		self.okbtn.text = MQSystem.getResourceString("OK")
		self.okbtn.modalResult = "ok"
		self.okbtn.default = 1
		self.okbtn.fillBeforeRate = 1
		self.cancelbtn = MQWidget.Button(self.frame2)
		self.cancelbtn.text = MQSystem.getResourceString("Cancel")
		self.cancelbtn.modalResult = "cancel"
		self.cancelbtn.default = 1
		self.cancelbtn.fillAfterRate = 1
		
dlg = NumberDialog(MQWidget.getMainWindow())
if dlg.execute() == "ok":
	division = dlg.spin.position
	
	doc = MQSystem.getDocument()
	
	num = doc.numObject
	for oi in range(0,num):
		obj = doc.object[oi]
		if obj is None: continue
	
		numFace = obj.numFace
		numVert = obj.numVertex
	
		edge_hash = []
		for x in range(numVert):
			edge_hash.append([])
	
		# Subdivide selected faces.
		for fi in range(0, numFace):
			apex = obj.face[fi].numVertex
			if apex >= 3 and doc.isSelectFace(oi, fi):
				if apex >= 5:
					# Add a center vertex.
					cp = MQSystem.newPoint(0,0,0)
					cc = MQSystem.newCoordinate(0,0)
					for n in range(apex):
						cp = cp + obj.vertex[obj.face[fi].index[n]].getPos()
						cc = cc + obj.face[fi].coord[n]
					cp = cp * (1/float(apex))
					cc = cc * (1/float(apex))
					cvi = obj.addVertex(cp)				
					# Add vertices between original vertex and center.
					ce = []
					for n in range(apex):
						vp = obj.vertex[obj.face[fi].index[n]].getPos()
						e = []
						for u in range(1,division):
							t = float(u) / float(division)
							vi = obj.addVertex(vp*(1-t) + cp*t)
							e.append(vi)
						ce.append(e)
					for n in range(apex):
						# Set up vertices for subdivided faces.
						en = createVerticesOnEdge(obj, fi, n, edge_hash)
						vert = []
						vert.append(obj.face[fi].index[n])
						vert.extend(createVerticesOnEdge(obj, fi, n, edge_hash))
						vert.append(obj.face[fi].index[(n+1)%apex])
						for v in range(1,division):
							vert.append(ce[n][v-1])
							for u in range(1,division-v):
								t = float(u) / float(division-v)
								vi = obj.addVertex(obj.vertex[ce[n][v-1]].getPos()*(1-t) + obj.vertex[ce[(n+1)%apex][v-1]].getPos()*t)
								vert.append(vi)
							vert.append(ce[(n+1)%apex][v-1])
							for u in range(v):
								vert.append(-1)
						vert.append(cvi)
						# Add subdivided faces.
						for v in range(division):
							dv0 = float(v) / float(division)
							dv1 = float(v+1) / float(division)
							for u in range(division-v):
								du00 = float(u) / float(division-v)
								du01 = float(u+1) / float(division-v)
								du10 = float(u) / float(max(1,division-v-1))
								du11 = float(u+1) / float(max(1,division-v-1))
								fvi = []
								fvi.append(vert[u+v*(division+1)])
								fvi.append(vert[u+1+v*(division+1)])
								fvi.append(vert[u+(v+1)*(division+1)])
								nfi = obj.addFace(fvi)
								obj.face[nfi].material = obj.face[fi].material
								obj.face[nfi].coord[0] = obj.face[fi].coord[n]*(1-du00)*(1-dv0) + obj.face[fi].coord[(n+1)%apex]*du00*(1-dv0) + cc*dv0
								obj.face[nfi].coord[1] = obj.face[fi].coord[n]*(1-du01)*(1-dv0) + obj.face[fi].coord[(n+1)%apex]*du01*(1-dv0) + cc*dv0
								obj.face[nfi].coord[2] = obj.face[fi].coord[n]*(1-du10)*(1-dv1) + obj.face[fi].coord[(n+1)%apex]*du10*(1-dv1) + cc*dv1
								doc.addSelectFace(oi, nfi)
								if u < division-v-1:
									fvi = []
									fvi.append(vert[u+1+v*(division+1)])
									fvi.append(vert[u+1+(v+1)*(division+1)])
									fvi.append(vert[u+(v+1)*(division+1)])
									nfi = obj.addFace(fvi)
									obj.face[nfi].material = obj.face[fi].material
									obj.face[nfi].coord[0] = obj.face[fi].coord[n]*(1-du01)*(1-dv0) + obj.face[fi].coord[(n+1)%apex]*du01*(1-dv0) + cc*dv0
									obj.face[nfi].coord[1] = obj.face[fi].coord[n]*(1-du11)*(1-dv1) + obj.face[fi].coord[(n+1)%apex]*du11*(1-dv1) + cc*dv1
									obj.face[nfi].coord[2] = obj.face[fi].coord[n]*(1-du10)*(1-dv1) + obj.face[fi].coord[(n+1)%apex]*du10*(1-dv1) + cc*dv1
									doc.addSelectFace(oi, nfi)
					obj.deleteFace(fi)
				elif apex == 4:
					# Set up vertices for subdivided faces.
					vert = []
					vert.append(obj.face[fi].index[0])
					vert.extend(createVerticesOnEdge(obj, fi, 0, edge_hash))
					vert.append(obj.face[fi].index[1])
					e1 = createVerticesOnEdge(obj, fi, 1, edge_hash)
					e3 = createVerticesOnEdge(obj, fi, 3, edge_hash)
					for v in range(1,division):
						vert.append(e3[division-v-1])
						for u in range(1,division):
							t = float(u) / float(division)
							nvi = obj.addVertex(obj.vertex[e3[division-v-1]].getPos()*(1-t) + obj.vertex[e1[v-1]].getPos()*t)
							vert.append(nvi)
						vert.append(e1[v-1])
					e2 = createVerticesOnEdge(obj, fi, 2, edge_hash)
					vert.append(obj.face[fi].index[3])
					for u in range(1,division):
						vert.append(e2[division-u-1])
					vert.append(obj.face[fi].index[2])				
					# Add subdivided faces.
					for v in range(division):
						dv0 = float(v) / float(division)
						dv1 = float(v+1) / float(division)
						for u in range(division):
							du0 = float(u) / float(division)
							du1 = float(u+1) / float(division)
							fvi = []
							fvi.append(vert[u+v*(division+1)])
							fvi.append(vert[u+1+v*(division+1)])
							fvi.append(vert[u+1+(v+1)*(division+1)])
							fvi.append(vert[u+(v+1)*(division+1)])
							nfi = obj.addFace(fvi)
							obj.face[nfi].material = obj.face[fi].material
							obj.face[nfi].coord[0] = (obj.face[fi].coord[0]*(1-du0) + obj.face[fi].coord[1]*du0)*(1-dv0) + (obj.face[fi].coord[3]*(1-du0)+obj.face[fi].coord[2]*du0)*dv0
							obj.face[nfi].coord[1] = (obj.face[fi].coord[0]*(1-du1) + obj.face[fi].coord[1]*du1)*(1-dv0) + (obj.face[fi].coord[3]*(1-du1)+obj.face[fi].coord[2]*du1)*dv0
							obj.face[nfi].coord[2] = (obj.face[fi].coord[0]*(1-du1) + obj.face[fi].coord[1]*du1)*(1-dv1) + (obj.face[fi].coord[3]*(1-du1)+obj.face[fi].coord[2]*du1)*dv1
							obj.face[nfi].coord[3] = (obj.face[fi].coord[0]*(1-du0)+obj.face[fi].coord[1]*du0)*(1-dv1) + (obj.face[fi].coord[3]*(1-du0)+obj.face[fi].coord[2]*du0)*dv1
							doc.addSelectFace(oi, nfi)
					obj.deleteFace(fi)
				elif apex == 3:
					# Set up vertices for subdivided faces.
					vert = []
					vert.append(obj.face[fi].index[0])
					vert.extend(createVerticesOnEdge(obj, fi, 0, edge_hash))
					vert.append(obj.face[fi].index[1])
					e1 = createVerticesOnEdge(obj, fi, 1, edge_hash)
					e2 = createVerticesOnEdge(obj, fi, 2, edge_hash)
					for v in range(1,division):
						vert.append(e2[division-v-1])
						for u in range(1,division-v):
							t = float(u) / float(division-v)
							vi = obj.addVertex(obj.vertex[e2[division-v-1]].getPos()*(1-t) + obj.vertex[e1[v-1]].getPos()*t)
							vert.append(vi)
						vert.append(e1[v-1])
						for u in range(v):
							vert.append(-1)
					vert.append(obj.face[fi].index[2])
					# Add subdivided faces.
					for v in range(division):
						dv0 = float(v) / float(division)
						dv1 = float(v+1) / float(division)
						for u in range(division-v):
							du00 = float(u) / float(division-v)
							du01 = float(u+1) / float(division-v)
							du10 = float(u) / float(max(1,division-v-1))
							du11 = float(u+1) / float(max(1,division-v-1))
							fvi = []
							fvi.append(vert[u+v*(division+1)])
							fvi.append(vert[u+1+v*(division+1)])
							fvi.append(vert[u+(v+1)*(division+1)])
							nfi = obj.addFace(fvi)
							obj.face[nfi].material = obj.face[fi].material
							obj.face[nfi].coord[0] = obj.face[fi].coord[0]*(1-du00)*(1-dv0)+obj.face[fi].coord[1]*du00*(1-dv0) + obj.face[fi].coord[2]*dv0
							obj.face[nfi].coord[1] = obj.face[fi].coord[0]*(1-du01)*(1-dv0)+obj.face[fi].coord[1]*du01*(1-dv0) + obj.face[fi].coord[2]*dv0
							obj.face[nfi].coord[2] = obj.face[fi].coord[0]*(1-du10)*(1-dv1)+obj.face[fi].coord[1]*du10*(1-dv1) + obj.face[fi].coord[2]*dv1
							doc.addSelectFace(oi, nfi)
							if u < division-v-1:
								fvi = []
								fvi.append(vert[u+1+v*(division+1)])
								fvi.append(vert[u+1+(v+1)*(division+1)])
								fvi.append(vert[u+(v+1)*(division+1)])
								nfi = obj.addFace(fvi)
								obj.face[nfi].material = obj.face[fi].material
								obj.face[nfi].coord[0] = obj.face[fi].coord[0]*(1-du01)*(1-dv0)+obj.face[fi].coord[1]*du01*(1-dv0) + obj.face[fi].coord[2]*dv0
								obj.face[nfi].coord[1] = obj.face[fi].coord[0]*(1-du11)*(1-dv1)+obj.face[fi].coord[1]*du11*(1-dv1) + obj.face[fi].coord[2]*dv1
								obj.face[nfi].coord[2] = obj.face[fi].coord[0]*(1-du10)*(1-dv1)+obj.face[fi].coord[1]*du10*(1-dv1) + obj.face[fi].coord[2]*dv1
								doc.addSelectFace(oi, nfi)
					obj.deleteFace(fi)
	
		# Modify neighbor faces.
		for fi in range(numFace):
			apex = obj.face[fi].numVertex
			if apex >= 3:
				vert = []
				coord = []
				for n in range(apex):
					vert.append(obj.face[fi].index[n])
					coord.append(obj.face[fi].coord[n])
					e = getVerticesOnEdge(obj, fi, n, edge_hash)
					if e is not None:
						vert.extend(e)
						for v in range(1,division):
							t = float(v) / float(division)
							coord.append(obj.face[fi].coord[n]*(1-t) + obj.face[fi].coord[(n+1)%apex]*t)
				if len(vert) > apex:
					nfi = obj.addFace(vert)
					obj.face[nfi].material = obj.face[fi].material
					for v in range(len(vert)):
						obj.face[nfi].coord[v] = coord[v]
					obj.deleteFace(fi)
