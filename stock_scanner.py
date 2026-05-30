import telebot
import yfinance as yf
import ta
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- KONFIGURASI ---
TOKEN = '8930743381:AAHFIRkpH-l7yqLhZB9q65nnpnCwKRCr9Yc'
bot = telebot.TeleBot(TOKEN)

# --- DAFTAR TICKER US ---
tickers_us = [
    "AAPL", "TSLA", "NVDA", "AMD", "MSFT", "IBM", "DELL", "OKTA", "NTAP",
    "HPE", "NOW", "TEAM", "AMBA", "ASML", "BABA", "UBER", "MU", "SOFI",
    "SMCI", "IREN", "SPCE", "ASAN", "GAP", "ASTS", "QVCAQ", "AXTI",
    "ATOM", "WIT", "COIN", "BIDU", "MSTR", "HOOD", "DECK", "PYPL",
    "SANA", "AMLX", "GRAB",
    "SPY", "QQQ", "VOO", "IWM", "SMH", "DIA", "XLE", "XLF", "TQQQ", "SOXL", "ARKK",
    "LLY", "JPM", "XOM", "INTC", "ORCL", "JNJ", "CSCO", "COST", "MA", "CAT",
    "LRCX", "NFLX", "BAC", "ARM", "KO", "PLTR", "PG", "GE", "MS", "HSBC",
    "TXN", "GEV", "QCOM", "KLAC", "SHEL", "BHP", "PEP", "STX", "WDC", "SHOP",
    "COP", "BTI", "PLD", "BKNG", "SONY", "UL", "SPGI", "SBUX", "SPOT", "ABNB",
    "MMM", "NOC", "DDOG", "NTES", "AEP", "BKR", "NU", "DB", "NDAQ", "ADSK",
    "EBAY", "CRDO", "AIG", "SYY", "TRI", "RBLX", "RDDT", "VICI", "TWLO", "PPG",
    "CTSH", "ILMN", "HPQ", "DLTR", "ZS", "AKAM", "EXPD", "DKS", "DOCN", "BBY", "APTV",
    "SNOW", "CRWD", "TTD", "PATH", "U", "DUOL", "APP",
    "T", "VZ", "PFE", "ABBV", "MO", "WMT", "TGT",
    "RIVN", "LCID", "NIO", "ENPH", "SEDG", "FSLR",
    "SQ", "AFRM", "UPST", "MARA", "RIOT", "CLSK",
    "IONQ", "JOBY", "ACHR", "RKLB", "LUNR"
]

# --- DAFTAR TICKER IHSG (150+ saham, semua sektor) ---
tickers_ihsg = [
    # Perbankan (20)
    "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "BBTN.JK", "BRIS.JK",
    "ARTO.JK", "BNGA.JK", "NISP.JK", "BJBR.JK", "BJTM.JK", "PNBN.JK",
    "MEGA.JK", "BTPS.JK", "AGRO.JK", "BNII.JK", "SDRA.JK", "MAYA.JK",
    "NOBU.JK", "BBYB.JK",

    # Telko & Teknologi (10)
    "TLKM.JK", "ISAT.JK", "EXCL.JK", "GOTO.JK", "BUKA.JK", "EMTK.JK",
    "MTEL.JK", "DMMX.JK", "FREN.JK", "DCII.JK",

    # Konsumer — Makanan & Minuman (15)
    "UNVR.JK", "ICBP.JK", "KLBF.JK", "MYOR.JK", "INDF.JK", "ULTJ.JK",
    "DLTA.JK", "CPIN.JK", "JPFA.JK", "HMSP.JK", "GGRM.JK", "WIIM.JK",
    "ROTI.JK", "SKLT.JK", "HOKI.JK",

    # Healthcare & Farmasi (8)
    "SIDO.JK", "HEAL.JK", "TSPC.JK", "KAEF.JK", "SILO.JK", "MIKA.JK",
    "PRDA.JK", "PEVE.JK",

    # Energi Batu Bara (12)
    "ADRO.JK", "PTBA.JK", "ITMG.JK", "INDY.JK", "BYAN.JK", "HRUM.JK",
    "DSSA.JK", "BOSS.JK", "ADMR.JK", "MBAP.JK", "TOBA.JK", "DEWA.JK",

    # Mineral & Logam & Nikel (10)
    "ANTM.JK", "INCO.JK", "MDKA.JK", "TINS.JK", "PSAB.JK", "NCKL.JK",
    "BRMS.JK", "NICL.JK", "HILL.JK", "ARKO.JK",

    # Minyak & Gas (6)
    "MEDC.JK", "PGAS.JK", "ELSA.JK", "RUIS.JK", "ENRG.JK", "BIPI.JK",

    # Agrikultur & Perkebunan (8)
    "AALI.JK", "LSIP.JK", "SSMS.JK", "SIMP.JK", "DSNG.JK", "PALM.JK",
    "SGRO.JK", "TBLA.JK",

    # Otomotif & Industri (10)
    "ASII.JK", "UNTR.JK", "IMAS.JK", "AUTO.JK", "SMSM.JK", "GJTL.JK",
    "MASA.JK", "INTP.JK", "SMGR.JK", "WTON.JK",

    # Properti (12)
    "BSDE.JK", "CTRA.JK", "PWON.JK", "SMRA.JK", "LPKR.JK", "DILD.JK",
    "MTLA.JK", "ASRI.JK", "APLN.JK", "KIJA.JK", "JRPT.JK", "DUTI.JK",

    # Infrastruktur & Konstruksi (8)
    "PTPP.JK", "WSKT.JK", "WIKA.JK", "JSMR.JK", "TOWR.JK", "TBIG.JK",
    "AKRA.JK", "BALI.JK",

    # Kertas & Packaging (4)
    "INKP.JK", "TKIM.JK", "FASW.JK", "ALDO.JK",

    # Keuangan Non-Bank (8)
    "ADMF.JK", "BFIN.JK", "MFIN.JK", "WOMF.JK", "AMAG.JK", "MCAS.JK",
    "PANS.JK", "TRIM.JK",

    # Retail & Perdagangan (8)
    "MAPI.JK", "LPPF.JK", "AMRT.JK", "ACES.JK", "DMAS.JK", "RANC.JK",
    "HERO.JK", "MIDI.JK",

    # Media & Entertainment (5)
    "SCMA.JK", "MNCN.JK", "LINK.JK", "MSIN.JK", "INET.JK",

    # Shipping & Logistik (6)
    "TMAS.JK", "SMDR.JK", "MBSS.JK", "HITS.JK", "NELY.JK", "SOCI.JK",

    # Lainnya / Holding (5)
    "SRTG.JK", "MLPL.JK", "BHIT.JK", "BNBR.JK", "KINO.JK",
]

