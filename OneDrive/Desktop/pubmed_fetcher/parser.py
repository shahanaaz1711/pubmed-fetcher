from typing import Tuple, List
import xml.etree.ElementTree as ET

def parse_pubmed_xml(xml_data: str) -> List[dict]:
    root = ET.fromstring(xml_data)
    papers = []
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle")
        pmid = article.findtext(".//PMID")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        authors = []
        affiliations = []
        emails = []

        for author in article.findall(".//Author"):
            aff = author.findtext(".//AffiliationInfo/Affiliation")
            if aff:
                affiliations.append(aff)
                if "@" in aff:
                    emails.append(aff.split()[-1])
                if not any(kw in aff.lower() for kw in ["university", "college", "institute", "hospital"]):
                    authors.append(author.findtext("LastName") or "Unknown")

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(authors),
            "Company Affiliation(s)": "; ".join(affiliations),
            "Corresponding Author Email": "; ".join(emails)
        })
    return papers
