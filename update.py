
import urllib.request
import base64

INPUT = "config.txt"
OUTPUT = "subscription.txt"

protocols = (
    "vless://", "vmess://", "trojan://",
    "ss://", "hysteria2://", "tuic://"
)

configs = set()

with open(INPUT, "r", encoding="utf-8") as f:
    sources = [
        line.strip() for line in f
        if line.strip().startswith("http")
    ]

for url in sources:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        data = urllib.request.urlopen(
            req, timeout=20
        ).read().decode("utf-8", errors="ignore")

        try:
            decoded = base64.b64decode(
                data + "=" * (-len(data) % 4)
            ).decode("utf-8")
            if "://" in decoded:
                data = decoded
        except Exception:
            pass

        for line in data.splitlines():
            line = line.strip()
            if line.startswith(protocols):
                configs.add(line)

    except Exception as e:
        print("Source failed:", url, str(e))

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(configs)))

print("Total configs:", len(configs))