# --- TOP 50 BROKER TICKER (untuk /broker — lebih cepat) ---
tickers_broker = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK-B", "LLY", "JPM",
    "V", "UNH", "XOM", "MA", "JNJ", "PG", "HD", "COST", "ABBV", "MRK",
    "NFLX", "BAC", "CRM", "AMD", "ORCL", "ACN", "CVX", "KO", "PEP", "TMO",
    "AVGO", "CSCO", "MCD", "INTC", "IBM", "QCOM", "TXN", "ADBE", "NOW", "PLTR",
    "PYPL", "UBER", "COIN", "SNOW", "CRWD", "DDOG", "APP", "TTD", "SHOP", "MSTR"
]

# ============================================================
# FUNGSI HELPER
# ============================================================
def get_waktu():
    return datetime.now(timezone(timedelta(hours=7))).strftime("%d %b %Y, %H:%M WIB")

def fmt_price(price, market):
    return f"Rp{price:,.0f}" if market == "IHSG" else f"${price:,.2f}"

def build_df(symbol, period='6mo'):
    data = yf.download(symbol, period=period, interval='1d', progress=False)
    if data.empty or len(data) < 30:
        return None
    df = data.copy()
    close  = df['Close'].squeeze()
    open_  = df['Open'].squeeze()
    high   = df['High'].squeeze()
    low    = df['Low'].squeeze()
    volume = df['Volume'].squeeze()

    df['close']      = close
    df['open']       = open_
    df['high']       = high
    df['low']        = low
    df['volume']     = volume

    # --- Trend ---
    df['ma20']       = close.rolling(20).mean()
    df['ma50']       = close.rolling(50).mean()

    # --- Momentum ---
    df['rsi']        = ta.momentum.rsi(close, window=14)
    stoch            = ta.momentum.StochRSIIndicator(close, window=14, smooth1=3, smooth2=3)
    df['stoch_k']    = stoch.stochrsi_k()
    df['stoch_d']    = stoch.stochrsi_d()

    # --- MACD ---
    macd_obj         = ta.trend.MACD(close=close)
    df['macd']       = macd_obj.macd()
    df['macd_signal']= macd_obj.macd_signal()

    # --- Volatility ---
    df['atr']        = ta.volatility.average_true_range(high, low, close, window=14)
    bb               = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
    df['bb_upper']   = bb.bollinger_hband()
    df['bb_lower']   = bb.bollinger_lband()
    df['bb_mid']     = bb.bollinger_mavg()

    # --- Volume ---
    df['vol_ma20']   = volume.rolling(20).mean()
    df['obv']        = ta.volume.on_balance_volume(close, volume)

    return df

# ============================================================
# SCAN UTAMA — RSI + Stoch RSI + MACD + MA + BB + OBV
# ============================================================
def perform_scan(ticker_list, market):
    strong_buys, dips, overbought = [], [], []

    for symbol in ticker_list:
        try:
            df = build_df(symbol)
            if df is None: continue

            rsi     = float(df['rsi'].iloc[-1])
            stoch_k = float(df['stoch_k'].iloc[-1])
            macd    = float(df['macd'].iloc[-1])
            msig    = float(df['macd_signal'].iloc[-1])
            price   = float(df['close'].iloc[-1])
            ma20    = float(df['ma20'].iloc[-1])
            ma50    = float(df['ma50'].iloc[-1])
            bb_low  = float(df['bb_lower'].iloc[-1])
            bb_up   = float(df['bb_upper'].iloc[-1])
            obv_now = float(df['obv'].iloc[-1])
            obv_pre = float(df['obv'].iloc[-6])
            label   = symbol.replace('.JK', '')
            harga   = fmt_price(price, market)

            trend       = "📈" if price > ma20 > ma50 else ("📉" if price < ma20 else "➡️")
            obv_up      = obv_now > obv_pre
            near_bb_low = price <= bb_low * 1.02
            near_bb_up  = price >= bb_up * 0.98

            if rsi < 30 and macd > msig and stoch_k < 20:
                strong_buys.append(
                    f"✅ *{label}* — {harga}\n"
                    f"   RSI: {rsi:.1f} | StochRSI: {stoch_k:.1f} | OBV: {'↑' if obv_up else '↓'} {trend}"
                )
            elif rsi < 40 or near_bb_low:
                dips.append(
                    f"🟡 *{label}* — {harga} | RSI: {rsi:.1f} {trend}"
                )
            elif rsi > 70 or near_bb_up:
                overbought.append(
                    f"⚠️ *{label}* — {harga} | RSI: {rsi:.1f} {trend}"
                )
        except Exception as e:
            print(f"Error {symbol}: {e}")
            continue

    return strong_buys, dips, overbought

