import asyncio
import scene
import ui

def YARITAIKOTO():
	# 初期化
	gm = GameManager()
	
	while(True):
		# タイトルシーンを開始
		ret = gm.Show(TitleScene())
		
		# ゲームシーンを開始
		ret = gm.Show(GameScene())
		
		# タイトルシーンに戻る

def fit_to_size(node, target):
	'''nodeのスケールをtargetのサイズになるように調整する'''
	# 現状期待した動きをしていない。。。
	
	#node.x_scale = target.frame.width / node.frame.width
	#node.y_scale = target.frame.height / node.frame.height
	node.x_scale = target.size.w / node.size.w
	node.y_scale = target.size.h / node.size.h
	#print(node.x_scale)
	#print(dir(target.frame))

class TitleScene(scene.Scene):
	def __init__(self, gm):
		self.gm = gm
		self.evt_tapped = asyncio.Event()
		self.nodes = []
		
	def touch_began(self, touched):
		print('touch_began called.')
		self.set_tapped()
		
	def touch_moved(self, node, touch):
		print('touch moved')
		
	def touch_ended(self, node, touch):
		print('touch ended.')
		
	def update(self):
		print('update')
		
	def get_root(self):
		return self.gm.get_rootpyscene()
	
	def add_child(self, node):
		root = self.get_root()
		root.add_child(node)
		self.nodes.append(node)
		
	async def init(self):
		root = self.get_root()
		
		ssize = scene.get_screen_size()
		sscale = scene.get_screen_scale()
		pnt_center = scene.Point(ssize.x / 2, ssize.y / 2)
		
		## Background
		#bg = scene.SpriteNode('plf:BG_Colored_land')
		#fit_to_size(bg, root)
		bg = scene.ShapeNode()
		bg.path = ui.Path.rect(0,0,ssize.w,ssize.h)
		bg.x_scale = sscale
		bg.y_scale = sscale
		bg.fill_color = 'green'
		#bg.touch_began = self.touch_began
		self.add_child(bg)
		
		## Title logo
		logo = scene.LabelNode()
		logo.text = 'Pong Solo'
		logo.position = pnt_center + scene.Point(0, 200)
		self.add_child(logo)
	
	async def term(self):
		for node in self.nodes:
			node.remove_from_parent()
		self.nodes = []
		
	async def show(self):
		await self.init()
		#await self.wait_tapped()
		#await self.term()
		
		return 0
		
	async def wait_tapped(self):
		self.evt_tapped.clear()
		await self.evt_tapped.wait()
		
	def set_tapped(self):
		self.evt_tapped.set()
		pass


class RootPyScene(scene.Scene):
	def setup(self):
		self.background_color = 'blue'


class GameManager():
	def __init__(self):
		self.rootpyscene = None
		
	def get_rootpyscene(self):
		return self.rootpyscene
	
	async def init(self):
		self.rootpyscene = RootPyScene()
		scene.run(self.rootpyscene)
		
	async def show(self, scene):
		ret = await scene.show()
		return ret
		
	async def main_loop(self):
		print('main_loop began')
		
		# 初期化
		await self.init()
		
		# タイトル
		title = TitleScene(self)
		ret = await self.show(title)
		print(f'ret is {ret}')
		
		print('main_loop finish.')

	def start_main_loop(self):
		#loop = asyncio.get_event_loop()
		loop = asyncio.get_event_loop_policy().new_event_loop()
		loop.run_until_complete(self.main_loop())
		loop.close()		

def main():
	print('start')
	GameManager().start_main_loop()
	print('finish')

if '__main__' == __name__:
	main()


