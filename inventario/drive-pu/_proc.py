import sys, json, os, subprocess
# uso: _proc.py <json_file> <path_label>
# 1) anexa linhas de arquivo no bronze CSV (via _transform.py)
# 2) imprime subpastas encontradas (id<TAB>title) e o nextPageToken numa linha NEXT<TAB>token
HERE = os.path.dirname(os.path.abspath(__file__))
BRONZE = os.path.join(HERE, "catalogo-lake-bronze-raw.csv")
IDX = os.path.join(HERE, "_indexed-ids.txt")
TRANSFORM = os.path.join(HERE, "_transform.py")
jf, path_label = sys.argv[1], sys.argv[2]
with open(BRONZE, "a", encoding="utf-8") as out:
    subprocess.run([sys.executable, TRANSFORM, jf, path_label, IDX], stdout=out, check=True)
d = json.load(open(jf, encoding="utf-8"))
files = d.get("files", [])
for f in files:
    if f.get("mimeType") == "application/vnd.google-apps.folder":
        title = (f.get("title") or f.get("name") or "").replace("\t", " ").replace("\n", " ")
        print(f"{f.get('id')}\t{title}")
tok = d.get("nextPageToken", "") or ""
print(f"NEXT\t{tok}")
