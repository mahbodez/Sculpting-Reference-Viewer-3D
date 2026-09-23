# PyInstaller spec for the self-contained desktop releases.

from pathlib import Path
import sys

from PyInstaller.utils.hooks import collect_submodules


project_root = Path(SPECPATH).parent
# Windows wants a multi-resolution .ico for the Explorer and taskbar icon; the
# other platforms take the PNG straight.
images = project_root / "resources" / "images"
icon = str(images / ("icon.ico" if sys.platform == "win32" else "icon-large.png"))
hiddenimports = collect_submodules("OpenGL")
datas = [(str(project_root / "resources"), "resources")]
datas.append((str(project_root / "pyproject.toml"), "."))
# The GLSL is read from beside the renderer's modules, so it goes where they do.
datas.append((str(project_root / "src" / "refview" / "render" / "glsl"), "refview/render/glsl"))

# Conda builds keep CPython's support DLLs in Library/bin, where PyInstaller's
# dependency scan does not look; without ffi-8.dll the frozen app cannot import
# _ctypes. A python.org build has no such directory, so this is a no-op there.
binaries = []
conda_bin = Path(sys.prefix) / "Library" / "bin"
if conda_bin.is_dir():
    for name in ("ffi-8.dll", "libffi-8.dll", "libbz2.dll", "liblzma.dll", "libexpat.dll"):
        dll = conda_bin / name
        if dll.is_file():
            binaries.append((str(dll), "."))

a = Analysis(
    [str(project_root / "run.py")],
    pathex=[str(project_root / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name="ReferenceViewer",
    icon=icon,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

if sys.platform == "darwin":
    # What Finder may hand the bundle: the model formats, a saved session and
    # the matcap images.  Without these the app is not offered under "Open
    # with", and a file dragged onto it is refused.  The file itself arrives
    # as a QFileOpenEvent, which refview.application.Application handles.
    def document_type(name, extensions, role="Viewer"):
        return {
            "CFBundleTypeName": name,
            "CFBundleTypeExtensions": list(extensions),
            "CFBundleTypeRole": role,
            "LSHandlerRank": "Alternate",
        }

    app = BUNDLE(
        exe,
        name="Reference Viewer.app",
        icon=icon,
        bundle_identifier="com.refview.referenceviewer",
        info_plist={
            "CFBundleDocumentTypes": [
                document_type("Wavefront OBJ model", ["obj"]),
                document_type("STL model", ["stl"]),
                document_type("glTF model", ["glb", "gltf"]),
                document_type("Reference Viewer session", ["json"], role="Editor"),
                document_type("Matcap image", ["png", "jpg", "jpeg", "bmp", "tif", "tiff", "webp"]),
            ],
            "NSHighResolutionCapable": True,
        },
    )
