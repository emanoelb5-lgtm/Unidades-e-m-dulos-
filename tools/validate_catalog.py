"""Validate an import package independently from the currently published APK snapshot."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def validate(path):
    raw=path.read_bytes()
    assert len(raw)<=2_000_000,'Content package exceeds the APK limit'
    c=json.loads(raw)
    assert c['schemaVersion']==1 and c['contentVersion']>0
    assert 1<=len(c['modules'])<=10 and 1<=len(c['units'])<=100
    outlines={u['id']:m['id'] for m in c['modules'] for u in m['units']}
    assert sum(m['hours'] for m in c['modules'])==200
    all_ids=[]
    for u in c['units']:
        assert outlines[u['id']]==u['moduleId']
        assert 1<=len(u['lessons'])<=100
        ids=[l['id'] for l in u['lessons']];all_ids+=ids
        chapters=u.get('chapters',[])
        if chapters:
            assert [id for ch in chapters for id in ch['lessonIds']]==ids
            assert len({ch['id'] for ch in chapters})==len(chapters)
        for l in u['lessons']:
            assert l['title'].strip() and l['subtitle'].strip()
            assert l['objectives'] and len(l['guide'])>=3
            assert 1<=l['minutes']<=240
            kinds={b['kind'] for b in l['blocks']}
            assert {'text','example','practice'}<=kinds
            assert kinds<={'text','example','practice','callout'}
            for b in l['blocks']:assert b['title'].strip() and b['text'].strip() and len(b['text'])<=30000
            assert l.get('lab') in [None,'Bits','Bases','Sinal','Precisão','Texto','Cores','Mídia']
        assert 1<=len(u['quiz'])<=150 and len({q['id'] for q in u['quiz']})==len(u['quiz'])
        for q in u['quiz']+[l['check'] for l in u['lessons']]:
            assert q['prompt'].strip() and q['explanation'].strip()
            assert 2<=len(q['choices'])<=6 and all(x.strip() for x in q['choices'])
            assert 0<=q['correct']<len(q['choices'])
        assert {q['lessonId'] for q in u['quiz']}==set(ids)
        assert len({t['term'].casefold() for t in u['glossary']})==len(u['glossary'])
        assert all(r['url'].startswith('https://') for r in u.get('references',[]))
    assert len(set(all_ids))==len(all_ids),'Lesson IDs must be unique across units'
    return c

if __name__=='__main__':
    import argparse, subprocess
    parser=argparse.ArgumentParser(description='Validar as lições públicas do VibeCode.')
    parser.add_argument('--baseline', default='', help='Commit anterior para preservar IDs e versões.')
    args=parser.parse_args()
    package=validate(ROOT/'content/catalog.json')
    assert len({m['id'] for m in package['modules']})==len(package['modules'])
    assert len({u['id'] for u in package['units']})==len(package['units'])
    for unit in package['units']:
        assert unit.get('assessmentVersion',1)>0
        assert unit['description'].strip() and unit['title'].strip()
        assert all(t['term'].strip() and t['definition'].strip() for t in unit['glossary'])
        for lesson in unit['lessons']:
            assert lesson['check'].get('lessonId',lesson['id'])==lesson['id']
    if args.baseline and set(args.baseline)!={'0'}:
        before=subprocess.run(['git','show',args.baseline+':content/catalog.json'],capture_output=True,text=True)
        if before.returncode==0:
            previous=json.loads(before.stdout)
            assert package['contentVersion']>=previous['contentVersion'],'Não reduza contentVersion.'
            if package!=previous:
                assert package['contentVersion']>previous['contentVersion'],'Aumente contentVersion quando modificar as lições.'
            for old in previous['units']:
                current=next((u for u in package['units'] if u['id']==old['id']),None)
                assert current is not None,'Preserve as unidades anteriores.'
                assert current['moduleId']==old['moduleId'],'Preserve a unidade no mesmo módulo.'
                assert current.get('assessmentVersion',1)>=old.get('assessmentVersion',1),'Não reduza assessmentVersion.'
                assert {l['id'] for l in old['lessons']}<={l['id'] for l in current['lessons']},'Preserve todas as lições publicadas.'
    print(f"Catálogo válido: conteúdo {package['contentVersion']}, {len(package['units'])} unidades, {sum(len(u['lessons']) for u in package['units'])} lições.")
