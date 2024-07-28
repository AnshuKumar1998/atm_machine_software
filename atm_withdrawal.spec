# -*- mode: python ; coding: utf-8 -*-


# In atm_machine.spec
a = Analysis(
    ['atm_new_atm.py'],
    pathex=['path_to_your_script'],
    binaries=[('path_to_libiconv.dll', 'libiconv.dll')],
    datas=[],
    hiddenimports=['requests', 'cv2', 'pyzbar.pyzbar', 'threading'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='atm_withdrawal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
