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

class TitleScene():
	def __init__(self, gm):
		self.gm = gm
		self.is_tapped = False
		
	def touch_began(self, touched):
		self.is_tapped = True
		
	def get_root(self):
		return self.gm.get_rootpyscene()
		
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
		root.add_child(bg)
		
		## Title logo
		logo = scene.LabelNode()
		logo.text = 'Pong Solo'
		logo.position = pnt_center + scene.Point(0, 200)
		root.add_child(logo)
		
		##
		self.is_tapped = False
		
	async def show(self):
		await self.init()
		await self.wait_tapped()
		return 10
		
	async def wait_tapped(self):
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