# ============================================================
# BSJP — Beli Sore Jual Pagi
# Fix: stoch_ok bug, tambah pola candlestick + tren mingguan
# ============================================================
def detect_candle_pattern(open_, close, high, low, open_prev, close_prev):
    body       = abs(close - open_)
    full_range = high - low
    lower_shadow = open_ - low if close >= open_ else close - low
    upper_shadow = high - close if close >= open_ else high - open_

    # Hammer: body kecil, lower shadow panjang (2x body+), muncul di area dip
    hammer = (lower_shadow >= 2 * body) and (upper_shadow <= body) and (body > 0)

    # Bullish Engulfing: candle hijau hari ini lebih besar dari candle merah kemarin
    prev_body     = abs(close_prev - open_prev)
    prev_bearish  = close_prev < open_prev
    curr_bullish  = close > open_
    engulfing     = curr_bullish and prev_bearish and body > prev_body

    if engulfing: return "🕯️ Engulfing"
    if hammer:    return "🔨 Hammer"
    return ""

def scan_bsjp(ticker_list, market):
    results = []
    for symbol in ticker_list:
        try:
            df = build_df(symbol, period='6mo')
            if df is None or len(df) < 10: continue

            rsi       = float(df['rsi'].iloc[-1])
            stoch_k   = float(df['stoch_k'].iloc[-1])
            stoch_k_p = float(df['stoch_k'].iloc[-2])
            macd      = float(df['macd'].iloc[-1])
            msig      = float(df['macd_signal'].iloc[-1])
            close     = float(df['close'].iloc[-1])
            close_p   = float(df['close'].iloc[-2])
            open_     = float(df['open'].iloc[-1])
            open_p    = float(df['open'].iloc[-2])
            high      = float(df['high'].iloc[-1])
            low       = float(df['low'].iloc[-1])
            vol       = float(df['volume'].iloc[-1])
            vol_ma    = float(df['vol_ma20'].iloc[-1])
            obv_now   = float(df['obv'].iloc[-1])
            obv_pre   = float(df['obv'].iloc[-4])
            label     = symbol.replace('.JK', '')
            harga     = fmt_price(close, market)

            # Tren mingguan: close hari ini vs 5 hari lalu
            close_5d_ago    = float(df['close'].iloc[-6])
            weekly_uptrend  = close > close_5d_ago

            vol_ratio       = vol / vol_ma if vol_ma > 0 else 0
            close_near_high = (close / high) >= 0.93 if high > 0 else False
            bullish_candle  = close > open_
            rsi_ok          = 40 <= rsi <= 68
            stoch_naik      = stoch_k > stoch_k_p          # FIX: bandingkan dengan hari sebelumnya
            macd_bullish    = macd > msig
            obv_naik        = obv_now > obv_pre
            pola            = detect_candle_pattern(open_, close, high, low, open_p, close_p)

            skor = sum([vol_ratio >= 1.5, close_near_high, bullish_candle,
                        rsi_ok, stoch_naik, macd_bullish, obv_naik, weekly_uptrend])

            if skor >= 5 and bullish_candle and vol_ratio >= 1.5:
                # Bangun alasan otomatis berdasarkan indikator yang terpicu
                alasan = []
                if vol_ratio >= 1.5:
                    alasan.append(f"volume {vol_ratio:.1f}x di atas rata-rata (minat beli tinggi)")
                if macd_bullish:
                    alasan.append("MACD di atas sinyal (momentum naik)")
                if rsi_ok:
                    alasan.append(f"RSI {rsi:.0f} di zona aman beli (belum overbought)")
                if stoch_naik:
                    alasan.append("Stochastic RSI naik (momentum mulai menguat)")
                if obv_naik:
                    alasan.append("OBV naik (akumulasi volume oleh big buyer)")
                if weekly_uptrend:
                    alasan.append("tren mingguan positif (harga lebih tinggi dari 5 hari lalu)")
                if pola:
                    alasan.append(f"pola candlestick {pola} terdeteksi (sinyal reversal bullish)")
                if close_near_high:
                    alasan.append("tutup dekat harga tertinggi hari ini (seller lemah)")

                strength = "🔥 STRONG BUY" if skor >= 7 else "✅ WORTH TO BUY"
                alasan_txt = ", ".join(alasan[:4])  # max 4 alasan supaya tidak terlalu panjang

                results.append(
                    f"🌙 *{label}* — {harga} | {strength} _(skor: {skor}/8)_\n"
                    f"   RSI: {rsi:.1f} | StochK: {stoch_k:.1f}{'↑' if stoch_naik else '↓'} | "
                    f"Vol: {vol_ratio:.1f}x | OBV ↑{' | ' + pola if pola else ''}\n"
                    f"   💬 _Layak beli karena: {alasan_txt}_"
                )
        except Exception as e:
            print(f"Error BSJP {symbol}: {e}")
            continue
    return results

