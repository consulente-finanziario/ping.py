#!/usr/bin/env python3
"""
Script per segnalare le sitemap a Yandex e ai servizi RPC selezionati.
Genera un report in report-ping.txt, mostra in console il log in tempo reale,
mostra l'URL pingato e attende un "Premi Invio" al termine per chiudere lo script.
"""

import urllib.request
import urllib.parse
import xmlrpc.client
import logging
import sys

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)

# Configurazione siti e percorsi sitemap
domains = {
    "ciemmezeta.it": "/sitemap_index.xml",
    "centrostuditelesio.it": "/sitemap_index.xml",
    "lanzonicarburatori.com": "/sitemap.xml",
    "cerutisrl.it": "/sitemap_index.xml",
    "consulente-finanziario.org": "/sitemap_index.xml",
}

# Endpoint di ping motore di ricerca (solo Yandex)
search_engines = {
    "Yandex": "http://webmaster.yandex.ru/ping?sitemap=",
}

# Servizi RPC da contattare
rpc_services = {
    "Ping-O-Matic": "http://rpc.pingomatic.com",
    "Twingly": "http://rpc.twingly.com",
    "Blo.gs": "http://ping.blo.gs/",
}

report_lines = []
total_domains = len(domains)

for idx, (domain, sitemap_path) in enumerate(domains.items(), start=1):
    sitemap_url = f"https://{domain}{sitemap_path}"
    site_url = f"https://{domain}"
    header = f"=== {domain} ({idx}/{total_domains}) ==="
    logging.info(header)
    report_lines.append(header)

    # Ping motore di ricerca (sitemap)
    for name, endpoint in search_engines.items():
        ping_url = endpoint + urllib.parse.quote_plus(sitemap_url)
        try:
            with urllib.request.urlopen(ping_url) as response:
                status = response.status
                msg = f"{name} ping [{ping_url}]: HTTP {status}"
                logging.info(msg)
                report_lines.append(msg)
        except Exception as e:
            msg = f"{name} ping error on [{ping_url}]: {e}"
            logging.error(msg)
            report_lines.append(msg)

    # Segnalazione a servizi RPC (site e sitemap)
    for name, endpoint in rpc_services.items():
        try:
            client = xmlrpc.client.ServerProxy(endpoint)
            result = client.weblogUpdates.extendedPing(domain, site_url, sitemap_url)
            msg = (f"{name} RPC extendedPing to {endpoint} "
                   f"[site: {site_url}, sitemap: {sitemap_url}]: {result}")
            logging.info(msg)
            report_lines.append(msg)
        except Exception as e:
            msg = (f"{name} RPC error on {endpoint} "
                   f"[site: {site_url}, sitemap: {sitemap_url}]: {e}")
            logging.error(msg)
            report_lines.append(msg)

    report_lines.append("")

# Scrittura report su file
report_file = "report-ping.txt"
with open(report_file, "w") as f:
    f.write("\n".join(report_lines))

logging.info(f"Report scritto in {report_file}")

# Attendi input per chiudere
input("\nOperazione completata. Premi Invio per chiudere...")
