#Select Faces Polygonal Number.

class NumberDialog(MQWidget.Dialog):
	def minCheckCallback(self,sender):
		if self.minCheck.checked :
			self.minSpin.enabled = True
		else:
			self.minSpin.enabled = False
		if self.maxSpin.position < self.minSpin.position:
			self.minSpin.position = self.maxSpin.position
	def maxCheckCallback(self,sender):
		if self.maxCheck.checked :
			self.maxSpin.enabled = True
		else:
			self.maxSpin.enabled = False
		if self.maxSpin.position < self.minSpin.position:
			self.maxSpin.position = self.minSpin.position
	def minSpinCallback(self,sender):
		if self.maxCheck.checked :
			if self.minSpin.position > self.maxSpin.position:
				self.minSpin.position = self.maxSpin.position
	def maxSpinCallback(self,sender):
		if self.minCheck.checked :
			if self.maxSpin.position < self.minSpin.position:
				self.maxSpin.position = self.minSpin.position
				
	def __init__(self, parent):
		MQWidget.Dialog.__init__(self, parent)
		self.title = "Select n-sided polygon"
		
		self.frame0 = self.createHorizontalFrame(self)
		self.frame0.uniformSize = True
		
		self.tab = MQWidget.Tab (self.frame0)
		self.tab.currentPage = 0
		self.tab.setTabTitle(0,"Value")
		
		self.frame1 = self.createHorizontalFrame(self.tab)
		self.frame1.uniformSize = True
		
		self.numSpin = MQWidget.SpinBox(self.frame1)
		self.numSpin.min = 3
		self.numSpin.position = 3

		self.tab.currentPage = 1
		self.tab.setTabTitle(1,"Range")		
		
		self.frame2 = self.createVerticalFrame(self.tab)
		self.frame2.uniformSize = True
		
		self.frame3_0 = self.createHorizontalFrame(self.frame2)
		self.frame3_0.uniformSize = True
		
		self.minCheck = MQWidget.CheckBox(self.frame3_0)
		self.minCheck.text = "Min"
		self.minCheck.checked = True
		self.minSpin = MQWidget.SpinBox(self.frame3_0)
		self.minSpin.min = 3
		self.minSpin.position = 3
		
		self.frame3_1 = self.createHorizontalFrame(self.frame2)
		self.frame3_1.uniformSize = True
		
		self.maxCheck = MQWidget.CheckBox(self.frame3_1)
		self.maxCheck.text = "Max"
		self.maxCheck.checked = True
		self.maxSpin = MQWidget.SpinBox(self.frame3_1)
		self.maxSpin.min = 3
		self.maxSpin.position = 3
			
		self.minCheck.addChangedEvent(self.minCheckCallback)
		self.maxCheck.addChangedEvent(self.maxCheckCallback)
		self.minSpin.addChangingEvent(self.minSpinCallback)
		self.maxSpin.addChangingEvent(self.maxSpinCallback)
		
		self.frame4 = self.createHorizontalFrame(self)
		self.frame4.uniformSize = True
		self.okbtn = MQWidget.Button(self.frame4)
		self.okbtn.text = "OK"
		self.okbtn.modalResult = "ok"
		self.okbtn.default = 1
		self.okbtn.fillBeforeRate = 1
		self.cancelbtn = MQWidget.Button(self.frame4)
		self.cancelbtn.text = "Cancel"
		self.cancelbtn.modalResult = "cancel"
		self.cancelbtn.default = 1
		self.cancelbtn.fillAfterRate = 1
		
		
dlg = NumberDialog(MQWidget.getMainWindow())
if dlg.execute() == "ok":
	num = dlg.numSpin.position
	min	= dlg.minSpin.position
	max = dlg.maxSpin.position
	
	minCheck = dlg.minCheck.checked
	maxCheck = dlg.maxCheck.checked
	doc = MQSystem.getDocument()
	
	numObj = doc.numObject
	for oi in range(0,numObj):
		obj = doc.object[oi]
		if obj is None: continue
	
		numFace = obj.numFace
		
		#Select Faces Polygonal Number
		for fi in range(0, numFace):
			if dlg.tab.currentPage == 0:
				if obj.face[fi].numVertex == num :
					obj.face[fi].select = 1
				else:
					obj.face[fi].select = 0
			elif dlg.tab.currentPage == 1:
				if minCheck and maxCheck :
					if obj.face[fi].numVertex >= min and obj.face[fi].numVertex <= max :
						obj.face[fi].select = 1
					else:
						obj.face[fi].select = 0
				elif minCheck and not maxCheck :
					if obj.face[fi].numVertex >= min :
						obj.face[fi].select = 1
					else:
						obj.face[fi].select = 0
				elif not minCheck and maxCheck :
					if obj.face[fi].numVertex <= max :
						obj.face[fi].select = 1
					else:
						obj.face[fi].select = 0	