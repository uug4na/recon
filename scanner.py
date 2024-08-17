from .commands import run_command
import os

class Scanner:
    def __init__(self, domain):
        self.domain = domain
        self.target_dir = f"../targets/{domain}"

    def setup_directory(self):
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        os.chdir(self.target_dir)
        print(f"[+] Directory changed to {os.path.abspath(os.getcwd())}")

    def subdomain_enum(self):
        run_command(f"subfinder -d {self.domain} -all -o subs.txt")
        run_command(f"ffuf -d https://FUZZ.{self.domain} -w ~/bug/wordlists/subdomains-top1million-110000.txt -o ffuf-subs.txt")
        run_command(f"assetfinder -subs-only {self.domain} >> subs.txt")
        run_command(f"crtsh -d {self.domain} >> subs.txt")
        run_command(f"findomain -t {self.domain} >> findomain.txt")
        run_command(f"sort subs.txt | uniq > unique-subs.txt")

    def httpx_check(self):
        print(f"[+] Directory changed to {os.path.abspath(os.getcwd())}")
        run_command("httpx -l subs.txt -ports 80,8080,8000,8888 -fc 403,401 > unique-subs.txt")

    def nuclei_run(self):
        print("[+] Nuclei started")
        run_command("nuclei -l unique-subs.txt -t ../../templates/nuclei-templates -o nuclei.txt")

    def find_params(self):
        run_command("paramspider -l unique-subs.txt > params.txt")

    def waymore(self):
        run_command(f"waymore -i {self.domain} -mode U -mc 200 -oR ./waymore-result -oU ./{self.domain}-urls.txt")

    def nmap(self):
        run_command(f"nmap ")

    def start_scan(self):
        self.setup_directory()
        print("[+] Subdomain Enum Started")
        self.subdomain_enum()
        self.httpx_check()
        # self.find_params()
        self.waymore()
        self.nuclei_run()
