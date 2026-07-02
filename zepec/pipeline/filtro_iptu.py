import sys, csv
sqls=set(open('cedentes_sqls.txt').read().split())
sqls.discard('0000000000')
w=csv.writer(open('oficiais/cedentes_area_iptu.csv','w',newline='',encoding='utf-8'))
w.writerow(['sql_mestre','area_terreno','area_construida','v_venal_m2','codlog','uso','padrao','endereco'])
n=hit=0
rd=csv.reader((l.decode('latin-1','replace') for l in sys.stdin.buffer), delimiter=';')
next(rd,None)  # header
for r in rd:
    n+=1
    if len(r)<24: continue
    sql=r[0].split('-')[0]
    if sql in sqls:
        hit+=1
        end=f"{r[6].strip()}, {r[7].strip()}"
        w.writerow([sql, r[14], r[15], r[17], r[5], r[22], r[23], end])
sys.stderr.write(f"lidas={n} casadas={hit}\n")
