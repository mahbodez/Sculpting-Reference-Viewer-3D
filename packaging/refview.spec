# PyInstaller spec for the self-contained desktop releases.

from pathlib import Path
import sys

from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules, copy_metadata


project_root = Path(SPECPATH).parent
# Windows wants a multi-resolution .ico for the Explorer and taskbar icon; the
# other platforms take the PNG straight.
images = project_root / "resources" / "images"
icon = str(images / ("icon.ico" if sys.platform == "win32" else "icon-large.png"))
hiddenimports = collect_submodules("OpenGL")
# The path tracer is imported lazily, from inside functions, so that numba is
# not loaded at startup; name every module of it rather than trust the scan.
# (From the checkout, so a build works without the package installed.)
sys.path.insert(0, str(project_root / "src"))
hiddenimports += collect_submodules("refview.trace")
# Intel Open Image Denoise finds Dr.Jit's thread pool beside the drjit
# package without importing it, and checks both versions through their
# metadata, so the package and both sets of metadata have to be there.  Its
# extension is a nanobind "split mode" one, whose backend is a package of its
# own that loads the compiled part lazily.
hiddenimports += ["mitsuba_oidn", "drjit"] + collect_submodules("nanobind_backend")
datas = [(str(project_root / "resources"), "resources")]
datas += copy_metadata("mitsuba-oidn") + copy_metadata("drjit")
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

# OIDN loads its CPU and CUDA device modules from the folder its core library
# is in, and the thread pool from drjit's, so each keeps its own folder.
binaries += collect_dynamic_libs("mitsuba_oidn") + collect_dynamic_libs("drjit")
binaries += collect_dynamic_libs("nanobind_backend")

# UPX must leave alone what it breaks or only slows down: LLVM (which
# llvmlite loads and patches at runtime), the MSVC runtime, and the denoiser's
# libraries, the CUDA one of which is most of the download and does not shrink.
upx_exclude = [
    "*llvmlite*", "vcruntime140*.dll", "msvcp140*.dll",
    "*mitsuba_oidn*", "*drjit*", "*nanothread*", "*nb_backend*",
]

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
    upx_exclude=upx_exclude,
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
