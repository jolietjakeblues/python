# Zesde conversie omzetten <skos:prefLabel> en </skos:prefLabel> naar <dcterms:subject> en </dcterms:subject>
#test
import re

# Lees het RDF/XML-bestand
with open('/Users/patrickmout/Downloads/zzm/zzm_aangepast_stap5_xml.rdf', 'r') as file:
    rdf_content = file.read()

# Omzetten van <skos:prefLabel> naar <dcterms:subject>
modified_content = re.sub(r'<skos:prefLabel>(.*?)</skos:prefLabel>', r'<dcterms:subject>\1</dcterms:subject>', rdf_content)

# Schrijf het aangepaste XML-bestand
with open('/Users/patrickmout/Downloads/zzm/zzm_aangepast_stap6_xml.rdf', 'w') as file:
    file.write(modified_content)
	
	
	#TEST JOOP
