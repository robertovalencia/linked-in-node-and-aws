"""Opt-in public-document GET checks; no credentials, AWS API or write request."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, unquote
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser


def document_anchors(text):
    class Anchors(HTMLParser):
        def __init__(self):
            super().__init__()
            self.values=set()
        def handle_starttag(self,tag,attrs):
            self.values.update(value for key,value in attrs if key in ('id','name') and value)
    parser=Anchors()
    parser.feed(text)
    return parser.values


def check(url):
    row={'url':url}
    try:
        request=Request(url,headers={'User-Agent':'NodeBackendStudyLinkCheck/1.0'})
        with urlopen(request,timeout=25) as response:
            content=response.read(5_000_000)
            row.update(status=response.status,effective_url=response.url,bytes_read=len(content),sha256=hashlib.sha256(content).hexdigest())
            fragment=unquote(urlsplit(url).fragment)
            if fragment:
                text=content.decode('utf-8',errors='replace')
                anchors=document_anchors(text)
                row['fragment_observed_in_response']=fragment in anchors
    except HTTPError as error:
        row.update(status=error.code,error=str(error))
    except (URLError,TimeoutError,OSError) as error:
        row.update(status=None,error=str(error))
    return row


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    items=json.loads((root/'docs/nodejs-aws-study-path/node-backend-questionnaire-map.json').read_text())['items']
    urls=sorted({u for r in items for u in [*r['official_references'],r.get('worked_example_url')] if u})
    with ThreadPoolExecutor(max_workers=10) as pool:
        results=list(pool.map(check,urls))
    failures=[r for r in results if r.get('status')!=200]
    fragments=[r for r in results if r.get('fragment_observed_in_response') is False]
    report=dict(date='2026-11-05',scope='Public documentation GET reachability, separate from technical claim review or execution of external examples.',
                urls=len(urls),http_200=len(results)-len(failures),non_200=len(failures),unobserved_fragments=len(fragments),results=results)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}))
    for row in failures:print(row['url'],row.get('status'),row.get('error'))
    for row in fragments:print('FRAGMENT NOT OBSERVED',row['url'])
    raise SystemExit(bool(failures or fragments))
