"""Package existing English and saved translated files without translation or rendering."""
from pathlib import Path
import argparse,json,shutil
ROOT=Path(__file__).resolve().parents[1]
MEDIA={'.png','.jpg','.jpeg','.webp','.gif','.svg','.pdf','.mp4','.webm','.ico','.woff','.woff2'}
def build(output):
    output=Path(output).resolve()
    if output.exists():raise RuntimeError('Use a fresh output directory; existing files are never overwritten.')
    config=json.loads((ROOT/'tools/production-pages.json').read_text(encoding='utf-8'))
    routes=config['english']+[language+'/'+route for language,entries in config['locales'].items() for route in entries]
    for route in routes:
        source=ROOT/route
        if not source.is_file():raise RuntimeError('Missing approved saved page: '+route)
    output.mkdir(parents=True)
    photography=json.loads((ROOT/'tools/photography-policy.json').read_text(encoding='utf-8'))
    retired=set(photography['prohibited_references'])
    def omit_retired(directory,names):
        return [name for name in names if (Path(directory)/name).relative_to(ROOT).as_posix() in retired]
    shutil.copytree(ROOT/'assets',output/'assets',ignore=omit_retired)
    for source in ROOT.iterdir():
        if source.is_file() and (source.suffix.lower() in MEDIA or source.name in {'CNAME','robots.txt','llms.txt','.nojekyll'} or source.name.startswith('sitemap') and source.suffix=='.xml'):
            shutil.copy2(source,output/source.name)
    for route in routes:
        destination=output/route;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/route,destination)
    (output/'.nojekyll').touch()
    return {'pages':len(routes),'english':len(config['english']),'saved_localized':len(routes)-len(config['english']),'translation_calls':0,'output':str(output)}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT/'dist-existing'));args=parser.parse_args()
    print(json.dumps(build(args.output),indent=2))
