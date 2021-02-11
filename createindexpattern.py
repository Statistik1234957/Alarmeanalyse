# Script fetches all elasticsearch indices and then registers index patterns

import argparse, requests
from config_utils import ConfigUtils


def create_index_pattern(indexFilter):

    # get path from config file
    cfg = ConfigUtils()
    elastic_url = cfg.read_cfgvalue("elasticsearch", "elasticurl")
    kibana_url = cfg.read_cfgvalue("kibana", "kibanaurl")
    space = cfg.read_cfgvalue("kibana", "selectedspace")

    parser = argparse.ArgumentParser(
        description="Create automatically index patterns, from elasticsearch indices."
    )
    parser.add_argument("elasticsearch_url", type=str, help="elasticsearch full URL")
    parser.add_argument("kibana_url", type=str, help="kibana full URL")

    args = parser.parse_args([elastic_url, kibana_url])

    try:
        indices = requests.get(
            args.elasticsearch_url + "/_cat/indices?format=json",
            verify=False,
            proxies={"http": "", "https": ""},
        ).json()

        try:

            for index in indices:

                #filters for given index
                if str.startswith(index["index"], indexFilter):

                    print()
                    print("Selected Index: " + index["index"])

                    payload = {"attributes": {"title": index["index"]}}

                    name = str.replace(index["index"], indexFilter, "")

                    requests.post(

                        args.kibana_url + "/s/" + space +"/api/saved_objects/index-pattern/" + name,
                        json=payload,
                        headers={"kbn-xsrf": "true"},
                        proxies={"http": "", "https": ""},
                        verify=False,
                    )
                    print("Sucessfully created Index Pattern :" + index["index"])

        except TypeError:
            print()
            print("Your given argument is invalid. PLease pass an Indexname or at least a part of it as a String.")


    except requests.exceptions.InvalidURL:
        print("Invalid URL, please check the given URLS.")

    return None


