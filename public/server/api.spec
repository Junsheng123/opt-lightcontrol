# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_binaries = [
    ( 'tisgrabber_x64.dll', '.' ),
    ( 'TIS_UDSHL11_x64.dll', '.' ),
    ( 'C:\\opt-lightcontrol\\public\\server\\OPTControllerPython\\OPTControllerSDK\\x64\\OPTController.dll', '.')
]

added_files = [
    ( 'tisgrabber_x64.dll', '.' ),
    ( 'TIS_UDSHL11_x64.dll', '.' ),
]

a = Analysis(['api.py'],
             pathex=['C:\\opt-lightcontrol\\public\\server','C:\\opt-lightcontrol\\public\\server\\OPTControllerPython'],
             binaries=added_binaries,
             datas=added_files,
             hiddenimports=['pkg_resources.py2_warn'],
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
          name='api',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
