
import random
import statistics
import time


def gen(n, rng, horizon=100):
    reqs = []
    for _ in range(n):
        s, d = rng.randint(0, horizon), rng.randint(2, 25)
        reqs.append((s, s + d, d * rng.uniform(0.8, 1.2)))
    return reqs


def overlap(a, b):


def greedy_length(reqs):
    for r in sorted(reqs, key=lambda r: r[1] - r[0]):
        if all(not overlap(r, c) for c in chosen):
            chosen.append(r)
    return chosen


def greedy_end(reqs):
    chosen, last = [], -1
    for r in sorted(reqs, key=lambda r: r[1]):
        if r[0] >= last:
            chosen.append(r)
            last = r[1]
    return chosen


def exact(reqs, weighted=False):
    rs = sorted(reqs, key=lambda r: r[1])
    best = []
    for i, r in enumerate(rs):
        w = r[2] if weighted else 1
        best.append(w + max((best[j] for j in range(i) if rs[j][1] <= r[0]), default=0))
    return max(best, default=0)


def main():

    ce = [(0, 5, 5), (4, 6, 2), (5, 10, 5)]
    print("Контрпример:", [(a, b) for a, b, _ in ce])
    print("  min длительность:", [(a, b) for a, b, _ in greedy_length(ce)], "| раннее окончание:",
          [(a, b) for a, b, _ in greedy_end(ce)], "| оптимум:", exact(ce))

    rng = random.Random(2024)
    dev = {"Минимальная длительность": [], "Раннее окончание": []}
    hits = dict.fromkeys(dev, 0)
    sets = [gen(40, rng) for _ in range(500)]
    for reqs in sets:
        opt = exact(reqs)
        for name, f in (("Минимальная длительность", greedy_length), ("Раннее окончание", greedy_end)):
            got = len(f(reqs))
            dev[name].append((opt - got) / opt * 100)
            hits[name] += got == opt
    print(f"\n{'Критерий':<26}{'среднее,%':>10}{'медиана,%':>11}{'максимум,%':>12}{'совпало':>9}")
    for name, d in dev.items():
        print(f"{name:<26}{statistics.mean(d):>10.2f}{statistics.median(d):>11.2f}{max(d):>12.2f}{hits[name] / 5:>8.1f}%")

    print(f"\n{'n':>6}{'жадный,с':>11}{'ДП,с':>9}{'отношение':>11}")
    for n in (100, 500, 1000, 2000, 5000):
        reqs = gen(n, random.Random(1), horizon=2 * n)
        t0 = time.perf_counter(); greedy_end(reqs); tg = time.perf_counter() - t0
        t0 = time.perf_counter(); exact(reqs); te = time.perf_counter() - t0
        print(f"{n:>6}{tg:>11.5f}{te:>9.4f}{te / tg:>11.0f}")

    loss_e, loss_l, opt_sum = [], [], []
    for reqs in sets:
        opt = exact(reqs, weighted=True)
        opt_sum.append(opt)
        loss_e.append(opt - sum(r[2] for r in greedy_end(reqs)))
        loss_l.append(opt - sum(r[2] for r in greedy_length(reqs)))
    print(f"\nЖ7: средний максимальный доход за день {statistics.mean(opt_sum):.1f} тыс. ₽")
    for name, loss in (("раннее окончание", loss_e), ("минимальная длительность", loss_l)):
        m = statistics.mean(loss)
        print(f"  {name:<26} потеря {m:6.1f} тыс. ₽/день ({m / statistics.mean(opt_sum) * 100:.1f} %), "
              f"{m * 250 / 1000:.2f} млн ₽/год")


if __name__ == "__main__":
    main()
