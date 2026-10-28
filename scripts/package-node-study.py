"""Build the managed study ZIP without personal notes, Terraform state or caches."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

root = Path(__file__).resolve().parents[1]
pack = root / 'docs/nodejs-aws-study-path'
output = pack / 'NodeJs-AWS-study-pack.zip'
manifest = json.loads((pack / 'cloud-coverage.json').read_text())
lessons = sorted((pack / 'generated').glob('[0-9][0-9]-*.md'))
assert [int(p.name[:2]) for p in lessons] == list(range(manifest['lesson_count']))
files = [pack / name for name in ('README.md','cloud-coverage.json','cloud-source-excerpts.json','core-44-63-reference-manifest.json','deployment-handoff.md','deployment-coordination.json')]
files += lessons
for directory in ('labs','evidence'):
    files += sorted(p for p in (pack / directory).rglob('*') if p.is_file() and not any(part in ('__pycache__','.terraform','personal','saved','comments') for part in p.parts) and not p.name.endswith(('.pyc','.tfstate','.tfstate.backup','.tfplan','.zip')))
assert all(p.exists() for p in files)
with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, 'NodeJs-AWS/' + path.relative_to(pack).as_posix())
print(f'Wrote {output.name}: {len(files)} managed files, {len(lessons)} lessons; no personal notes.')
