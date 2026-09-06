#!/usr/bin/env python3
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--apply", action="store_true")
    ap.parse_args()
    print("Bank $56 retry marker: no-op")
