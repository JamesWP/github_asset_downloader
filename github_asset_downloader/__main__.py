import requests
import sys

def main():



    org = "FRUK-Simulator"
    repo = "Simulator"
    asset_name = 'artifact.zip'

    url = f"https://api.github.com/repos/{org}/{repo}/releases/latest"

    response = requests.get(url)
    if response and response.status_code == 200:
        content = response.json()
        release = content['name']
        assets = [ asset for asset in content['assets'] if asset['name'] == asset_name ]
        if len(assets) != 1:
            print("Multiple assets", file=sys.stderr)
            return 2
        [asset] = assets
        download_url = asset['browser_download_url']
        name = asset['name']
        print("Release", release, file=sys.stderr)
        print("Download url", download_url, file=sys.stderr)
        print("Download name", name, file=sys.stderr)
        print(download_url)
        return 0
    else:
        print("Error response", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
