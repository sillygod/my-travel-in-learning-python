import logging
from typing import Dict, Tuple, Callable, Optional
import requests

from collections import defaultdict

logging.basicConfig(level = logging.INFO) # violently enable level info to be showed.

endpoint = 'https://api.cloudflare.com/client/v4/'
api_token = ''
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_token}',
}

allows_ports = (
    2053,
    2083,
    2087,
    2096,
    8443,
)

fh_ips = ()

def get_zones_ids_domains_mapping(target_ips: Tuple) -> Dict[str, str]:
    """find the domains points to the target ips and arrange them as a group belong to 
    the corresponding zone id
    """
    zone_mapping = defaultdict(list)
    page_num = 1
    per_page = 100

    res = requests.get(url=f'{endpoint}zones', params={'page': page_num, 'per_page': per_page}, headers=headers).json()
    total_count = res['result_info']['total_count']

    logging.info(f"there are total {total_count} zones")
    total_page = res['result_info']['total_pages']

    while total_page >= page_num:

        for obj in res['result']:
            zone_id =obj['id']
            res = requests.get(url=f'{endpoint}zones/{zone_id}/dns_records', headers=headers).json()

            for record in res['result']:
                if record['content'] in target_ips:
                    zone_mapping[zone_id].append(record['name'])


        page_num += 1
        res = requests.get(url=f'{endpoint}zones', params={'page': page_num, 'per_page': per_page}, headers=headers).json()

    return zone_mapping 

def list_page_rules(zone_id: str, filter_func: Optional[Callable] = None):
    res = requests.get(url=f'{endpoint}zones/{zone_id}/pagerules', headers=headers).json()
    if filter_func:
        return list(filter(filter_func, res['result']))

    return [result for result in res['result']]

def change_ssl_settings(zone_id: str, mode='full'):
    res = requests.patch(url=f'{endpoint}zones/{zone_id}/settings/ssl', headers=headers, json={'value': mode}).json()
    logging.info(res)

def remove_page_rules(zone_id: str, rule_id: str):
    res = requests.delete(url=f'{endpoint}zones/{zone_id}/pagerules/{rule_id}', headers=headers).json()
    logging.info(res)

def add_https_allowed_ports_page_rules(zone_id: str, domain: str, ports: Tuple[int]) -> Dict:
    pruned_domain = '.'.join(domain.split('.')[-2:])
    # for port in ports:
    domain_cond = f'https://*{pruned_domain}:2*/' 
    # NOTE: temporarily hard code wildcard port
    # due to the limitation of the page rule's numbers
    forward_domain =  f'https://$1{pruned_domain}/'
    payload = {
        'targets': [
            {
                'target': 'url',
                'constraint': {
                    'operator': 'matches',
                    'value': domain_cond,
                }
            }
        ],
        'actions': [
            {
                'id': 'forwarding_url',
                'value': {
                    'url': forward_domain,
                    'status_code': 301,
                }
            }
        ],
        'status': 'active',
    }
    res = requests.post(url=f'{endpoint}zones/{zone_id}/pagerules', headers=headers, json=payload).json()
    logging.info(res)


if __name__ == '__main__':
    mapping = get_zones_ids_domains_mapping(fh_ips)

    target_domains = [
    ]

    # to add page rules
    # for zone_id, domains in mapping.items():
    #     logging.info(f'start working on: {zone_id}, {domains}')
    #     for domain in domains:
    #         if domain in target_domains:
    #             add_https_allowed_ports_page_rules(zone_id, domains[0], allows_ports)
    #             break

    for zone_id, domains in mapping.items():
        for domain in domains:
            if domain in target_domains:
                logging.info(f'start working on: {zone_id}, {domains}')
                change_ssl_settings(zone_id)
                break



    # to delete page rules
    # for zone_id, domains in mapping.items():
    #     rules = list_page_rules(zone_id, lambda x: x['actions'][0]['id'] == 'forwarding_url')

    #     for rule in rules:
    #         remove_page_rules(zone_id, rule['id'])