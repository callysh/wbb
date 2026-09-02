# -*- coding: utf-8 -*-
"""초안 .md → 스마트에디터 붙여넣기용 .html (마루부리 16px, 여백, 표 테두리)
사용: python scripts/md2html.py drafts/2026-09-02-주제-초안.md  → 같은 경로 .html 생성"""
import io, re, sys, html, os

FONT = "font-family:'마루부리','MaruBuri',serif;font-size:16px;line-height:1.9;"
P = FONT + "margin:0 0 10px 0;"

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

def table(rows):
    out = ['<table style="border-collapse:collapse;width:100%;margin:8px 0 12px 0;' + FONT + '">']
    for i, r in enumerate(rows):
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        tag = "th" if i == 0 else "td"
        bg = ' background:#f3f3f3;' if i == 0 else ''
        out.append("<tr>" + "".join(
            f'<{tag} style="border:1px solid #bbb;padding:8px 10px;text-align:left;{bg}{FONT}">{inline(c)}</{tag}>'
            for c in cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)

def convert(src):
    lines = io.open(src, encoding="utf-8").read().splitlines()
    body, i = [], 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s\-:|]+\|$", lines[i]):
                    rows.append(lines[i])
                i += 1
            body.append(table(rows)); continue
        if l.strip() == "---":
            body.append(f'<p style="{P}">&nbsp;</p>')
        elif not l.strip():
            body.append(f'<p style="{P}">&nbsp;</p>')
        elif l.startswith("# "):
            body.append(f'<p style="{P}font-size:19px;"><b>{inline(l[2:])}</b></p>')
        elif l.startswith("## "):
            body.append(f'<p style="{P}"><b>{inline(l[3:])}</b></p>')
        elif l.startswith("- "):
            body.append(f'<p style="{P}">&#8226; {inline(l[2:])}</p>')
        else:
            body.append(f'<p style="{P}">{inline(l)}</p>')
        i += 1
    # 연속 빈 문단 1개로 압축
    out, prev_blank = [], False
    for b in body:
        blank = b.endswith("&nbsp;</p>")
        if blank and prev_blank: continue
        out.append(b); prev_blank = blank
    title = os.path.basename(src)
    return ('<!doctype html><html><head><meta charset="utf-8"><title>' + html.escape(title) + '</title></head>'
            '<body style="margin:0;background:#fafafa;"><div style="max-width:720px;margin:40px auto;padding:32px 40px;'
            'background:#fff;border:1px solid #e5e5e5;' + FONT + '">\n' + "\n".join(out) + "\n</div></body></html>")

if __name__ == "__main__":
    for src in sys.argv[1:]:
        dst = os.path.splitext(src)[0] + ".html"
        io.open(dst, "w", encoding="utf-8").write(convert(src))
        print("saved", dst)
