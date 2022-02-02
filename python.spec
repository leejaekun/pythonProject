# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['plotMotorChar.pyC:\\Users\\local_ojguiak\\AppData\\Local\\Programs\\Python\\Python38-32\\python.exe', 'c:/Users/local_ojguiak/Desktop/catalogue/pythonProject/plotMotorChar.py'],
             pathex=['C:\\Users\\local_ojguiak\\Desktop\\catalogue\\pythonProject'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy.spatial.transform._rotation_groups'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='python',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='python')
