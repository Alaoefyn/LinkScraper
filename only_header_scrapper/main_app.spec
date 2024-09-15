# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['main_app.py'],
    pathex=[],
    binaries=[
        ('whitestyle.qss', '.'),  # Include whitestyle.qss
        ('darkstyle.qss', '.'),   # Include darkstyle.qss
    ],
    datas=[
        ('whitestyle.qss', '.'),  # Include whitestyle.qss
        ('darkstyle.qss', '.'),   # Include darkstyle.qss
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Header Scrapper Program',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Prevent terminal window from opening
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ghost.ico'  # Set the icon for the executable
)
