#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

BASE_URL = "https://prod.dcn.hubs.delving.org/api/oai-pmh/"

# Start request (zonder libraries buiten stdlib)
params = {
    "verb": "ListRecords",
    "metadataPrefix": "edm",
    "set": "amsterdam-museum",
}

# OAI namespace
NS_OAI = "{http://www.openarchives.org/OAI/2.0/}"

# Regex om ongeldige XML control chars te verwijderen (0x00-0x08,0x0B,0x0C,0x0E-0x1F)
INVALID_XML_CHARS = re.compile(
    r"[\x00-\x08\x0B\x0C\x0E-\x1F]"
)

out_path = "data_am.xml"
last_resp_path = "last_response_dump.xml"
num_records = 0

def build_url(base, params):
    return f"{base}?{urllib.parse.urlencode(params)}"

def clean_xml(s):
    # strip ongeldige control chars
    return INVALID_XML_CHARS.sub("", s)

# Open output en schrijf wrapper root, zodat het resultaat valide XML is
with open(out_path, "w", encoding="utf-8") as out:
    out.write("<records>\n")

    while True:
        url = build_url(BASE_URL, params)
        print(url)

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "OAI-PMH harvester (Python urllib)",
                "Accept": "application/xml, text/xml;q=0.9, */*;q=0.1",
            },
        )

        # Haal response op
        with urllib.request.urlopen(req) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read()

        # Probeer UTF-8 te decoderen; vervang ongeldige bytes
        text = raw.decode("utf-8", errors="replace")

        # Sommige servers sturen geen juiste content-type bij tijdelijke fouten.
        # Sla de response weg als hij niet op XML lijkt.
        if "<OAI-PMH" not in text and "<?xml" not in text:
            with open(last_resp_path, "w", encoding="utf-8") as dump:
                dump.write(text)
            raise RuntimeError(
                "Response lijkt geen geldige OAI-PMH XML te zijn. "
                f"Ruwe response weggeschreven naar {last_resp_path}."
            )

        # Verwijder ongeldige XML control characters
        text = clean_xml(text)

        # Parse veilig; bij fout: dump en stop
        try:
            root = ET.fromstring(text)
        except ET.ParseError as e:
            with open(last_resp_path, "w", encoding="utf-8") as dump:
                dump.write(text)
            raise RuntimeError(
                f"XML parsefout: {e}. Ruwe response weggeschreven naar {last_resp_path}."
            )

        # Schrijf alle <record>-elementen
        with open(out_path, "a", encoding="utf-8") as out_append:
            for record in root.findall(f".//{NS_OAI}record"):
                out_append.write(ET.tostring(record, encoding="unicode"))
                out_append.write("\n")
                num_records += 1

        # ResumptionToken verwerken
        rt_el = root.find(f".//{NS_OAI}resumptionToken")
        rt = ""
        if rt_el is not None and rt_el.text:
            rt = rt_el.text.strip()

        if rt:
            # Bij resumptionToken alleen verb + resumptionToken meesturen
            params = {
                "verb": "ListRecords",
                "resumptionToken": rt,
            }
        else:
            # Klaar
            break

    with open(out_path, "a", encoding="utf-8") as out_end:
        out_end.write("</records>\n")

print(f"Klaar. Totaal aantal records: {num_records}")
