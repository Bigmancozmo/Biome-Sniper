import shutil
import updater
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
import pathspec

print("\nTarget version:", updater.CURRENT, "\n")

print("Clearing existing zips...")
folder = Path(__file__).parent
for file in folder.glob("*.zip"):
    file.unlink()
    print("Removed:", file.name)
if (folder / "build").exists():
    shutil.rmtree(folder / "build")
print("Complete\n")

# extra files/folders to ignore
custom_exclude = {"data.json", ".gitignore", "play.ahk", "__pycache__", ".git", "BUILD-ZIP-FILE.py", "README.md"}

gitignore_file = folder / ".gitignore"
if gitignore_file.exists():
    with gitignore_file.open() as f:
        spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
else:
    spec = pathspec.PathSpec.from_lines("gitwildmatch", [])

files_to_zip = []

for file in folder.rglob("*"):
    if file.is_file() and ".git" not in file.parts and file.name not in custom_exclude and not spec.match_file(str(file.relative_to(folder))):
        files_to_zip.append(file)

print("Collected files:")
for f in files_to_zip:
    print(f.relative_to(folder))

# make build folder
build_folder = folder / "build"
build_folder.mkdir(exist_ok=True)

# copy files preserving folder structure
for file in files_to_zip:
    dest = build_folder / file.relative_to(folder)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(file, dest)

print("Zipping...")
zip_file = folder / f"BMCs.Biome.Sniper.{updater.CURRENT}.zip"
with ZipFile(zip_file, "w", compression=ZIP_DEFLATED) as zipf:
    for file in build_folder.rglob("*"):
        zipf.write(file, arcname=file.relative_to(build_folder))
