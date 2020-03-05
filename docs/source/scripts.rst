Scripts
=========================================

`Scripts` directory contain some utility scirpts which are hard to classify into modules. They are listed here.


queryWikidataProperty
#####################

This script will make use of the direct data access offered by Wikidata and save them locally. You can find a copy of the data in the `data/wikidataProperty/` directory.

::

    import requests
    from tqdm import tqdm
    with requests.Session() as s:
        for i in tqdm(range(8000)):
            url = "https://www.wikidata.org/wiki/Special:EntityData/P" + \
                str(i) + ".json"
            res = requests.get(url)
            if res.status_code == 200:
                with open("P"+str(i)+".json", "w") as fh:
                    fh.writelines(res.text)
            if i % 200 == 0:
                print("Finished {} runs".format(i))