# example for separating selected vertices

doc = MQSystem.getDocument()

num = doc.numObject
for oi in range(0,num):
	obj = doc.object[oi]
	if obj is None: continue

	numFace = obj.numFace
	numVert = obj.numVertex

	# Enumurate selected vertices
	sel_vert = []
	for x in range(0,numVert):
		if obj.vertex[x].ref > 0 and obj.vertex[x].select:
			sel_vert.append(1)
		else:
			sel_vert.append(0)
	for x in range(0,numFace):
		if obj.face[x].numVertex >= 3:
			apex = obj.face[x].numVertex
			if obj.face[x].select:
				for y in range(0,apex):
					sel_vert[obj.face[x].index[y]] = 1
			else:
				for y in range(0,apex):
					if doc.isSelectLine(oi, x, y):
						sel_vert[obj.face[x].index[y]] = 1
						sel_vert[obj.face[x].index[(y+1)%apex]] = 1

	# Separate selected vertices
	del_face = []
	for x in range(0,numFace):
		if obj.face[x].numVertex >= 3:
			nvi = []
			newvi = 0
			for y in range(0,obj.face[x].numVertex):
				vi = obj.face[x].index[y]
				if sel_vert[vi]:
					p1 = obj.vertex[obj.face[x].index[y]].getPos()
					p2 = obj.vertex[obj.face[x].index[(y+1)%obj.face[x].numVertex]].getPos()
					p3 = obj.vertex[obj.face[x].index[(y+obj.face[x].numVertex-1)%obj.face[x].numVertex]].getPos()
					p = MQSystem.newPoint()
					p.x = p1.x * 0.9 + p2.x * 0.05 + p3.x * 0.05
					p.y = p1.y * 0.9 + p2.y * 0.05 + p3.y * 0.05
					p.z = p1.z * 0.9 + p2.z * 0.05 + p3.z * 0.05
					pvi = obj.addVertex(p)
					nvi.append(pvi)
					newvi = newvi + 1
				else:
					nvi.append(vi)
			if newvi > 0:
				nfi = obj.addFace(nvi)
				obj.face[nfi].material = obj.face[x].material
				for y in range(0,obj.face[x].numVertex):
					obj.face[nfi].coord[y] = obj.face[x].coord[y]
				del_face.append(x)

	# Delete original faces
	for x in del_face:
		obj.deleteFace(x)
