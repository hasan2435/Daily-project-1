#!/usr/bin/env python3
"""
Daily Project 1 - Pomodoro Timer terminal.
  python3 pomodoro.py              # 25 menit fokus, 5 menit istirahat, 4 putaran
  python3 pomodoro.py 15 3         # 15 menit fokus, 3 menit istirahat
Hanya Python standar, tanpa library tambahan. Tekan Ctrl+C untuk berhenti.
"""
import sys, time

def hitung_mundur(menit, label):
    total = int(menit * 60)
    try:
        while total > 0:
            m, s = divmod(total, 60)
            print(f"\r{label}: {m:02d}:{s:02d}  ", end="", flush=True)
            time.sleep(1); total -= 1
        print(f"\r{label}: selesai!{' ' * 20}")
    except KeyboardInterrupt:
        print("\nBerhenti. Istirahat dulu, lanjut lagi nanti.")
        raise SystemExit(0)

def main():
    fokus = float(sys.argv[1]) if len(sys.argv) > 1 else 25
    istirahat = float(sys.argv[2]) if len(sys.argv) > 2 else 5
    putaran = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    print(f"Pomodoro: {fokus} menit fokus, {istirahat} menit istirahat, {putaran} putaran.")
    for i in range(1, putaran + 1):
        print(f"\n--- Putaran {i}/{putaran}: FOKUS ---")
        hitung_mundur(fokus, "Fokus")
        if i < putaran:
            print(f"--- Istirahat ---")
            hitung_mundur(istirahat, "Istirahat")
    print("\nSemua putaran selesai. Kerja bagus!")

if __name__ == "__main__":
    main()
