#/bin/zsh

cd "$(dirname "$0")"
source .venv/bin/activate
./main.py --content .. --api http://localhost:8000 --port 9000 --wc http://localhost:5173/src/main.ts