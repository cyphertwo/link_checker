import asyncio
from concurrent.futures import ThreadPoolExecutor
from checker import check_post, check_link

MAX_WORKERS = 5  # nombre de threads simultanés

def verify_row(row):
    """
    Vérifie un post et un lien pour une entrée dictionnaire.
    Clés standard attendues : 'forum_url', 'keyword', 'target_url'
    """
    forum_url = row['forum_url']
    keyword = row['keyword']
    target_url = row['target_url']

    post_ok = check_post(forum_url, keyword)
    link_ok = check_link(forum_url, target_url) if post_ok else False

    return {
        "forum_url": forum_url,
        "target_url": target_url,
        "keyword": keyword,
        "post_ok": post_ok,
        "link_ok": link_ok
    }

async def batch_verify(data_list):
    """Vérifie toutes les entrées d'une liste de dictionnaires en parallèle"""
    results = []

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        tasks = [loop.run_in_executor(executor, verify_row, row) for row in data_list]
        for result in await asyncio.gather(*tasks):
            results.append(result)
    return results

if __name__ == "__main__":
    # Exemple de données de test avec clés standardisées
    test_data = [
        {"target_url": "https://valore2euro.it/", "forum_url": "https://modelingtime.com/forum/viewtopic.php?t=24362", "keyword": "Joakin"},
        {"target_url": "https://valore2euro.it/categoria-prodotto/anno/", "forum_url": "https://www.noieilmutamento.net/viewtopic.php?t=7276", "keyword": "m1guel"},
        {"target_url": "https://valore2euro.it/categoria-prodotto/anno/", "forum_url": "https://www.forumtromba.com/viewtopic.php?t=3883", "keyword": "David61"},
        {"target_url": "https://valore2euro.it/", "forum_url": "https://www.myhelpforum.net/viewtopic.php?f=57&t=26198", "keyword": "Karl0s"},
        {"target_url": "https://valore2euro.it/", "forum_url": "https://www.genesisforum.it/viewtopic.php?f=32&t=9902", "keyword": "Nola"},
    ]

    import time
    start = time.time()
    results = asyncio.run(batch_verify(test_data))
    for r in results:
        print(r)
    #print("Temps total:", time.time() - start)
