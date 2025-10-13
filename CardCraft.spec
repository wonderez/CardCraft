# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\RedBookCards-1.0.2\\resources', 'resources'), ('D:\\RedBookCards-1.0.2\\src', 'src')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.QtWebEngineCore', 'PyQt6.QtWebEngineWidgets', 'markdown', 'markdown.extensions', 'markdown.extensions.fenced_code', 'markdown.extensions.tables', 'markdown.extensions.nl2br', 'markdown.extensions.attr_list', 'markdown.extensions.def_list', 'markdown.extensions.footnotes', 'markdown.extensions.toc', 'markdown.extensions.sane_lists', 'markdown.extensions.smarty', 'bs4'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 'test', 'tests'],
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
    name='CardCraft',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='D:\\RedBookCards-1.0.2\\version_info.txt',
    icon=['D:\\RedBookCards-1.0.2\\resources\\icons\\app.ico'],
)