# ============================================================
# ARA DETECTOR — Multi-hari momentum + upper shadow + OBV
# Tambah: cek 2-3 hari naik berturut-turut + candle tutup dekat High
# ============================================================
def scan_ara(ticker_list, market):
    results = []
    for symbol in ticker_list:
        try:
            df = build_df(symbol, period='3mo')
            if df is None or len(df) < 5: continue

            close      = float(df['close'].iloc[-1])
            close_1    = float(df['close'].iloc[-2])
            close_2    = float(df['close'].iloc[-3])
            high       = float(df['high'].iloc[-1])
            vol        = float(df['volume'].iloc[-1])
            vol_ma     = float(df['vol_ma20'].iloc[-1])
            rsi        = float(df['rsi'].iloc[-1])
            stoch_k    = float(df['stoch_k'].iloc[-1])
            obv_now    = float(df['obv'].iloc[-1])
            obv_pre    = float(df['obv'].iloc[-4])
            label      = symbol.replace('.JK', '')
            harga      = fmt_price(close, market)

            vol_ratio     = vol / vol_ma if vol_ma > 0 else 0
            pct_today     = ((close - close_1) / close_1 * 100) if close_1 > 0 else 0
            pct_yesterday = ((close_1 - close_2) / close_2 * 100) if close_2 > 0 else 0
            obv_naik      = obv_now > obv_pre

            # Upper shadow kecil: candle tutup dekat High (konfirmasi tekanan beli kuat)
            upper_shadow_kecil = (close / high) >= 0.93 if high > 0 else False

            # Momentum multi-hari: minimal 2 hari naik berturut-turut
            momentum_2hari = pct_today >= 3 and pct_yesterday >= 1

            if vol_ratio >= 3.0 and pct_today >= 5 and rsi >= 60 and obv_naik:
                alasan = []
                alasan.append(f"harga naik {pct_today:.1f}% dengan volume {vol_ratio:.1f}x rata-rata (tekanan beli masif)")
                if momentum_2hari:
                    alasan.append(f"momentum 2 hari berturut-turut naik (kemarin +{pct_yesterday:.1f}%)")
                if upper_shadow_kecil:
                    alasan.append("candle tutup dekat High (seller tidak mampu tekan harga)")
                if obv_naik:
                    alasan.append("OBV naik konsisten (big player akumulasi)")
                if rsi >= 65:
                    alasan.append(f"RSI {rsi:.0f} kuat tapi belum overbought (masih ada ruang naik)")

                strength  = "🔥 STRONG BUY" if (momentum_2hari and upper_shadow_kecil) else "✅ WORTH TO BUY"
                alasan_txt = ", ".join(alasan[:3])

                results.append(
                    f"🚀 *{label}* — {harga} | {strength}\n"
                    f"   Hari ini: +{pct_today:.1f}% | Kemarin: +{pct_yesterday:.1f}%"
                    f"{' 🔥 2 Hari Naik!' if momentum_2hari else ''}\n"
                    f"   Vol: {vol_ratio:.1f}x | RSI: {rsi:.1f} | StochK: {stoch_k:.1f}"
                    f"{' | Tutup dekat High ✅' if upper_shadow_kecil else ''}\n"
                    f"   💬 _Layak beli karena: {alasan_txt}_"
                )
        except Exception as e:
            print(f"Error ARA {symbol}: {e}")
            continue
    return results

# ============================================================
# BPJS — Scalping, deteksi Gap Up + BB Breakout + volatilitas
# Tambah: previous high breakout + body candle kuat
# ============================================================
def scan_bpjs(ticker_list, market):
    results = []
    for symbol in ticker_list:
        try:
            df = build_df(symbol, period='3mo')
            if df is None or len(df) < 5: continue

            close      = float(df['close'].iloc[-1])
            close_prev = float(df['close'].iloc[-2])
            open_      = float(df['open'].iloc[-1])
            high       = float(df['high'].iloc[-1])
            low        = float(df['low'].iloc[-1])
            high_prev  = float(df['high'].iloc[-2])
            vol        = float(df['volume'].iloc[-1])
            vol_ma     = float(df['vol_ma20'].iloc[-1])
            atr        = float(df['atr'].iloc[-1])
            atr_avg    = float(df['atr'].rolling(20).mean().iloc[-1])
            rsi        = float(df['rsi'].iloc[-1])
            stoch_k    = float(df['stoch_k'].iloc[-1])
            bb_up      = float(df['bb_upper'].iloc[-1])
            bb_low     = float(df['bb_lower'].iloc[-1])
            label      = symbol.replace('.JK', '')
            harga      = fmt_price(close, market)

            gap_up        = open_ > close_prev * 1.005
            vol_ratio     = vol / vol_ma if vol_ma > 0 else 0
            atr_ratio     = atr / atr_avg if atr_avg > 0 else 0
            rsi_ok        = 35 <= rsi <= 65
            bb_squeeze    = (bb_up - bb_low) / bb_low < 0.05

            # Breakout di atas High kemarin = konfirmasi breakout valid
            breakout_high = close > high_prev

            # Body candle kuat: body >= 50% dari total range candle
            candle_range  = high - low
            body          = abs(close - open_)
            body_kuat     = (body / candle_range) >= 0.5 if candle_range > 0 else False

            if gap_up and vol_ratio >= 1.5 and atr_ratio >= 1.2 and rsi_ok:
                gap_pct = ((open_ - close_prev) / close_prev * 100)

                # Hitung skor konfirmasi untuk label STRONG / WORTH
                skor_bpjs = sum([bb_squeeze, breakout_high, body_kuat, vol_ratio >= 2.0, atr_ratio >= 1.5])

                alasan = []
                alasan.append(f"gap up {gap_pct:.1f}% dari penutupan kemarin (momentum pagi kuat)")
                if vol_ratio >= 1.5:
                    alasan.append(f"volume {vol_ratio:.1f}x rata-rata (banyak buyer masuk)")
                if breakout_high:
                    alasan.append("harga tembus High kemarin (breakout terkonfirmasi)")
                if body_kuat:
                    alasan.append("body candle kuat ≥50% range (tekanan beli dominan)")
                if bb_squeeze:
                    alasan.append("Bollinger Bands squeeze (volatilitas siap meledak)")
                if atr_ratio >= 1.5:
                    alasan.append(f"ATR {atr_ratio:.1f}x di atas normal (volatilitas tinggi, potensi gerak besar)")

                strength   = "🔥 STRONG BUY" if skor_bpjs >= 3 else "✅ WORTH TO BUY"
                alasan_txt = ", ".join(alasan[:3])

                results.append(
                    f"⚡ *{label}* — {harga} | {strength}\n"
                    f"   Gap: +{gap_pct:.1f}% | Vol: {vol_ratio:.1f}x | ATR: {atr_ratio:.1f}x | StochK: {stoch_k:.1f}"
                    f"{' 🔥 BB Squeeze!' if bb_squeeze else ''}"
                    f"{' | BreakHigh ✅' if breakout_high else ''}"
                    f"{' | Body Kuat ✅' if body_kuat else ''}\n"
                    f"   💬 _Layak beli karena: {alasan_txt}_"
                )
        except Exception as e:
            print(f"Error BPJS {symbol}: {e}")
            continue
    return results

