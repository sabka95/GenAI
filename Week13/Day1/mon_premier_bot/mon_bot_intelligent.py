import os 
import datetime
import time 

# --- SIMULATION MCP : La Classe Contexte (pour les notifications de progrès) ---
class ContexteSimule:
 """
 Simule l'objet 'contexte' que les outils peuvent utiliser
 pour envoyer des notifications (comme ctx.info() en MCP).
 """
 def info(self, message):
    # Affichez le message précédé de " [NOTIFICATION] "
    print(f" [NOTIFICATION] {message}")
    # Ajoutez une petite pause pour simuler un traitement (0.5 secondes)
    time.sleep(0.5)
# --- SIMULATION MCP : Les Fonctions Outils (ce sont nos 'APIs' internes) ---
# Nous définirons nos outils ici à l'étape suivante.

def recherche_web_simulee(sujet_de_recherche):
    print(f" -> Outil 'recherche_web_simulee' appelé pour : '{sujet_de_recherche}'")

    articles_trouves = [
        {
            "titre": "Les secrets d'une bonne hydratation",
            "url": "http://fauxsite.com/hydratation",
            "texte": (
                "Boire de l'eau est essentiel pour notre corps. "
                "Cela aide à réguler la température corporelle, "
                "à transporter les nutriments et à éliminer les toxines. "
                "Pensez à boire régulièrement tout au long de la journée."
            ),
        },
        {
            "titre": "L'importance du sommeil pour l'énergie",
            "url": "http://fauxsite.com/sommeil",
            "texte": (
                "Un sommeil de qualité est crucial pour la récupération physique et mentale. "
                "Il influence directement notre humeur, notre concentration et notre système immunitaire. "
                "Établir une routine de sommeil peut grandement améliorer votre quotidien."
            ),
        },
    ]

    return {"resultats": articles_trouves}


def resumer_avec_llm_simule(sujet_du_briefing, liste_articles, ctx: ContexteSimule):

    ctx.info("Démarrage du résumé avec le LLM simulé...")
    time.sleep(1)  

    resume_texte = f"=== Briefing Généré (LLM Simulé) ===\nSujet : {sujet_du_briefing}\n\n"
    resume_texte += "Points Clés (Générés) :\n"

    sources_pour_llm = []

    for i, article in enumerate(liste_articles):

        ctx.info(f"Analyse de l'article {i+1} : {article['titre']}")
        premiere_phrase = article["texte"].split(".")[0].strip() + "."
        resume_texte += f"- {premiere_phrase} [Source {i+1}]\n"
        sources_pour_llm.append(f"[Source {i+1}] {article['titre']} - {article['url']}")
        time.sleep(0.3)

    resume_texte += "\nSources Utilisées :\n" + "\n".join(sources_pour_llm)
    ctx.info("Résumé complété avec succès !")

    return {"briefing_complet": resume_texte}


def enregistrer_fichier(nom_fichier, contenu_briefing):
    dossier_sortie = "briefings_generes"

    os.makedirs(dossier_sortie, exist_ok=True)
    chemin_complet = os.path.join(dossier_sortie, nom_fichier)

    try:
        with open(chemin_complet, "w", encoding="utf-8") as f:
            f.write(contenu_briefing)
        print(f" -> Outil 'enregistrer_fichier' : Briefing enregistré dans '{chemin_complet}'")

        return {"chemin": chemin_complet}

    except Exception as e:
        print(f"Erreur lors de l'enregistrement du briefing : {e}")
        return {"chemin": None}


def lister_outils_mcp_simule():
    print(" -> Outil 'lister_outils_mcp_simule' appelé.")
    outils_disponibles = [
        {"nom": "recherche_web_simulee", "description": "Recherche des articles sur un sujet donné."},
        {"nom": "resumer_avec_llm_simule", "description": "Génère un résumé avec un LLM simulé et envoie des notifications."},
        {"nom": "enregistrer_fichier", "description": "Sauvegarde un contenu dans un fichier texte."},
    ]
    return {"outils": outils_disponibles}


if __name__ == "__main__":
    print("--- Démarrage du Client MCP Simulé ---")

    # --- Simulation MCP : Handshake (Poignée de Main) ---
    print("\nSIMULATION MCP : Effectuation du 'handshake' (établissement de la connexion)...")
    time.sleep(1)  # Simule le temps du handshake
    print("SIMULATION MCP : Handshake terminé. La 'session' est établie.")

    # --- Simulation MCP : Découverte des outils ---
    print("\nSIMULATION MCP : Demande des outils disponibles au 'serveur'...")
    resultats_decouverte = lister_outils_mcp_simule()
    print("SIMULATION MCP : Outils 'découverts' :")
    for outil in resultats_decouverte["outils"]:
        print(f" - {outil['nom']}: {outil['description']}")

    sujet_utilisateur = input("\nQuel sujet voulez-vous briefer (ex: 'écologie urbaine') ? ").strip()
    if not sujet_utilisateur:
        sujet_utilisateur = "Santé et bien-être"  
        print(f"Aucun sujet entré, utilisant le défaut : '{sujet_utilisateur}'")

    print(f"\nLe bot va générer un briefing pour : '{sujet_utilisateur}'")

    # 1. Appel de l'outil de recherche simulée
    print("\n1. Appel de l'outil 'recherche_web_simulee'...")
    result_recherche = recherche_web_simulee(sujet_utilisateur)
    articles = result_recherche.get("resultats", []) 

    if not articles:
        print(" -> Aucun article simulé trouvé. Arrêt du processus.")
    else:
        print(f" -> {len(articles)} articles simulés trouvés.")

        # 2. Appel de l'outil de résumé LLM simulé, en passant le CONTEXTE
        print("\n2. Appel de l'outil 'resumer_avec_llm_simule' (regardez les NOTIFICATIONS !) ...")
        contexte_pour_llm = ContexteSimule()
        result_resume = resumer_avec_llm_simule(sujet_utilisateur, articles, contexte_pour_llm)
        contenu_briefing = result_resume.get("briefing_complet", "Erreur: Contenu non généré.")

        # 3. Appel de l'outil d'enregistrement
        print("\n3. Appel de l'outil 'enregistrer_fichier'...")
        date_du_jour = datetime.date.today().isoformat()

        # Nettoyer le sujet pour le nom de fichier (supprimer espaces, caractères spéciaux simples)
        nom_fichier_propre = (
            sujet_utilisateur.replace(" ", "_")
            .replace("'", "")
            .replace('"', "")
            .lower()
        )
        nom_fichier_briefing = f"briefing_{nom_fichier_propre}_{date_du_jour}.txt"
        result_enregistrement = enregistrer_fichier(nom_fichier_briefing, contenu_briefing)
        chemin_final = result_enregistrement.get("chemin")

        print("\n--- Processus du Bot Intelligent Simulé Terminé ---")
        if chemin_final:
            print(f"Votre briefing est prêt ! Ouvrez le fichier : '{chemin_final}'")
        else:
            print("Une erreur est survenue lors de la création du briefing.")



