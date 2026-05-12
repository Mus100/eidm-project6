# =====================================================
# PUBMED COLLECTOR - PRÊT À L'EMPLOI pour m8380799@gmail.com
# =====================================================
import ssl
from Bio import Entrez
import pandas as pd
import time

# ✅ FIX SSL WINDOWS (fonctionne à 100%)
ssl._create_default_https_context = ssl._create_unverified_context

class PubMedCollector:
    def __init__(self, email):
        Entrez.email = email
        print(f"✅ Email configuré: {email}")

    def get_articles(self, query, n=5):
        print(f"\n🔍 Recherche PubMed: '{query}'")
        print("-" * 50)
        
        # 1. Trouver les articles
        handle = Entrez.esearch(db="pubmed", term=query, retmax=n)
        record = Entrez.read(handle)
        handle.close()
        ids = record["IdList"][:n]
        print(f"📊 {len(ids)} articles trouvés")
        
        if not ids:
            print("❌ Aucun résultat")
            return pd.DataFrame()
        
        # 2. Récupérer les détails
        articles = []
        for i, pmid in enumerate(ids, 1):
            print(f"📥 {i}/{len(ids)} - PMID: {pmid}")
            
            try:
                handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
                xml = Entrez.read(handle)
                handle.close()
                
                # Extraction des infos
                art = xml['PubmedArticle'][0]['MedlineCitation']['Article']
                
                # Titre
                title = str(art.get('ArticleTitle', 'N/A'))
                
                # Auteurs (3 max)
                authors = []
                for a in art.get('AuthorList', [])[:3]:
                    ln = a.get('LastName', '')
                    fn = a.get('Initials', '') or a.get('ForeName', '')[:2]
                    if ln: 
                        authors.append(f"{ln}, {fn}")
                authors_str = '; '.join(authors) or 'N/A'
                
                # Résumé
                abstract_parts = art.get('Abstract', {}).get('AbstractText', [])
                abstract = ' '.join(str(p) for p in abstract_parts)
                if len(abstract) > 300: abstract = abstract[:300] + "..."
                
                # Journal et année
                journal = art.get('Journal', {}).get('Title', 'N/A')
                year_str = art.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})
                year = year_str.get('Year', 'N/A')
                
                articles.append({
                    'PMID': pmid,
                    'Titre': title,
                    'Auteurs': authors_str,
                    'Résumé': abstract or 'N/A',
                    'Journal': journal,
                    'Année': year
                })
                
                time.sleep(0.6)  # Respect des limites NCBI
                
            except Exception as e:
                print(f"⚠️ Erreur {pmid}: {e}")
                continue
        
        df = pd.DataFrame(articles)
        return df

# 🚀 LANCEMENT AUTOMATIQUE
if __name__ == "__main__":
    print("🔬 PUBMED COLLECTOR v2.0")
    print("=" * 50)
    
    # ✅ TON EMAIL DÉJÀ CONFIGURÉ
    EMAIL = "m8380799@gmail.com"
    
    collect = PubMedCollector(EMAIL)
    
    # Test avec CANCER (5 articles)
    print("\n1️⃣ Collecte CANCER...")
    df_cancer = collect.get_articles("cancer", 5)
    
    # Test avec COVID (3 articles)
    print("\n2️⃣ Collecte COVID...")
    df_covid = collect.get_articles("COVID-19 vaccine", 3)
    
    # Sauvegarde
    if not df_cancer.empty:
        filename = "MES_ARTICLES_CANCER.csv"
        df_cancer.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n🎉 FICHIER CRÉÉ: {filename}")
        print("\n📋 Aperçu Cancer:")
        print(df_cancer[['Titre', 'Auteurs', 'Année']].head())
    
    if not df_covid.empty:
        filename2 = "MES_ARTICLES_COVID.csv"
        df_covid.to_csv(filename2, index=False, encoding='utf-8-sig')
        print(f"\n🎉 FICHIER CRÉÉ: {filename2}")