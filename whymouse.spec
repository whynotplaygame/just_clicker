# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['my_click_click.py', 'ui_click.py', 'ui_imagelist.py', 'click_other_widgets.py', 'click_model_threads.py'],
    pathex=['D:\\youlePeriod\\个人数据资源\\suibian\\.venv', '.'],
    binaries=[],
    datas=[],
    hiddenimports=['ui_click', 'ui_imagelist', 'click_model_threads', 'click_other_widgets'],
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
    name='whymouse',
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
)
