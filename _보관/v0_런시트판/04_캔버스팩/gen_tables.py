from statistics import NormalDist; import math
nd = NormalDist()
def n_per_group(p1, d, alpha=0.05, power=0.80):
    p2 = p1 + d
    za, zb = nd.inv_cdf(1 - alpha/2), nd.inv_cdf(power)
    return (za + zb)**2 * (p1*(1-p1) + p2*(1-p2)) / (d*d)
ceil10 = lambda x: int(math.ceil(x/10.0)*10)

rows = [.10,.15,.20,.25,.30,.40,.50,.60]
cols = [.03,.05,.08,.10,.15,.20]

def print_table(alpha, power, title):
    print(f"**표 {title}** (α={alpha}, power={power})")
    header = "| 기준 지표(p) | " + " | ".join([f"{int(c*100)}%p" for c in cols]) + " |"
    print(header)
    print("|---|" + "|".join(["---" for _ in cols]) + "|")
    for r in rows:
        row_str = f"| {int(r*100)}% |"
        for c in cols:
            val = ceil10(n_per_group(r, c, alpha, power))
            row_str += f" {val} |"
        print(row_str)
    print()

print_table(0.05, 0.80, "A")
print_table(0.05, 0.90, "B")
print_table(0.10, 0.80, "C")

print("**표 D (기간 환산)**")
d_rows = [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 3000, 4000]
print("| 필요 표본(군당) | " + " | ".join([f"{c}건/주" for c in [100, 200, 300, 400, 500, 1000]]) + " |")
print("|---|" + "|".join(["---" for _ in range(6)]) + "|")
for dr in d_rows:
    row_str = f"| {dr} |"
    for c in [100, 200, 300, 400, 500, 1000]:
        val = math.ceil(dr/c)
        row_str += f" {val}주 |"
    print(row_str)
