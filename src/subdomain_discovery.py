import argparse
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor

from nslookup import Nslookup


class Scanner:
    def __init__(self, config):
        self.target = config.domain
        self.output_file = config.output
        self.verbose_mode = config.verbose
        self.threads = config.threads

        if config.wordlist:
            self.candidates = config.wordlist.split(',')
        else:
            with open(args.file, 'r') as candidates_file:
                self.candidates = list(filter(bool, candidates_file.read().split('\n')))

        self.dns_query = Nslookup(dns_servers=["1.1.1.1"])  # set optional Cloudflare public DNS server

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            resolver_futures = {executor.submit(self.resolve, subdomain): subdomain for subdomain in self.candidates}

            for future in futures.as_completed(resolver_futures):
                try:
                    data = future.result()
                    if self.verbose_mode:
                        print(f'{data["domain"]} - {",".join(data["answer"]) if len(data["answer"]) > 0 else "Not found"}')
                    else:
                        if len(data['answer']) > 0:
                            print(f'{data["domain"]} - {", ".join(data["answer"])}')
                except Exception as exc:
                    print(exc)

    def resolve(self, subdomain):
        domain = subdomain + '.' + self.target
        return {'domain': domain, 'answer': self.dns_query.dns_lookup(domain).answer}


def process_arguments():
    parser = argparse.ArgumentParser(prog='subdomain_discovery.py', description='Dictionary based subdomain discovery')

    parser.add_argument('-d', '--domain', help='Target domain', required=True)
    parser.add_argument('-t', '--threads', help='Number of threads', required=False, type=int, default=8)
    parser.add_argument('-o', '--output', help="Write output to a file", required=False)
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help='Verbose mode', required=False)

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-w', '--wordlist', help='Wordlist. Comma separator.', required=False)
    input_group.add_argument('-f', '--file', help="Supplied wordlist file. End line separator.", required=False)

    return parser.parse_args()


if __name__ == "__main__":
    args = process_arguments()
    scan = Scanner(args)
    scan.run()
