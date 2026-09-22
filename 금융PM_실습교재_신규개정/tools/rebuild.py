"""One-command deterministic rebuild. Standard library; PDF is optional."""
import argparse,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--pdf',action='store_true');p.add_argument('--package',action='store_true');a=p.parse_args();root=Path(__file__).parent
for script in ['build.py','enrich.py','teaching.py','finish_content.py','guided_course.py','validate.py','guided_check.py','reader_check.py']+(['publish.py'] if a.pdf else [])+(['package.py'] if a.package else []):
 subprocess.run([sys.executable,str(root/script)],check=True)
