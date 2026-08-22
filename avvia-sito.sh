#!/bin/bash
# Riavvia il sito pubblico del portolano (link temporaneo mentre il Mac è acceso)
cd "$(dirname "$0")"
pkill -f "http.server 8090" 2>/dev/null; pkill -f "cloudflared tunnel" 2>/dev/null
(nohup python3 -m http.server 8090 > /tmp/http_paesi.log 2>&1 &)
(nohup cloudflared tunnel --url http://localhost:8090 > /tmp/tunnel.log 2>&1 &)
sleep 8
echo "🔗 Il tuo link: $(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/tunnel.log | head -1)"
echo "Apri /paesi.html"