# ============================================================
# BANDARMOLOGY — Deteksi akumulasi diam-diam oleh big player
# Upgrade: rolling 5-hari akumulasi + analisis range candle sempit
# Fase Akumulasi: vol tinggi KONSISTEN 5 hari, range candle sempit
# Fase Markup: breakout vol masif + harga meledak
# ============================================================
def scan_bandar(ticker_list, market):
    akumulasi, markup = [], []
    for symbol in ticker_list:
        try:
            df = build_df(symbol, period='3mo')
            if df is None or len(df) < 10: continue

            close      = float(df['close'].iloc[-1])
            close_prev = float(df['close'].iloc[-2])
            high       = float(df['high'].iloc[-1])
            low        = float(df['low'].iloc[-1])
            vol        = float(df['volume'].iloc[-1])
            vol_ma     = float(df['vol_ma20'].iloc[-1])
            obv_now    = float(df['obv'].iloc[-1])
            obv_5      = float(df['obv'].iloc[-6])
            rsi        = float(df['rsi'].iloc[-1])
            label      = symbol.replace('.JK', '')
            harga      = fmt_price(close, market)

            # --- Rolling 5 hari: rata-rata vol ratio & pct perubahan harga ---
            vol_5d      = df['volume'].iloc[-5:]
            close_5d    = df['close'].iloc[-5:]
            vol_ma_5d   = df['vol_ma20'].iloc[-5:]
            high_5d     = df['high'].iloc[-5:]
            low_5d      = df['low'].iloc[-5:]

            # Rata-rata volume ratio 5 hari terakhir
            vol_ratios_5d   = (vol_5d.values / vol_ma_5d.values)
            avg_vol_ratio   = float(vol_ratios_5d.mean())

            # Rata-rata pergerakan harga harian (abs %) 5 hari
            pct_changes_5d  = close_5d.pct_change().abs().dropna() * 100
            avg_pct_change  = float(pct_changes_5d.mean())

            # Range candle sempit: (High-Low)/Close kecil = bandar jaga harga
            candle_ranges   = ((high_5d - low_5d) / close_5d) * 100
            avg_range       = float(candle_ranges.mean())

            vol_ratio_hari_ini = vol / vol_ma if vol_ma > 0 else 0
            pct_change_hari_ini = abs((close - close_prev) / close_prev * 100) if close_prev > 0 else 0
            pct_naik_hari_ini   = (close - close_prev) / close_prev * 100 if close_prev > 0 else 0
            obv_naik            = obv_now > obv_5

            # AKUMULASI: 5 hari vol di atas rata-rata, harga gerak sempit, range candle kecil
            akumulasi_rolling = avg_vol_ratio >= 1.5 and avg_pct_change < 2.0 and avg_range < 4.0
            akumulasi_hari_ini = vol_ratio_hari_ini >= 2.0 and pct_change_hari_ini < 2.0

            if (akumulasi_rolling or akumulasi_hari_ini) and obv_naik:
                durasi = "5 Hari" if akumulasi_rolling else "Hari Ini"
                akumulasi.append(
                    f"🏦 *{label}* — {harga} _({durasi})_\n"
                    f"   Vol avg 5H: {avg_vol_ratio:.1f}x | Range candle: {avg_range:.1f}% | "
                    f"Harga gerak: {avg_pct_change:.1f}% | OBV ↑"
                )

            # MARKUP: vol masif hari ini + harga naik kuat = bandar distribusi/dorong
            elif vol_ratio_hari_ini >= 3.0 and pct_naik_hari_ini >= 3.0 and rsi < 75:
                markup.append(
                    f"💥 *{label}* — {harga}\n"
                    f"   Vol: {vol_ratio_hari_ini:.1f}x | +{pct_naik_hari_ini:.1f}% | "
                    f"RSI: {rsi:.1f} | Range: {avg_range:.1f}% (Markup/Breakout)"
                )
        except Exception as e:
            print(f"Error Bandar {symbol}: {e}")
            continue
    return akumulasi, markup

# ============================================================
# BROKER ANALYSIS (US Only — via Yahoo Finance analyst data)
# ============================================================
def scan_broker(ticker_list):
    results = []
    for symbol in ticker_list:
        try:
            ticker   = yf.Ticker(symbol)
            info     = ticker.info
            rating   = info.get('recommendationKey', '').upper()
            target   = info.get('targetMeanPrice')
            price    = info.get('currentPrice') or info.get('regularMarketPrice')
            analysts = info.get('numberOfAnalystOpinions', 0)

            if not rating or not target or not price: continue
            if analysts < 3: continue

            upside = ((target - price) / price * 100) if price > 0 else 0

            # Hanya tampil kalau ada potensi naik > 10% dan rating positif
            if upside >= 10 and rating in ['BUY', 'STRONG_BUY']:
                results.append(
                    f"📈 *{symbol}* — ${price:,.2f}\n"
                    f"   Rating: {rating} | Target: ${target:,.2f} | Upside: +{upside:.1f}% | Analis: {analysts}"
                )
        except Exception as e:
            print(f"Error Broker {symbol}: {e}")
            continue
    return results

# ============================================================
# PORTFOLIO — Daftar saham yang dimiliki user
# ============================================================
MY_PORTFOLIO = {
    # Ticker: (nama tampilan, market)
    "BULL.JK":  ("BULL",  "IHSG"),
    "BUMI.JK":  ("BUMI",  "IHSG"),
    "INET.JK":  ("INET",  "IHSG"),
    "MINA.JK":  ("MINA",  "IHSG"),
    "PTRO.JK":  ("PTRO",  "IHSG"),
    "MU":       ("MU",    "US"),
    "SOFI":     ("SOFI",  "US"),
    "SMH":      ("SMH",   "US"),
    "QQQ":      ("QQQ",   "US"),
    "AVGO":     ("AVGO",  "US"),
    "SMCI":     ("SMCI",  "US"),
    "SCHD":     ("SCHD",  "US"),
    "IREN":     ("IREN",  "US"),
}

