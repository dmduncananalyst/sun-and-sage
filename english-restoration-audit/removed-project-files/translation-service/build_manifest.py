import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parent.parent/'homepage-service/capture_source.py'),run_name='__main__')
