import subprocess
import sys

# Define the URLs and their prefixes for the output files
urls = {
    'landing': 'http://localhost:8000/',
    'haqqimizda': 'http://localhost:8000/haqqimizda/',
    'faq': 'http://localhost:8000/faq/'
}

for name, url in urls.items():
    print(f"Running audits for {name} ({url})")
    
    # Desktop
    cmd_desktop = [
        "npx", "-y", "lighthouse", url,
        "--output=html", "--output=json",
        f"--output-path=./lighthouse-reports/{name}-desktop",
        "--preset=desktop",
        "--chrome-flags=--headless"
    ]
    print(" ".join(cmd_desktop))
    subprocess.run(cmd_desktop, shell=True)
    
    # Mobile
    cmd_mobile = [
        "npx", "-y", "lighthouse", url,
        "--output=html", "--output=json",
        f"--output-path=./lighthouse-reports/{name}-mobile",
        "--chrome-flags=--headless"
    ]
    print(" ".join(cmd_mobile))
    subprocess.run(cmd_mobile, shell=True)

print("All audits completed!")
