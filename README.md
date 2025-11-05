# 🎯 Gossip-Scraper

A powerful and efficient web scraper that aggregates celebrity news and gossip from popular entertainment news websites. Built with Python, it automatically summarizes articles using AI for quick consumption.

## 🌟 Features

- Scrapes news from multiple popular celebrity news sources:
  - TMZ
  - E! Online
  - Page Six
  - Daily Mail
  - People Magazine
  - US Weekly
  - Hollywood Life
  - Perez Hilton
- AI-powered article summarization using DistilBART
- Clean text processing and formatting
- Configurable scraping parameters
- Robust error handling and retry mechanisms

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rasandu17/Gossip-Scraper.git
cd Gossip-Scraper
```

2. Install the required packages:
```bash
pip install requests beautifulsoup4 transformers torch lxml
```

### Usage

Simply run the script:
```bash
python gossip_scraper.py
```

The script will:
1. Visit each configured news source
2. Extract recent celebrity news articles
3. Generate AI summaries for longer articles
4. Save the results in a structured format

## ⚙️ Configuration

You can modify the following parameters in the script:

- `HEADERS`: User agent for web requests
- `TIMEOUT`: Request timeout in seconds
- `PAUSE_BETWEEN_SITES`: Delay between scraping different sites

## 🛠️ Technical Details

The scraper uses:
- `requests` for fetching web pages
- `BeautifulSoup4` for HTML parsing
- `transformers` library with DistilBART model for AI summarization
- Regular expressions for text cleaning

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