# ============================================================
# ANALISIS SAHAM INDIVIDUAL — HOLD / JUAL / TAMBAH MUATAN
# ============================================================
def analyze_stock(symbol, market):
    try:
        df = build_df(symbol, period='6mo')
        if df is None or len(df) < 30:
            return None

        close      = float(df['close'].iloc[-1])
        close_prev = float(df['close'].iloc[-2])
        close_5d   = float(df['close'].iloc[-6])
        open_      = float(df['open'].iloc[-1])
        high       = float(df['high'].iloc[-1])
        low        = float(df['low'].iloc[-1])
        vol        = float(df['volume'].iloc[-1])
        vol_ma     = float(df['vol_ma20'].iloc[-1])
        rsi        = float(df['rsi'].iloc[-1])
        stoch_k    = float(df['stoch_k'].iloc[-1])
        stoch_k_p  = float(df['stoch_k'].iloc[-2])
        macd       = float(df['macd'].iloc[-1])
        msig       = float(df['macd_signal'].iloc[-1])
        macd_p     = float(df['macd'].iloc[-2])
        ma20       = float(df['ma20'].iloc[-1])
        ma50       = float(df['ma50'].iloc[-1])
        bb_up      = float(df['bb_upper'].iloc[-1])
        bb_low     = float(df['bb_lower'].iloc[-1])
        atr        = float(df['atr'].iloc[-1])
        obv_now    = float(df['obv'].iloc[-1])
        obv_5      = float(df['obv'].iloc[-6])

        harga      = fmt_price(close, market)
        pct_1d     = (close - close_prev) / close_prev * 100
        pct_5d     = (close - close_5d) / close_5d * 100
        vol_ratio  = vol / vol_ma if vol_ma > 0 else 0

        # --- STATUS TIAP INDIKATOR ---
        macd_bullish  = macd > msig
        macd_cross_up = macd > msig and macd_p <= msig  # golden cross baru
        macd_cross_dn = macd < msig and macd_p >= msig  # death cross baru
        obv_naik      = obv_now > obv_5
        trend_kuat    = close > ma20 > ma50
        trend_lemah   = close < ma20 < ma50
        near_bb_up    = close >= bb_up * 0.97
        near_bb_low   = close <= bb_low * 1.03
        stoch_naik    = stoch_k > stoch_k_p
        rsi_overbought = rsi > 70
        rsi_oversold   = rsi < 35

        # ── SCORING: poin positif vs negatif ──
        positif = sum([
            macd_bullish, obv_naik, trend_kuat,
            stoch_naik, rsi < 65, near_bb_low,
            pct_5d > 0
        ])
        negatif = sum([
            not macd_bullish, not obv_naik, trend_lemah,
            rsi_overbought, near_bb_up, pct_5d < -5
        ])

        # ── VERDICT ──
        alasan_beli, alasan_jual, alasan_waspada = [], [], []

        if macd_bullish:
            alasan_beli.append("MACD di atas sinyal (momentum bullish)")
        else:
            alasan_jual.append("MACD di bawah sinyal (momentum bearish)")

        if macd_cross_up:
            alasan_beli.append("⚡ MACD golden cross baru terjadi (sinyal beli segar)")
        if macd_cross_dn:
            alasan_jual.append("⚡ MACD death cross baru terjadi (sinyal jual segar)")

        if obv_naik:
            alasan_beli.append("OBV naik (big buyer masih akumulasi)")
        else:
            alasan_jual.append("OBV turun (distribusi, big player pelan-pelan keluar)")

        if trend_kuat:
            alasan_beli.append(f"tren kuat: harga > MA20 > MA50 (uptrend terkonfirmasi)")
        elif trend_lemah:
            alasan_jual.append(f"tren lemah: harga < MA20 < MA50 (downtrend)")
        else:
            alasan_waspada.append("tren sideways (MA20 & MA50 belum searah)")

        if rsi_overbought:
            alasan_jual.append(f"RSI {rsi:.0f} overbought (harga sudah terlalu tinggi, rawan koreksi)")
        elif rsi_oversold:
            alasan_beli.append(f"RSI {rsi:.0f} oversold (harga tertekan, potensi rebound)")
        else:
            alasan_beli.append(f"RSI {rsi:.0f} di zona sehat")

        if near_bb_up:
            alasan_waspada.append("harga mendekati Bollinger Band atas (resistensi kuat)")
        if near_bb_low:
            alasan_beli.append("harga mendekati Bollinger Band bawah (area support, dip bagus)")

        if stoch_naik:
            alasan_beli.append("Stochastic RSI naik (momentum jangka pendek membaik)")
        else:
            alasan_waspada.append("Stochastic RSI turun (momentum jangka pendek melemah)")

        if vol_ratio >= 2.0 and macd_bullish:
            alasan_beli.append(f"volume {vol_ratio:.1f}x rata-rata + MACD bullish (konfirmasi kuat)")
        elif vol_ratio >= 2.0 and not macd_bullish:
            alasan_waspada.append(f"volume {vol_ratio:.1f}x rata-rata tapi MACD bearish (hati-hati distribusi)")

        # ── KEPUTUSAN AKHIR ──
        if negatif >= 4 or (rsi_overbought and not obv_naik and not macd_bullish):
            verdict  = "🔴 JUAL SEMUA"
            emoji    = "🔴"
            ringkasan = "Mayoritas indikator merah. Tekanan jual kuat, disarankan keluar posisi."
            alasan_utama = alasan_jual[:3]

        elif (rsi_overbought and near_bb_up) or (not macd_bullish and not obv_naik and pct_5d < -3):
            verdict  = "🟠 JUAL SEBAGIAN"
            emoji    = "🟠"
            ringkasan = "Ada beberapa tanda pelemahan. Pertimbangkan ambil profit sebagian (50%)."
            alasan_utama = (alasan_jual + alasan_waspada)[:3]

        elif rsi_oversold and macd_bullish and obv_naik:
            verdict  = "🟢 TAMBAH MUATAN"
            emoji    = "🟢"
            ringkasan = "Saham ini sedang dip dengan indikator mulai berbalik naik. Bagus untuk averaging down."
            alasan_utama = alasan_beli[:3]

        elif positif >= 4 and macd_bullish and obv_naik:
            verdict  = "🟢 HOLD KUAT"
            emoji    = "🟢"
            ringkasan = "Posisi aman. Indikator mayoritas positif. Tahan dan pantau."
            alasan_utama = alasan_beli[:3]

        elif negatif >= 2 or len(alasan_waspada) >= 2:
            verdict  = "🟡 HOLD — WASPADA"
            emoji    = "🟡"
            ringkasan = "Ada sinyal campuran. Tahan posisi tapi siap pasang stop-loss."
            alasan_utama = (alasan_waspada + alasan_jual)[:3]

        else:
            verdict  = "🟡 HOLD"
            emoji    = "🟡"
            ringkasan = "Kondisi netral. Tidak ada sinyal kuat untuk aksi apapun saat ini."
            alasan_utama = (alasan_beli + alasan_waspada)[:3]

        # ── FORMAT OUTPUT ──
        tren_icon  = "📈" if trend_kuat else ("📉" if trend_lemah else "➡️")
        alasan_txt = "\n   • ".join(alasan_utama) if alasan_utama else "tidak ada sinyal dominan"

        hasil = (
            f"{emoji} *{symbol.replace('.JK','')}* — {harga} | *{verdict}*\n"
            f"   {tren_icon} RSI: {rsi:.1f} | MACD: {'▲' if macd_bullish else '▼'} | "
            f"Vol: {vol_ratio:.1f}x | OBV: {'↑' if obv_naik else '↓'} | "
            f"1H: {pct_1d:+.1f}% | 5H: {pct_5d:+.1f}%\n"
            f"   📝 _{ringkasan}_\n"
            f"   💬 Alasan:\n   • {alasan_txt}"
        )
        return hasil

    except Exception as e:
        return f"❌ Gagal analisis {symbol}: {e}"

