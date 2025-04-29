# 🔍 URL Parameter Extractor & Payload Injector

This Python script takes a website URL as input, extracts all unique URLs on the page that contain **query parameters**, and then **injects a payload** (`../../../etc/passwd`) into those parameters to test for possible Local File Inclusion (LFI) vulnerabilities.

## 📌 Features

- Crawls the given URL and collects all internal links with query parameters.
- Filters URLs to ensure only **one per unique parameter** is tested.
- Injects a payload into the parameter value.
- Displays the HTTP response for each injected URL (first 1000 characters).

## 💡 Use Case

This is helpful for:
- Web vulnerability testing (e.g., LFI).
- Bug bounty automation.
- Manual recon of input-handling endpoints.

## 🛠 Requirements

Install the required packages:

```bash
pip install requests beautifulsoup4
