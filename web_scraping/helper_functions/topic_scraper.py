import pandas as pd

def econ_topic_scaper(source_path, output_folder_path, output_file_name):
    # ==========================================
    # 1. Setup & Load Data
    # ==========================================
    print(f"--- Loading data from: {source_path} ---")

    # Load directly into a DataFrame (use `df` so we don't overwrite the filename variable)
    df = pd.read_json(source_path, lines=True)

    # Define topics and keywords
    topic_map = {
        "topic_inflation": ["inflation", "cpi", "price hike", "cost of living", "expensive", "prices"],
        "topic_taxes":     ["tax", "taxes", "irs", "corporate tax", "tax cut", "deduction"],
        "topic_stocks":    ["stock market", "wall street", "s&p", "dow jones", "nasdaq", "bull market", "bear market"],
        "topic_jobs":      ["jobs", "unemployment", "hiring", "wages", "labor", "layoffs", "workforce"],
        "topic_housing":   ["housing", "rent", "mortgage", "real estate", "home prices"],
        "topic_energy":    ["energy", "oil", "gas", "fuel", "green energy", "climate"],
        "topic_crypto":    ["crypto", "bitcoin", "ethereum", "blockchain"]
    }

    # ==========================================
    # 2. binary Topic Flagging (1 or 0)
    # ==========================================
    print(f"Processing {len(df)} rows...")

    def has_topic(text, keywords):
        if not isinstance(text, str):
            return 0
        text_lower = text.lower()
        # Return 1 if ANY keyword is found, else 0
        if any(k in text_lower for k in keywords):
            return 1
        return 0

    # Apply checking for each topic
    topic_cols = []
    for topic, keywords in topic_map.items():
        df[topic] = df['body'].apply(
            lambda x: has_topic(x, keywords)
        )
        topic_cols.append(topic)

    # ==========================================
    # 3. Create & Print Summary Table
    # ==========================================
    # Calculate sums for just the topic columns
    totals = df[topic_cols].sum().sort_values(ascending=False)

    print("\n--- Topic Totals (Articles containing topic) ---")
    print(f"{'TOPIC':<20} | {'TOTAL':<5}")
    print("-" * 30)
    for topic, count in totals.items():
        print(f"{topic:<20} | {count:<5}")
    print("-" * 30)

    # ==========================================
    # 4. Save Data
    # ==========================================
    print(f"\nSaving to {output_folder_path+output_file_name}...")

    df.to_json(output_folder_path+output_file_name, orient="records", lines=True, date_format='iso')

    print("[✓] Done. File updated.")