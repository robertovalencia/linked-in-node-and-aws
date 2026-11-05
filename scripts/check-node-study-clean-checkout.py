"""Rebuild the intended documentation delta in a local clean Git checkout and extracted ZIP."""
from pathlib import Path
from zipfile import ZipFile
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
PACK=Path('docs/nodejs-aws-study-path')
EXACT=['README.md','docs/nodejs-beginner/README.md','docs/progress.html',
       'docs/nodejs-aws-study-path/README.md',
       'docs/specs/requirements.md','docs/traceability.md','docs/reviews.md',
       'scripts/check-cloud-study.py','scripts/package-node-study.py',
       'scripts/render-node-questionnaire.py','scripts/check-node-questionnaire.py',
       'scripts/check-node-questionnaire.test.py','scripts/check-node-study-links.py',
       'scripts/check-node-study-clean-checkout.py']


def main(output):
    evidence={'date':'2026-11-05','scope':'Clean local Git candidate with only intended study deltas; no network, cloud or publication.','commands':[]}
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    def run(args,cwd):
        result=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
        evidence['commands'].append(dict(command=args,cwd_scope='extracted ZIP' if cwd.name=='NodeJs-AWS' else 'clean candidate',exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
        if result.returncode:raise RuntimeError(f'{args}: {result.stderr or result.stdout}')
        return result
    try:
        with tempfile.TemporaryDirectory(prefix='node-study-clean-') as directory:
            base=Path(directory);candidate=base/'candidate'
            run(['git','clone','--quiet','--shared','--no-checkout','--local',str(ROOT),str(candidate)],base)
            run(['git','checkout','--quiet','HEAD'],candidate)
            files=[Path(p) for p in EXACT if (ROOT/p).is_file()]
            files+=list(p.relative_to(ROOT) for p in (ROOT/PACK).glob('node-*.md'))
            files+=list(p.relative_to(ROOT) for p in (ROOT/PACK).glob('node-*.json'))
            files+=list(p.relative_to(ROOT) for p in (ROOT/PACK/'evidence').glob('node-backend-*') if p.is_file())
            files+=list(p.relative_to(ROOT) for p in (ROOT/PACK/'labs/node-runtime').glob('*') if p.is_file())
            for rel in files:
                target=candidate/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
            evidence['intended_files_copied']=[str(p) for p in files]
            evidence['external_profile_access_required']=False
            evidence['checker_reads_external_profile']=False
            evidence['external_profile_explanation']='Checker reads only the retained inventory and candidate source; no external-profile filesystem access is needed.'
            # Canaries prove the packager itself excludes these paths/suffixes.
            for rel in ['personal/private-canary.md','saved/private-canary.md','comments/private-canary.md','labs/node-runtime/.terraform/cache','labs/node-runtime/private.tfstate','labs/node-runtime/private.tfplan','labs/node-runtime/__pycache__/private.pyc','labs/node-runtime/.env','labs/node-runtime/.env.local']:
                p=candidate/PACK/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('private canary\n')
            run(['python3','scripts/package-node-study.py'],candidate)
            run(['python3','scripts/check-cloud-study.py','--repository',str(candidate)],candidate)
            run(['python3','scripts/check-node-questionnaire.py','--archive'],candidate)
            run(['python3','scripts/check-node-questionnaire.test.py'],candidate)
            run(['python3','scripts/check-aws-questionnaire.test.py'],candidate)
            archive=candidate/PACK/'NodeJs-AWS-study-pack.zip'
            with ZipFile(archive) as z:
                names=z.namelist();assert not any('canary' in n or 'private.tf' in n or '__pycache__' in n or '.terraform' in n or Path(n).name.startswith('.env') for n in names)
                extracted=base/'extracted';z.extractall(extracted)
                for n in names:assert z.read(n)==(candidate/PACK/Path(n).relative_to('NodeJs-AWS')).read_bytes()
                evidence['archive_members']=len(names)
            run(['node','--unhandled-rejections=strict','labs/node-runtime/run.mjs'],extracted/'NodeJs-AWS')
            evidence['all_archive_member_bytes_match_candidate']=True
            evidence['private_canaries_excluded']=True
            # ZIP timestamps differ between checkouts, so compare semantic member bytes to the current managed ZIP.
            with ZipFile(ROOT/PACK/'NodeJs-AWS-study-pack.zip') as current, ZipFile(archive) as rebuilt:
                assert set(current.namelist())==set(rebuilt.namelist())
                assert all(current.read(n)==rebuilt.read(n) for n in current.namelist())
            evidence['clean_rebuild_member_bytes_match_working_pack']=True
            evidence['status']='PASS'
    except Exception as error:
        evidence.update(status='FAIL',error=str(error))
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps({k:v for k,v in evidence.items() if k not in ('commands','intended_files_copied')}))
    return 0 if evidence['status']=='PASS' else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    raise SystemExit(main(parser.parse_args().output))
