import requests
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("org", type=str, help="github org")
    parser.add_argument("repo", type=str, help="github repo")
    parser.add_argument("--asset-name", type=str, default="artifact.zip", help="name of artifact")
    parser.add_argument("-o", "--output", type=str, default="artifact.zip", help="name of artifact download location")
    parser.add_argument("-d", "--download", action="store_true", default=False, help="do download")
    parser.add_argument("-p", "--persist", action="store_true", default=False, help="save etag file")
    parser.add_argument("-e", "--etag", type=str, help="etag of existing download, only download if asset is different")
    parser.add_argument("-E", "--etag-output", type=str, default=".github_asset_downloader_etag", help="path of etag file to store new etag in")

    return parser.parse_args()

def get_latest_release_url(org, repo, asset_name):
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
        return download_url
    else:
        raise ValueError("Error getting latest release")

def download_file(url, etag, dest_path):
    headers = {}
    if etag:
        headers["If-None-Match"] = etag
    response = requests.get(url, stream=True, headers=headers)
    if response and response.status_code == 200:
        dest_file = open(dest_path, "wb")
        for chunk in response.iter_content(chunk_size=4096):
            dest_file.write(chunk)
        return response.headers.get("etag")
    elif response and response.status_code == 304: # not modified
        print("Download skipped", file=sys.stderr)
        return response.headers.get("etag")
    else:
        raise ValueError("unable to get asset", url, response.raw)


def main():
    args = parse_args()

    try:
        asset_url = get_latest_release_url(args.org, args.repo, args.asset_name)

        if args.download:
            etag = download_file(asset_url, args.etag, args.output)

            if args.persist:
                with open(args.etag_output, "w") as etag_file:
                    etag_file.write(etag)

            print(etag)
        else:
            print(asset_url)
        return 0
    except ValueError as e:
        print("No release found:", e, file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
