# Discord Gift Link Checker

A Python script that checks the validity of Discord gift links, identifies if they are valid, invalid, or already claimed, and organizes the results accordingly. The script supports the use of proxies for improved performance and handles errors gracefully.

## Features

- Checks Discord gift links for validity.
- Identifies links as valid, invalid, or already claimed.
- Supports the use of proxies to enhance performance.
- Saves results to categorized output files.
- Configurable settings for timeouts and retries.

## Requirements

- Python 3.x
- `requests` library

## Usage

### Clone the repository

```bash
git clone https://github.com/mediax1/discord-gift-link-checker.git
cd discord-gift-checker
```
## Install required packages

You can install the required packages using pip:

```bash
pip install requests
```
### Create a configuration file:

Create a `config.json` file in the project directory with the following structure:
```json
{
    "timeout": 10,
    "threads": 5
}
```
- timeout: The maximum time (in seconds) to wait for a response from the Discord API.
- threads: The number of concurrent threads to use for checking links.

### Prepare your input files:

Create a `gift.txt` file containing the Discord gift links you want to check (one link per line).

Optionally, create a `proxies.txt` file containing proxy addresses in the format ip:port:username:password (one proxy per line).

### Run the Tool

```bash
python discord_gift_checker.py
```

### Example Output

The script will create an output directory containing the following files:
- `valid.txt`: Contains valid gift links with expiration information.
- `invalid.txt`: Contains invalid gift links.
- `already_claimed.txt`: Contains links that have already been claimed.

### User Prompts

If the `proxies.txt` file is empty or does not exist, the script will prompt you to decide whether to continue without proxies.

## Disclaimer

This tool is intended for educational purposes only. Use it responsibly and ensure that you comply with Discord's Terms of Service. The author is not responsible for any misuse or consequences arising from the use of this tool. Always respect the privacy and rights of others when using this software.

### License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.<br>Make sure to join my discord server at https://discord.gg/darkeyes