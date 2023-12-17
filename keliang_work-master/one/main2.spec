# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main2.py'],
    pathex=[],
    binaries=[],
    datas=[('./Constant_output.txt', '.'), ('./Constant_output_1.txt', '.'), ('./Sine_Wave_output.txt', '.'), ('./data.txt', '.'), ('./Gain_output.txt', '.'), ('./SumCalculator_output.txt', '.'), ('./Mult_data_output.txt', '.'), ('./空.txt', '.'), ('./Real_time_read_file_data1.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main2',
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
