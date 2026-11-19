"""Check that the class version equals the last CHANGELOG version and that no version is skipped."""
import re

cls = open(r"C:\biu\02\closettwin.cls", encoding="utf-8").read()
m = re.search(r"\\ProvidesClass\{closettwin\}\[([\d/]+) (v[\d.]+)", cls)
ch = open(r"C:\biu\02\fix\CHANGELOG.md", encoding="utf-8").read()
vs = re.findall(r"closettwin (v[\d.]+)", ch)
nums = [int(v.split(".")[1]) for v in vs]
print("class:", m.group(2), m.group(1))
print("changelog:", vs[0], "..", vs[-1], f"({len(vs)} rows)")
print("sequence complete:", nums == list(range(1, len(nums) + 1)))
print("MATCH" if vs[-1] == m.group(2) else "MISMATCH")
