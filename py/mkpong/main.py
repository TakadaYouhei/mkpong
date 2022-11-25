import asyncio
import queue
import scene
import ui


def YARITAIKOTO():
	# 初期化
	gm = GameManager()

	while (True):
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


class GameScene():
	def __init__(self, gm):
		self.gm = gm
		self.evt_closed = asyncio.Event()
		self.nodes = []

	def touch_began(self, touch):
		self.set_closed()

	def close(self):
		self.set_closed()

	async def wait_closed(self):
		print('GameScene.wait_closed called.')
		if self.evt_closed.is_set():
			return
		await self.evt_closed.wait()

	def set_closed(self):
		print('GameScene.set_closed called.')
		self.evt_closed.set()

	def get_root(self):
		return self.gm.get_rootpyscene()

	def add_child(self, node):
		root = self.get_root()
		root.add_child(node)
		self.nodes.append(node)

	def remove_child(self, node):
		root = self.get_root()
		if node in self.nodes:
			print('remove')
			node.remove_from_parent()
			self.nodes.remove(node)
		else:
			print('cannot remove. it is not found.')

	async def init(self):
		root = self.get_root()
		root.set_receiver(self)

		ssize = scene.get_screen_size()
		sscale = scene.get_screen_scale()
		pnt_center = scene.Point(ssize.x / 2, ssize.y / 2)

		## Background
		bg = scene.ShapeNode()
		bg.path = ui.Path.rect(0, 0, ssize.w, ssize.h)
		bg.x_scale = sscale
		bg.y_scale = sscale
		bg.fill_color = 'pink'
		self.add_child(bg)

		## 何か文字
		logo = scene.LabelNode()
		logo.text = 'Game scene'
		logo.position = pnt_center + scene.Point(0, 500)
		self.add_child(logo)

	async def term(self):
		for node in self.nodes:
			node.remove_from_parent()
		self.nodes = []
		root = self.get_root()
		root.set_receiver(None)

	async def show(self):
		await self.init()

		# Ready
		await self.ready_init()
		await self.ready_main()
		await self.ready_term()

		# Game
		await self.game_init()
		await self.game_main()
		await self.game_term()

		await self.wait_closed()
		await self.term()

		return 0

	async def ready_init(self):
		p = scene.Node()

		ssize = scene.get_screen_size()
		sscale = scene.get_screen_scale()
		pnt_center = scene.Point(ssize.x / 2, ssize.y / 2)

		label = scene.LabelNode()
		label.text = 'Ready'
		label.position = pnt_center
		p.add_child(label)

		self.ready_node = p
		self.add_child(self.ready_node)

	async def ready_term(self):
		self.remove_child(self.ready_node)
		self.ready_node = None

	async def ready_main(self):
		await asyncio.sleep(2)

	async def game_init(self):
		p = scene.Node()

		ssize = scene.get_screen_size()

		# 左側の縦線
		line_lv = scene.ShapeNode()
		line_lv.path = ui.Path.rect(400, -800, 400, 400)
		line_lv.path.line_width = 2.0
		line_lv.path.move_to(0, 0)
		line_lv.path.line_to(100, 100)
		line_lv.path.line_to(100, -100)
		line_lv.path.line_to(-100, -100)
		line_lv.path.line_to(-100, 100)
		line_lv.path.line_to(100, 100)
		line_lv.path.stroke()
		line_lv.fill_color = 'green'
		p.add_child(line_lv)

		self.game_node = p
		self.add_child(p)

	async def game_term(self):
		self.remove_child(self.game_node)
		self.game_node = None

	async def game_main(self):
		await asyncio.sleep(10)


class TitleScene():
	def __init__(self, gm):
		self.gm = gm
		self.evt_tapped = asyncio.Event()
		self.nodes = []

	def touch_began(self, touch):
		print('touch_began called.')
		self.set_tapped()

	def touch_moved(self, touch):
		print('touch moved')

	def touch_ended(self, touch):
		print('touch ended.')

	def close(self):
		print('close called.')
		self.set_tapped()

	#def update(self):
	#	pass

	def get_root(self):
		return self.gm.get_rootpyscene()

	def add_child(self, node):
		root = self.get_root()
		root.add_child(node)
		self.nodes.append(node)

	async def init(self):
		root = self.get_root()
		root.set_receiver(self)

		ssize = scene.get_screen_size()
		sscale = scene.get_screen_scale()
		pnt_center = scene.Point(ssize.x / 2, ssize.y / 2)

		## Background
		#bg = scene.SpriteNode('plf:BG_Colored_land')
		#fit_to_size(bg, root)
		bg = scene.ShapeNode()
		bg.path = ui.Path.rect(0, 0, ssize.w, ssize.h)
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
		root = self.get_root()
		root.set_receiver(None)

	async def show(self):
		await self.init()
		await self.wait_tapped()
		await self.term()

		return 1

	async def wait_tapped(self):
		print('wait_tapped start.')
		self.evt_tapped.clear()
		print('wait_tapped waiting...')
		await self.evt_tapped.wait()
		print('wait_tapped ended.')

	def set_tapped(self):
		print('set_tapped called.')
		self.evt_tapped.set()
		print('set_tapped ended.')


class RootPyScene(scene.Scene):
	def __init__(self, loop):
		super().__init__()
		self.loop = loop
		self._is_stopped = False

	def is_stopped(self):
		return self._is_stopped

	def setup(self):
		self.receiver = None
		self.background_color = 'blue'

	def set_receiver(self, receiver):
		"""touch_began, touch_moved, touch_ended を受け取るオブジェクトを登録する"""
		self.receiver = receiver

	def update(self):
		pass

	def call_receiver_func(self, func, *args):
		if self.receiver is not None:
			try:
				self.loop.call_soon_threadsafe(getattr(self.receiver, func), *args)
			except AttributeError:
				pass

	def touch_began(self, touch):
		self.call_receiver_func('touch_began', touch)

	def touch_moved(self, touch):
		self.call_receiver_func('touch_moved', touch)

	def touch_ended(self, touch):
		self.call_receiver_func('touch_ended', touch)

	def stop(self):
		self.call_receiver_func('close')
		self._is_stopped = True


class GameManager():
	def __init__(self):
		self.rootpyscene = None
		self.loop = None
		self.rootpyscene_task = None

	def get_rootpyscene(self):
		return self.rootpyscene

	async def init(self):
		self.rootpyscene = RootPyScene(self.loop)
		scene.run(self.rootpyscene)

	async def term(self):
		self.rootpyscene_task = None

	async def show(self, scene):
		ret = await scene.show()
		return ret

	async def main_loop(self):
		print('main_loop began')

		# 初期化
		await self.init()

		while True:

			# タイトル
			title = TitleScene(self)
			ret = await self.show(title)
			if ret == 0:
				break
			if self.get_rootpyscene().is_stopped():
				break

			# ゲームシーン
			game = GameScene(self)
			await self.show(game)
			if self.get_rootpyscene().is_stopped():
				break

		# 後始末
		await self.term()

		print('main_loop finish.')

	def start_main_loop(self):
		#loop = asyncio.get_event_loop()
		self.loop = asyncio.get_event_loop_policy().new_event_loop()
		self.loop.run_until_complete(self.main_loop())
		self.loop.close()


def main():
	print('start')
	GameManager().start_main_loop()
	print('finish')


if '__main__' == __name__:
	main()

