# BookCollection

Python scripts for adding data about books to Notion library

## Prerequisites

#### Python version ≥ 3.10

#### Packages:
```bash
pip install beautifulsoup4
pip install python-dotenv
pip install requests
pip install selenium
```

#### ChromeDriver
[Download](https://googlechromelabs.github.io/chrome-for-testing/) `chromedriver.exe` and add it to `path`

#### Setup .env
1. [Create a Notion Integration](https://www.notion.so/profile/integrations)
2. Copy Internal Integration Secret to **`NOTION_TOKEN=secret_...`**
3. Add the Integration to your Notion Database (go to `...` and `+ Add connections`)
4. From URL copy part in between `notion.so/` and `?v=` to **`DATABASE_ID=`**
5. Create API key at [Google Keys & Credentials](https://console.cloud.google.com/apis/credentials) and copy it to **`GOOGLE_API_KEY=`**

You can change which language file to use via `LANGUAGE=` (Only implemented one is "en")  
You can change which sources will be used for data retrieval wia `SOURCE_...=`

## Running the application
If you are using VS Code, you can use the configuration from `launch.json`.  
Otherwise you can run it from terminal `python -m app.src.main`