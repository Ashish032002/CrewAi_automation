# Financial News Crew 📰

An automated financial news aggregation and distribution system powered by AI agents using the CrewAI framework. This project collects, analyzes, translates, and distributes financial news summaries across multiple channels and languages.

## 🌟 Features

- Automated collection of recent financial news
- AI-powered news analysis and summarization
- Multi-language translation support (Hindi, Tamil, and Hebrew)
- Multiple distribution channels (Email and Telegram)
- Scheduled daily updates
- PDF report generation with proper RTL support for Hebrew

## 🤖 AI Models Used

- News Collection & Distribution: Mixtral-8x7B-Instruct
- News Analysis: Llama-2-70b
- Translation: mBART-large-50

## 🛠️ Prerequisites

- Python 3.8+
- Hugging Face API access
- Brevo (formerly Sendinblue) account for email distribution
- Telegram Bot token and channel
- News API access

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Ashish032002/CrewAi_automation/.git
cd financial-news-crew
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```env
HUGGINGFACE_API_KEY=your_huggingface_token
NEWS_API_KEY=your_news_api_key
BREVO_API_KEY=your_brevo_api_key
SENDER_EMAIL=your_sender_email
RECIPIENT_EMAIL=your_recipient_email
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
```

## 🚀 Usage

Run the main script to start the scheduled news aggregation:

```bash
python financial_news_crew.py
```

The script will:
1. Collect financial news every hour
2. Generate a 500-word summary
3. Translate the summary into multiple languages
4. Generate PDF reports
5. Distribute reports via email and Telegram
6. Run automatically at 16:30 EST daily

## 📋 Project Structure

```
financial-news-crew/
├── financial_news_crew.py  # Main script
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## 🔒 Security Note

- Never commit your `.env` file to version control
- Rotate API keys regularly
- Monitor API usage to stay within limits
- Validate and sanitize all input data

## 📝 Required Dependencies

```
crewai
python-dotenv
schedule
reportlab
brevo-sdk
python-telegram-bot
litellm
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Always verify financial information from multiple sources before making any financial decisions.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the AI agent framework
- Hugging Face for providing the language models
- Various open-source libraries that made this project possible
