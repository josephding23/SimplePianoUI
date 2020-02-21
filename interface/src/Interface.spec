# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Interface.py'],
             pathex=['C:/ProgramData/Anaconda3/Lib/site-packages', 'D:\\PycharmProjects\\SimplePianoInterface\\interface\\src'],
             binaries=[],
             datas=[('D:/PycharmProjects/SimplePianoInterface/interface/src/icon/*.png', 'icon')],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Interface',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='gramophone.ico')
