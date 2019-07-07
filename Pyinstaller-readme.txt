1:命令行,cd到要打包的.py文件根目录下；
2：运行 pyinstaller --onedir --windowed --icon="c:\Users\hero\PycharmProjects\DAP\ico.ico" Login.py
3:出现递归错误：Maximum recursion depth exceeded解决办法：在根目录下打开生成的spce文件，顶部添加 
	import sys
	sys.setrecursionlimit(5000)
	再次CD到根目录下，运行：pyinstaller Main.spec
4:打包成功，若出现failed to execute script main错误：重新运行第一步打包时添加次属性
	--hidden-import=queue
	或在spec文件中修改：
	hiddenimports=['queue'],
	再次运行pyinstaller Main.spec
5：若还不行，在spec中添加目录：
	pathex=['C:\\Users\\Administrator\\PycharmProjects\\LZL0704\\venv\\Lib\\site-packages', 'C:\\Users\\Administrator\\PycharmProjects\\LZL0704','C:\ProgramData\Anaconda3\Lib\site-packages'],
6：若依然报错，则在spec中修改：
	console=True ,
   生成exe，运行CMD，cd到exe目录，call Main.exe ,看看错误提示。
7：大部分错误是：No module Named
	比如：No module Named 'typedefs'
	则，添加目录C:\Users\Administrator\PycharmProjects\LZL0704\venv\Lib\site-packages\sklearn\neighbors
		或hiddenimports=['sklearn.neighbors.typedefs']
8:最终总结如下：
	缺少模块的时候，在主程序中加入from sklearn.neighbors import typedefs，
	或者在spec文件中修改hiddenimports=['sklearn.neighbors.typedefs'],
	或者在命令行添加--hidden-import=sklearn.neighbors.typedefs
9:打包成功，不要忘记改回console=false，并重新打包。

10：出现问题在spec中修改-debug=true，运行exe时可以查看错误信息
11：datas存储需要的文件夹，也可以打包完成后自行拷贝。

#########
把db，config，html，logs文件夹拷贝至生成的Login.exe根目录
把dist/MyPlotly中的plotly文件夹拷贝至生成的Login.exe根目录
