import requests
import re
import argparse
from tqdm import tqdm

def check_embedded_exists(os_release, python_version):
    url = f'https://www.python.org/ftp/python/{python_version}/python-{python_version}-embed-{os_release}.zip'
    response = requests.head(url)
    return response.status_code == 200

def get_available_versions(os_releases, chosen_os):
    response = requests.get('https://www.python.org/downloads/')
    versions = re.findall(r'Python (3\.\d+\.\d+)', response.text)
    unique_versions = sorted(set(versions), reverse=True)

    embedded_versions = []
    print(f"Checking available embedded Python versions for {chosen_os}...")
    for version in tqdm(unique_versions, desc="Versions"):
        if check_embedded_exists(chosen_os, version):
            embedded_versions.append((version, chosen_os))
    return embedded_versions




def version_link_builder(os_release, python_version):
    return f'https://www.python.org/ftp/python/{python_version}/python-{python_version}-embed-{os_release}.zip'


def download_python_embedded(os_release, python_version):
    url = version_link_builder(os_release, python_version)
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'python-{python_version}-embed-{os_release}.zip', 'wb') as f:
            f.write(response.content)
        return f'python-{python_version}-embed-{os_release}.zip'
    else:
        print(f"Embedded version not found for {os_release} {python_version}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Download Python Embedded Packages")
    parser.add_argument("--os", choices=["win32", "amd64", "arm64"], help="Operating System")
    parser.add_argument("--version", type=str, help="Python version (e.g. 3.11.3)")
    args = parser.parse_args()

    os_releases = ["win32", "amd64", "arm64"]
    if args.os is None:
        print("Choose an Operating System:")
        for idx, os_choice in enumerate(os_releases):
            print(f"{idx}: {os_choice}")
        os_index = int(input("Enter the index of the operating system you want to use: "))
        args.os = os_releases[os_index]

    if args.version is None:
        available_versions = get_available_versions(os_releases, args.os)
        print("Available Python versions with embedded packages:")
        for idx, (version, os_release) in enumerate(available_versions):
            print(f"{idx}: {version} for {os_release}")

        index = int(input("Enter the index of the version you want to download: "))
        selected_version, selected_os = available_versions[index]
    else:
        selected_version = args.version
        selected_os = args.os

    print(f"Downloading Python {selected_version} for {selected_os}")
    result = download_python_embedded(selected_os, selected_version)
    if result:
        print(f"Downloaded {result}")
    else:
        print("Download failed")
    return result

if __name__ == "__main__":
    main()