# ============================================================
# KIRIM HASIL
# ============================================================
def send_result(message, title, total, sb, dp, ob):
    pesan = f"📊 *HASIL SCAN {title}* ({total} saham)\n🕒 {get_waktu()}\n\n"
    if sb: pesan += "🔥 *STRONG BUY:*\n" + "\n\n".join(sb) + "\n\n"
    if dp: pesan += "🟡 *DIP / SALE:*\n" + "\n".join(dp) + "\n\n"
    if ob: pesan += "⚠️ *OVERBOUGHT:*\n" + "\n".join(ob) + "\n\n"
    if not (sb or dp or ob):
        pesan += "Pasar lagi sideways, nggak ada sinyal kuat hari ini."
    bot.reply_to(message, pesan, parse_mode='Markdown')

def send_strategy(message, title, emoji, results, keterangan):
    pesan = f"{emoji} *{title}*\n🕒 {get_waktu()}\n_{keterangan}_\n\n"
    pesan += "\n\n".join(results) if results else "Tidak ada saham yang memenuhi kriteria saat ini."
    bot.reply_to(message, pesan, parse_mode='Markdown')

# ============================================================
# COMMAND HANDLERS
# ============================================================
@bot.message_handler(commands=['scan_us'])
def handle_us(message):
    total = len(tickers_us)
    bot.reply_to(message, f"⏳ Memindai {total} saham US...")
    sb, dp, ob = perform_scan(tickers_us, "US")
    send_result(message, "PASAR US", total, sb, dp, ob)

@bot.message_handler(commands=['scan_ihsg'])
def handle_ihsg(message):
    total = len(tickers_ihsg)
    bot.reply_to(message, f"⏳ Memindai {total} saham IHSG...")
    sb, dp, ob = perform_scan(tickers_ihsg, "IHSG")
    send_result(message, "PASAR IHSG", total, sb, dp, ob)

@bot.message_handler(commands=['scan'])
def handle_all(message):
    bot.reply_to(message, "⏳ Memindai semua pasar (US + IHSG)...")
    sb, dp, ob = perform_scan(tickers_us, "US")
    send_result(message, "PASAR US", len(tickers_us), sb, dp, ob)
    sb, dp, ob = perform_scan(tickers_ihsg, "IHSG")
    send_result(message, "PASAR IHSG", len(tickers_ihsg), sb, dp, ob)

@bot.message_handler(commands=['bsjp'])
def handle_bsjp(message):
    bot.reply_to(message, "🌙 Mencari kandidat BSJP di IHSG...")
    results = scan_bsjp(tickers_ihsg, "IHSG")
    send_strategy(message, "BSJP — Beli Sore Jual Pagi", "🌙", results,
                  "Vol spike + tutup dekat High + MACD bullish + OBV naik")

@bot.message_handler(commands=['ara'])
def handle_ara(message):
    bot.reply_to(message, "🚀 Mendeteksi kandidat ARA di IHSG...")
    results = scan_ara(tickers_ihsg, "IHSG")
    send_strategy(message, "ARA DETECTOR", "🚀", results,
                  "Volume 3x avg + harga naik 5%+ + OBV naik")

@bot.message_handler(commands=['bpjs'])
def handle_bpjs(message):
    bot.reply_to(message, "⚡ Mencari kandidat Scalping BPJS di IHSG...")
    results = scan_bpjs(tickers_ihsg, "IHSG")
    send_strategy(message, "BPJS — Scalping Beli Pagi Jual Siang", "⚡", results,
                  "Gap Up + volume tinggi + ATR besar + BB Squeeze")

