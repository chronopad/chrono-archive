title: DNXSS-over-HTTPS
value: 193
description: Do you like DNS-over-HTTPS? Well, I'm proxying `https://dns.google/`! Would be cool if you can find an XSS!

Report to admin locally:
```sh
curl http://localhost:8008/report -H "Content-Type: application/json" -d '{"url":"http://proxy/"}'
```

Report to admin for the real flag:
```sh
curl https://dnxss.chal-kalmarc.tf/report -H "Content-Type: application/json" -d '{"url":"http://proxy/"}'
```