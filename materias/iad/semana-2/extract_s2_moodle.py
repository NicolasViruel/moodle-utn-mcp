import re
import html
from pathlib import Path

text = Path(r"C:\Users\Pollo\.cursor\projects\c-Users-Pollo-moodle-utn-mcp\agent-tools\7594d51f-3e02-427c-9f3a-eed98ae029aa.txt").read_text(encoding="utf-8")
i = text.find("Unidad N° 1 - Semana 2")
chunk = text[i : i + 20000]
plain = html.unescape(re.sub(r"<[^>]+>", "\n", chunk))
Path(__file__).with_name("s2-moodle-extract.txt").write_text(plain, encoding="utf-8")
links = re.findall(r"https://tup\.sied\.utn\.edu\.ar/pluginfile\.php/[^\s\"\\]+", chunk)
print("\n".join(links))
