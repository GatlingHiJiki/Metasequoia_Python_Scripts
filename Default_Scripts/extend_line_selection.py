
doc = MQSystem.getDocument()

num = doc.numObject
for oi in range(0,num):
	obj = doc.object[oi]
	if obj is None: continue

	numFace = obj.numFace
	
	sel = []

	# Enum selected lines.
	for fi in range(numFace):
		apex = obj.face[fi].numVertex
		if apex == 2 and doc.isSelectLine(oi, fi, 0):
			sel.append(fi)
			
	for fi in sel:
		for j in range(2):
			nfaces = obj.vertex[obj.face[fi].index[j]].faces
			for nfi in nfaces:
				if nfi != fi and obj.face[nfi].numVertex == 2 and doc.isSelectLine(oi, nfi, 0) == 0:
					doc.addSelectLine(oi, nfi, 0)
					sel.append(nfi)
