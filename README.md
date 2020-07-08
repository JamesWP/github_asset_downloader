# github_asset_downloader
uses the github http api to get the download link of the latest release


# usage
```bash
$ python3.8 -m github_asset_downloader
> Release Release 0eddcb2
> Download url https://github.com/FRUK-Simulator/Simulator/releases/download/0eddcb2/artifact.zip
> Download name artifact.zip
> https://github.com/FRUK-Simulator/Simulator/releases/download/0eddcb2/artifact.zip
```

```bash
$ wget $(python3.8 -m github_asset_downloader 2>/dev/null)
> artifact.zip.2                100%[=================================================>]   2.78M  3.79MB/s    in 0.7s
> 2020-07-08 18:34:47 (3.79 MB/s) - ‘artifact.zip.2’ saved [2912667/2912667]
```
