import yfinance as yf
import pandas as pd
import ta
import telebot
from datetime import datetime, timezone, timedelta

# --- KONFIGURASI ---
TOKEN = '8930743381:AAHFIRkpH-l7yqLhZB9q65nnpnCwKRCr9Yc'
CHAT_ID = '6905606117'
bot = telebot.TeleBot(TOKEN)

# Daftar Ticker Saham US
tickers = [
    # --- SAHAM UTAMA & TECH ---
    "AAPL", "TSLA", "NVDA", "AMD", "MSFT", "IBM", "DELL", "OKTA", "NTAP",
    "HPE", "NOW", "TEAM", "AMBA", "ASML", "BABA", "UBER", "MU", "SOFI",
    "SMCI", "IREN", "SPCE", "ASAN", "GAP", "ASTS", "QVCAQ", "AXTI",
    "ATOM", "WIT", "COIN", "BIDU", "MSTR", "HOOD", "DECK", "PYPL",
    "SANA", "AMLX", "GRAB",

    # --- ETF (PASAR & SEKTOR) ---
    "SPY", "QQQ", "VOO", "IWM", "SMH", "DIA", "XLE", "XLF", "TQQQ", "SOXL", "ARKK",

    # --- TAMBAHAN ---
    "LLY", "JPM", "XOM", "INTC", "ORCL", "JNJ", "CSCO", "COST", "MA", "CAT",
    "LRCX", "NFLX", "BAC", "ARM", "KO", "PLTR", "PG", "GE", "MS", "HSBC",
    "TXN", "GEV", "QCOM", "KLAC", "SHEL", "BHP", "PEP", "STX", "WDC", "SHOP",
    "COP", "BTI", "PLD", "BKNG", "SONY", "UL", "SPGI", "SBUX", "SPOT", "ABNB",
    "MMM", "NOC", "DDOG", "NTES", "AEP", "BKR", "NU", "DB", "NDAQ", "ADSK",
    "EBAY", "CRDO", "AIG", "SYY", "TRI", "RBLX", "RDDT", "VICI", "TWLO", "PPG",
    "CTSH", "ILMN", "HPQ", "DLTR", "ZS", "AKAM", "EXPD", "DKS", "DOCN", "BBY", "APTV",

    # --- GROWTH STOCKS ---
    "SNOW", "CRWD", "TTD", "PATH", "U", "DUOL", "APP",

    # --- DIVIDEND & BLUE CHIP ---
    "T", "VZ", "PFE", "ABBV", "MO", "WMT", "TGT",

    # --- EV & ENERGI BARU ---
    "RIVN", "LCID", "NIO", "ENPH", "SEDG", "FSLR",

    # --- FINANCE & CRYPTO RELATED ---
    "SQ", "AFRM", "UPST", "MARA", "RIOT", "CLSK",

    # --- SMALL CAP VOLATILE ---
    "IONQ", "JOBY", "ACHR", "RKLB", "LUNR"
]

@bot.message_handler(commands=['scan'])
def run_scan(message):
    total = len(tickers)
    bot.reply_to(message, f"⏳ Scanning {total} saham, harap tunggu...")

    strong_buys = []
    dips = []
    overbought = []

    for i, symbol in enumerate(tickers, 1):
        try:
            data = yf.download(symbol, period='6mo', interval='1d', progress=False)
            if data.empty or len(data) < 30: continue

            df = data.copy()
            close = df['Close'].squeeze()
            df['rsi'] = ta.momentum.rsi(close, window=14)
            macd_obj = ta.trend.MACD(close=close)
            df['macd'] = macd_obj.macd()
            df['macd_signal'] = macd_obj.macd_signal()

            rsi = float(df['rsi'].iloc[-1])
            macd = float(df['macd'].iloc[-1])
            macd_sig = float(df['macd_signal'].iloc[-1])
            price = float(close.iloc[-1])

            print(f"DEBUG: {symbol} | Price: ${price:.2f} | RSI: {rsi:.1f} | MACD_Diff: {macd - macd_sig:.2f}")

            if rsi < 30 and macd > macd_sig:
                strong_buys.append(f"✅ *{symbol}* — ${price:.2f} (RSI: {rsi:.1f})")
            elif rsi < 40:
                dips.append(f"🟡 *{symbol}* — ${price:.2f} (RSI: {rsi:.1f})")
            elif rsi > 70:
                overbought.append(f"⚠️ *{symbol}* — ${price:.2f} (RSI: {rsi:.1f})")

        except Exception as e:
            print(f"Error pada {symbol}: {e}")
            continue

    # Waktu scan selesai (WIB = UTC+7)
    WIB = timezone(timedelta(hours=7))
    scan_time = datetime.now(WIB)
    waktu_str = scan_time.strftime("%d %b %Y, %H:%M WIB")

    # Ganti progress message dengan hasil akhir
    pesan = f"📊 *HASIL SCAN PASAR* ({total} saham)\n🕒 Data diambil: {waktu_str}\n\n"

    if strong_buys:
        pesan += "🔥 *STRONG BUY (Golden Signal):*\n" + "\n".join(strong_buys) + "\n\n"

    if dips:
        pesan += "🟡 *DIP / SALE (Potensi Beli):*\n" + "\n".join(dips) + "\n\n"

    if overbought:
        pesan += "⚠️ *OVERBOUGHT (Hati-hati):*\n" + "\n".join(overbought) + "\n\n"

    if not (strong_buys or dips or overbought):
        pesan += "Pasar lagi sideways, nggak ada sinyal kuat hari ini."

    bot.reply_to(message, pesan, parse_mode='Markdown')

# --- JALANKAN BOT ---
print("Bot sedang berjalan... (Tekan Ctrl+C untuk berhenti)")
bot.polling(non_stop=True)
