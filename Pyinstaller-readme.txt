1:������,cd��Ҫ�����.py�ļ���Ŀ¼�£�
2������ pyinstaller --onefile --windowed --icon="c:\Users\Administrator\PycharmProjects\LZL0704\ico.ico" Main.py
3:���ֵݹ����Maximum recursion depth exceeded����취���ڸ�Ŀ¼�´����ɵ�spce�ļ���������� 
	import sys
	sys.setrecursionlimit(5000)
	�ٴ�CD����Ŀ¼�£����У�pyinstaller Main.spec
4:����ɹ���������failed to execute script main�����������е�һ�����ʱ��Ӵ�����
	--hidden-import=queue
	����spec�ļ����޸ģ�
	hiddenimports=['queue'],
	�ٴ�����pyinstaller Main.spec
5���������У���spec�����Ŀ¼��
	pathex=['C:\\Users\\Administrator\\PycharmProjects\\LZL0704\\venv\\Lib\\site-packages', 'C:\\Users\\Administrator\\PycharmProjects\\LZL0704','C:\ProgramData\Anaconda3\Lib\site-packages'],
6������Ȼ��������spec���޸ģ�
	console=True ,
   ����exe������CMD��cd��exeĿ¼��call Main.exe ,����������ʾ��
7���󲿷ִ����ǣ�No module Named
	���磺No module Named 'typedefs'
	�����Ŀ¼C:\Users\Administrator\PycharmProjects\LZL0704\venv\Lib\site-packages\sklearn\neighbors
		��hiddenimports=['sklearn.neighbors.typedefs']
8:�����ܽ����£�
	ȱ��ģ���ʱ�����������м���from sklearn.neighbors import typedefs��
	������spec�ļ����޸�hiddenimports=['sklearn.neighbors.typedefs'],
	���������������--hidden-import=sklearn.neighbors.typedefs
9:����ɹ�����Ҫ���ǸĻ�console=false�������´����