@bot.message_handler(commands=['bandar'])
def handle_bandar(message):
    bot.reply_to(message, "🕵️ Mendeteksi pergerakan Bandar di IHSG...")
    akumulasi, markup = scan_bandar(tickers_ihsg, "IHSG")
    pesan = f"🕵️ *BANDARMOLOGY DETECTOR*\n🕒 {get_waktu()}\n\n"
    if akumulasi:
        pesan += "🏦 *FASE AKUMULASI* _(Bandar kumpulin diam-diam)_:\n" + "\n\n".join(akumulasi) + "\n\n"
    if markup:
        pesan += "💥 *FASE MARKUP/BREAKOUT* _(Bandar dorong harga)_:\n" + "\n\n".join(markup) + "\n\n"
    if not akumulasi and not markup:
        pesan += "Tidak terdeteksi aktivitas Bandar yang signifikan hari ini."
    bot.reply_to(message, pesan, parse_mode='Markdown')

@bot.message_handler(commands=['broker'])
def handle_broker(message):
    bot.reply_to(message, "📊 Mengambil rekomendasi 50 saham US terpopuler dari analis broker...")
    results = scan_broker(tickers_broker)
    pesan = f"📊 *REKOMENDASI BROKER ANALIS (US Top 50)*\n🕒 {get_waktu()}\n_Upside > 10% + Rating BUY_\n\n"
    pesan += "\n\n".join(results) if results else "Tidak ada rekomendasi kuat saat ini."
    bot.reply_to(message, pesan, parse_mode='Markdown')

@bot.message_handler(commands=['portfolio'])
def handle_portfolio(message):
    bot.reply_to(message, f"🗂️ Menganalisis {len(MY_PORTFOLIO)} saham portfolio kamu...")
    pesan = f"🗂️ *ANALISIS PORTFOLIO*\n🕒 {get_waktu()}\n\n"
    for symbol, (label, market) in MY_PORTFOLIO.items():
        hasil = analyze_stock(symbol, market)
        if hasil:
            pesan += hasil + "\n\n"
        else:
            pesan += f"❌ *{label}* — Data tidak tersedia\n\n"
        # Kirim per 3 saham supaya tidak timeout Telegram
        if pesan.count('\n\n') % 4 == 0 and pesan.count('\n\n') > 0:
            bot.reply_to(message, pesan, parse_mode='Markdown')
            pesan = ""
    if pesan.strip():
        bot.reply_to(message, pesan, parse_mode='Markdown')

@bot.message_handler(commands=['cek'])
def handle_cek(message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Contoh penggunaan: `/cek BUMI` atau `/cek MU`", parse_mode='Markdown')
        return
    raw    = parts[1].upper()
    # Deteksi otomatis IHSG vs US
    if raw in [t.replace('.JK','') for t in tickers_ihsg]:
        symbol = raw + ".JK"
        market = "IHSG"
    else:
        symbol = raw
        market = "US"
    bot.reply_to(message, f"🔍 Menganalisis *{raw}*...", parse_mode='Markdown')
    hasil = analyze_stock(symbol, market)
    pesan = f"🔍 *ANALISIS SAHAM — {raw}*\n🕒 {get_waktu()}\n\n"
    pesan += hasil if hasil else f"❌ Data untuk *{raw}* tidak ditemukan. Cek kembali kode ticker-nya."
    bot.reply_to(message, pesan, parse_mode='Markdown')

# --- Shortcut commands untuk tiap saham portfolio ---
def _make_handler(sym, mkt):
    def handler(message):
        label = sym.replace('.JK', '')
        bot.reply_to(message, f"🔍 Menganalisis *{label}*...", parse_mode='Markdown')
        hasil = analyze_stock(sym, mkt)
        pesan = f"🔍 *ANALISIS — {label}*\n🕒 {get_waktu()}\n\n"
        pesan += hasil if hasil else f"❌ Data tidak ditemukan untuk {label}."
        bot.reply_to(message, pesan, parse_mode='Markdown')
    return handler

for _sym, (_lbl, _mkt) in MY_PORTFOLIO.items():
    _cmd = _lbl.lower()
    bot.message_handler(commands=[_cmd])(_make_handler(_sym, _mkt))

@bot.message_handler(commands=['help'])
def handle_help(message):
    pesan = (
        "📋 *DAFTAR PERINTAH BOT*\n\n"
        "🔍 *SCAN PASAR:*\n"
        "/scan\\_us — Scan saham US\n"
        "/scan\\_ihsg — Scan saham IHSG\n"
        "/scan — Scan US + IHSG sekaligus\n\n"
        "🎯 *STRATEGI IHSG:*\n"
        "/bsjp — Beli Sore Jual Pagi\n"
        "/ara — ARA Detector\n"
        "/bpjs — Scalping Beli Pagi Jual Siang\n"
        "/bandar — Bandarmology Detector\n\n"
        "📊 *ANALISIS TAMBAHAN:*\n"
        "/broker — Rekomendasi analis broker (US)\n\n"
        "💼 *PORTFOLIO PRIBADI:*\n"
        "/portfolio — Analisis semua saham portfolio\n"
        "/cek [TICKER] — Analisis saham apapun\n"
        "   contoh: /cek BUMI atau /cek MU\n\n"
        "📌 *SHORTCUT PORTFOLIO:*\n"
        "/bull /bumi /inet /mina /ptro\n"
        "/mu /sofi /smh /qqq /avgo /smci /schd /iren\n\n"
        "💡 *INDIKATOR:*\n"
        "• RSI (14) + Stochastic RSI\n"
        "• MACD + Signal\n"
        "• MA20 & MA50\n"
        "• Bollinger Bands\n"
        "• ATR (volatilitas)\n"
        "• OBV (konfirmasi volume)\n"
        "• Bandarmology (akumulasi & markup)\n\n"
        "🔴 JUAL SEMUA  🟠 JUAL SEBAGIAN\n"
        "🟢 HOLD KUAT / TAMBAH MUATAN  🟡 HOLD"
    )
    bot.reply_to(message, pesan, parse_mode='Markdown')

# --- JALANKAN BOT ---
print("Bot siap! Ketik /help di Telegram.")
bot.polling(non_stop=True)
