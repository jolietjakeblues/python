from java.net import URL, HttpURLConnection

def follow_redirects(original_url, max_redirects=5):
    """
    Volgt maximaal 'max_redirects' keer een HTTP-redirect (301, 302, 303, 307, 308).
    Retourneert (conn, code) van de laatste connectie.
    """
    count = 0
    url = URL(original_url)
    
    while True:
        conn = url.openConnection()
        if not isinstance(conn, HttpURLConnection):
            # Geen HTTP-verbinding, dus direct stoppen
            return (None, -1)
        
        conn.setRequestMethod("GET")
        conn.setConnectTimeout(5000)
        conn.setReadTimeout(5000)
        # Vragen om RDF (en anders wat de server geeft)
        conn.addRequestProperty("Accept",
            "application/trig,application/n-triples,application/rdf+xml,text/turtle,application/json,application/ld+json,*/*;q=0.1")

        code = conn.getResponseCode()
        
        # Check of we een redirect-code hebben
        if code in [301, 302, 303, 307, 308]:
            location = conn.getHeaderField("Location")
            if not location or count >= max_redirects:
                # Geen nieuwe Location of we hebben teveel redirects
                return (conn, code)
            url = URL(location)
            count += 1
        else:
            # Geen redirect, dus we houden hiermee op
            return (conn, code)

def check_uri(uri):
    if not uri:
        return "Geen URL"
    try:
        conn, code = follow_redirects(uri)

        # Als follow_redirects geen geldige HTTP-verbinding opleverde
        if conn is None:
            return "Nee (Geen HTTP)"

        if code == 200:
            # 200 OK, controleer Content-Type
            content_type = conn.getContentType()
            if not content_type:
                return "Ja (Geen Content-Type)"
            content_type = content_type.lower()

            # Bekende RDF-formaten
            rdf_tokens = [
                "rdf",       # application/rdf+xml
                "turtle",    # text/turtle
                "n-triples", # application/n-triples
                "ntriples",  # sommige servers
                "trig",      # application/trig
                "ld+json",   # JSON-LD
                "json",      # algemenere JSON-indicatie
            ]
            for token in rdf_tokens:
                if token in content_type:
                    return "Ja (RDF)"
            return "Ja (Non-RDF)"
        else:
            return "Nee (HTTP %d)" % code

    except Exception, e:
        return "Nee (Fout: %s)" % e

return check_uri(value)
