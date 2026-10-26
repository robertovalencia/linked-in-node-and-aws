"""Build the downloadable managed study pack; never include personal/saved notes."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
pack = root / 'docs/nodejs-aws-study-path'
output = pack / 'NodeJs-AWS-study-pack.zip'
files = [pack / 'README.md', pack / 'cloud-source-excerpts.json',
         *sorted((pack / 'generated').glob('*.md')),
         *sorted(p for p in (pack / 'labs').rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc')),
         *sorted((pack / 'evidence').glob('*'))]
assert len(list((pack / 'generated').glob('[0-9][0-9]-*.md'))) == 44
with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, 'NodeJs-AWS/' + path.relative_to(pack).as_posix())
print(f'Wrote {output.name}: {len(files)} managed files, 44 lessons; no personal notes.')
