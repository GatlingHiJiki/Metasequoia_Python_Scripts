import copy
#消す頂点郡を取得
	#ドキュメント取得
doc = MQSystem.getDocument()
	#全てのオブジェクトを取得
for oi in range(0,doc.numObject):
	obj = doc.object[oi]
	if obj is None: continue
	#選択されている頂点を取得
	for vi in range(0, obj.numVertex):
		vert = obj.vertex[vi]
		if vert is None: continue
		if vert.select == 1:
			#print(vi)
			#消す頂点が所属する面郡に所属する頂点郡を取得する
			#点の右隣を記憶する(削除点以外の）
			#点を２回以上通りうる
			vcount = 0
			vertDic = {}
			for fi in vert.faces:
				index = list()
				for i in obj.face[fi].index:
					index.append(i);
				for key in  range(0,len(index)):
					item = (key + 1) % len(index)
					if index[key] != vi and index[item] != vi:
						if(index[key] not in vertDic):
							vertDic[index[key]] = list()
							vertDic[index[key]].append(index[item])
						else:
							vertDic[index[key]].append(index[item])
						vcount += 1
			#この辞書を元にリストを作成
			#print(vertDic)
			vertLists = list([])
			keyList = list(vertDic.keys())
			for i in range(0,len(keyList)):
				vertLists.append(list([]))
				vertLists[i].append(keyList[i])
				j = 0
				tmpDic = copy.deepcopy(vertDic)
				while keyList[i] != tmpDic[vertLists[i][j]][0]:
					vertLists[i].append(tmpDic[vertLists[i][j]][0])
					tmpDic[vertLists[i][j]].pop(0)
					j += 1
					if not vertLists[i][j] in vertDic: break
					if tmpDic[vertLists[i][j]]:continue
					else:
						break
			#print(vertLists)
			def makeVertLists(vLists,kList,newLists):
				endFlag = False
				count = 0
				for key in kList:
					for newlist in newLists:
						for v in newlist:
							if key == v:
								count += 1
				if len(kList) != count:
					if(len(vLists) == 0):
						return
					max = 0
					for i in range(0,len(vLists)):
						if len(vLists[max]) < len(vLists[i]):
							max = i
					tmpList = vLists[max]
					bAppend = True
					for newList in newLists:
						for vi in newList:
							if vi in tmpList:
								bAppend = False;
					if bAppend :newLists.append(tmpList)
					if len(keyList)==len(tmpList):
						return
					vLists.pop(max)
					for tmp in tmpList:
						for i in range(0,len(vLists)-1):
							if len(vLists[i])> 0:
								if tmp == vLists[i][0]:
									vLists.pop(i)
					makeVertLists(vLists,kList,newLists)
			newLists = list([])		
			makeVertLists(vertLists,keyList,newLists)
			#print(newLists)
			#print(vcount)
			#新しく作る面の情報を適当に決める
			for vertList in newLists:
				#もし新しい面の一番後ろの点の辞書に登録されている次の点が無かったら選択頂点のコピーを加える
				copyvi = None
				if vertList[-1] not in vertDic or vertList[0] not in vertDic[vertList[-1]]:
					pos = vert.getPos()
					copyvi = obj.addVertex(pos.x,pos.y,pos.z)
					vertList.append(copyvi)
				newfi = obj.addFace(vertList)
				newFace = obj.face[newfi]
				newList = list(newFace.index)
				if copyvi is not None:
					#print(copyvi)
					oldFace = obj.face[vert.faces[0]]
					oldList = list(oldFace.index)
					copyfvi = newList.index(copyvi)
					fvi = oldList.index(vi)
					newFace.setCoord(copyfvi,oldFace.getCoord(fvi))
					newFace.setColor(copyfvi,oldFace.getColor(fvi))
					newFace.setAlpha(copyfvi,oldFace.getAlpha(fvi))
					newFace.setEdgeCrease(copyfvi,oldFace.getEdgeCrease(fvi))				
				newFace.material = obj.face[vert.faces[0]].material
				for newvi in newFace.index:
					for oldfi in vert.faces:
						oldFace = obj.face[oldfi]
						oldList = list(oldFace.index)
						for oldvi in oldFace.index:
							if oldvi == newvi:
								oldfvi = oldList.index(oldvi)
								if(oldList[(oldfvi+1)%len(oldList)] == vi):continue
								newfvi = newList.index(newvi)
								#print(vi)
								#print(oldList)
								#print(oldfvi)
								#print(newList)
								#print(newfvi)
								newFace.setCoord(newfvi,oldFace.getCoord(oldfvi))
								newFace.setColor(newfvi,oldFace.getColor(oldfvi))
								newFace.setAlpha(newfvi,oldFace.getAlpha(oldfvi))
								newFace.setEdgeCrease(newfvi,oldFace.getEdgeCrease(oldfvi))
								#print(oldFace.getEdgeCrease(oldfvi))
								#print(newFace.getEdgeCrease(newfvi))
								#print()
			for fi in vert.faces:
				obj.deleteFace(fi,1)
					
