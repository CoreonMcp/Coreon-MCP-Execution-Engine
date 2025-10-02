from service.llm import generate_reply_from_results
from utils.kline_text_renderer import MCPKlineRendererPro
from utils.common import extract_step_recent_data

INTENT_KEYWORDS = {
    "market_analysis": ["行情", "走势", "价格", "涨跌", "k线", "报价", "price", "chart", "market", "trend", "quote", "valuation"],
    "news": ["新闻", "资讯", "update", "announcement", "headline"],
    "social": ["粉丝", "twitter", "followers", "社交", "telegram", "discord"],
    # 未来可以继续加
}

def build_tool_summary(results: list) -> str:

    lines = []
    for step in results:
        tool = step['call']['tool']
        function = step['call']['function']
        result = step['result']

        lines.append(f"{tool}.{function}.{result}")
    return "\n".join(lines)

def build_reply_prompt(user_input: str, tool_summary: str, lang: str = "en") -> str:
    if lang == "unknown":
        return (
            f"The user asked: \"{user_input}\"\n"
            f"The following information was retrieved using available tools:\n{tool_summary}\n"
            f"Now, based on the above context, please provide a fluent and natural response to the user"
        )

    return (
        f"The user asked: \"{user_input}\"\n"
        f"The following information was retrieved using available tools:\n{tool_summary}\n"
        f"Now, please provide a response in fluent and natural {lang}, based on the context above."
    )

def get_system_prompt(intent: str) -> str:
    if intent == "market_analysis":
        return """
   You are a professional crypto trading analyst with expert-level understanding of technical indicators. Your job is to analyze token market data and provide accurate, actionable buy/sell price zones.

You will receive multiple sections of data:

1️⃣ Technical Indicator Data:
• Short-Term Data ("short_summary", "short_interval", "short_recent_data") — typically 15-minute timeframe.
• Long-Term Data ("long_summary", "long_interval", "long_recent_data") — typically 1-day timeframe.

Each section includes multiple indicators:
• EMA (5, 10, 20, 50)
• RSI (Relative Strength Index)
• MACD (MACD, MACDh, MACDs)
• STOCH (STOCHk, STOCHd)
• CCI
• OBV (On-Balance Volume)
• ATR (Average True Range)
• Bollinger Bands (BBL, BBM, BBU, BBB, BBP)
• Amplitude, Highest/Lowest price, Average close price

2️⃣ News Sentiment Data (optional):
• A list of recent news headlines and summaries related to this token/project.

⸻

🧠 Your analysis task:

For short-term trading (15m interval):
• Evaluate RSI, MACD, STOCH to assess market strength.
• Suggest a reasonable short-term buy price range.
• Predict nearest resistance price.

For long-term trading (1d interval):
• Analyze overall trend, momentum, and market structure.
• Suggest a long-term buy price range.
• Predict long-term resistance level.

If news sentiment data is available, incorporate it into your evaluation and adjust your analysis accordingly.

⚠ Important Notes:
• RSI < 30 = oversold (potential buy zone); RSI > 70 = overbought (risk zone).
• Use multiple indicator cross-confirmation: EMA position, MACD crossover, Bollinger squeeze, etc.
• Always output price suggestions as concrete USD ranges.
• Do not output phrases like "cannot predict" — always provide your best estimate.
• Be concise, professional and actionable.

⸻

📝 Output Format (strictly follow):

Short-Term Analysis:
• Recommended Buy Price: $xxx ~ $xxx

Long-Term Analysis:
• Recommended Buy Price: $xxx ~ $xxx

⸻

Now begin your analysis based on the following full data payload:

{{input_data_json}}
    """
    else:
        return """
    You are an intelligent assistant. Based on the provided data, please generate a clear, natural, and human-like response.
    """

def classify_user_intent(user_input: str) -> str:
    user_input_lower = user_input.lower()

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in user_input_lower:
                return intent

    return "general"

def generate_final_reply(user_input: str, results: list, lang: str = "en") -> str:
    user_intent = classify_user_intent(user_input)
    user_prompt = get_system_prompt(user_intent)

    summary = build_tool_summary(results)
    prompt = build_reply_prompt(user_prompt, summary, lang)

    return generate_reply_from_results(prompt)