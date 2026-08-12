# GeoI18n SQL Toolkit

[English](README.en.md) | [中文](README.md)

A comprehensive toolkit for generating SQL data for country/region internationalization (i18n). Built on the ISO 3166-1 standard, it provides country/region information, currency data, language data, and multi-language country names for 250+ countries worldwide, with automatic translation support for 80+ languages via the Google Translate API.

## Features

- 🌍 **Global Coverage**: Data for 250+ countries and regions worldwide
- 🌐 **Multi-Language Support**: Built-in translations for 80+ languages
- 🤖 **Auto Translation**: Automatically generates missing language data using the free Google Translate API
- 📊 **Multi-Dimensional Data**: Country basics, currency info, language data, and i18n names
- 💾 **SQL Generation**: One-click generation of standard INSERT SQL statements
- 🔄 **Multi-Format Output**: Supports JSON, CSV, and SQL data formats

## Project Structure

```
GeoI18n-SQL-Toolkit/
├── gen_i18n_sql.py              # Core script: i18n SQL generator (with Google Translate support)
├── README.md                    # Chinese README
├── README.en.md                 # English README
├── gen_i18n_sql_usage.md        # gen_i18n_sql usage guide
├── region_data.json             # Country/region basic data (JSON)
├── region_data.csv              # Country/region basic data (CSV)
├── region_data.sql              # Country/region basic data (SQL)
└── data/
    ├── currency/                # Currency data
    │   ├── region_currency_data.json
    │   ├── region_currency_data.csv
    │   └── region_currency_data.sql
    ├── language/                # Language data
    │   ├── region_language_data.json
    │   ├── region_language_data.csv
    │   └── region_language_data.sql
    └── i18n/                    # Multi-language country name data
        ├── region_i18n_data.json
        ├── region_i18n_data.csv
        └── region_i18n_data.sql
```

## Data Descriptions

### region_data — Country/Region Basic Information

| Field | Description | Example |
|-------|-------------|---------|
| iso2 | ISO 3166-1 alpha-2 country code | CN |
| iso3 | ISO 3166-1 alpha-3 country code | CHN |
| continent | Continent | Asia |
| native_country_name | Country name in native language | 中国 |
| country_zh_name | Country name in Chinese | 中国 |
| country_en_name | Country name in English | China |
| latitude | Latitude | 35.86166 |
| longitude | Longitude | 104.195397 |
| phone_code | International dialing code | +86 |
| phone_format | Phone number format | ### #### #### |
| capital | Capital city | Beijing |
| tld | Top-level domain | .cn |
| flag_emoji | Flag emoji | 🇨🇳 |
| currency_code | Currency code | CNY |
| currency_zh_name | Currency name in Chinese | 人民币 |
| currency_en_name | Currency name in English | Chinese Yuan |
| currency_symbol | Currency symbol | ¥ |
| language_code | Official language code | zh |
| timezones | Timezone info (JSON array) | ... |

### region_i18n_data — Internationalized Country Names

| Field | Description | Example |
|-------|-------------|---------|
| iso2 | ISO country code | CN |
| language | Language code | zh |
| value | Country name in the specified language | 中国 |

### region_currency_data — Currency Information

| Field | Description | Example |
|-------|-------------|---------|
| iso2 | ISO country code | CN |
| currency_code | Currency code | CNY |
| native_currency_name | Currency name in native language | Chinese Yuan |
| currency_zh_name | Currency name in Chinese | 人民币 |
| currency_en_name | Currency name in English | Chinese Yuan |
| currency_symbol | Currency symbol | ¥ |
| decimal_place | Decimal places | 2 |
| thousand_separator | Thousand separator | , |
| decimal_separator | Decimal separator | . |

### region_language_data — Language Information

| Field | Description | Example |
|-------|-------------|---------|
| iso2 | ISO country code | CN |
| language_code | Language code | zh |
| native_language_name | Language name in native script | 中文 |
| language_zh_name | Language name in Chinese | 中文 |
| language_en_name | Language name in English | Chinese |

## Quick Start

### Requirements

- Python 3.7+
- No external dependencies (uses only the standard library)

### Installation

```bash
git clone https://github.com/your-username/GeoI18n-SQL-Toolkit.git
cd GeoI18n-SQL-Toolkit
```

### Usage

#### 1. Generate i18n SQL for a Specific Language

```bash
# Use local existing data (e.g., Chinese)
python gen_i18n_sql.py zh

# Auto-translate to generate Uzbek SQL
python gen_i18n_sql.py uz

# Auto-translate to generate Arabic SQL
python gen_i18n_sql.py ar
```

#### 2. Force Re-translation to Override Existing Data

```bash
# Force override existing Japanese data with Google Translate
python gen_i18n_sql.py ja --force
```

#### 3. Output to a Specific File

```bash
# Translate and save to file
python gen_i18n_sql.py ar -o ar.sql
```

#### 4. List Supported Languages

```bash
python gen_i18n_sql.py --list
```

### Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `<language_code>` | ISO 639-1 language code (required) |
| `--force` | Force override existing data with Google Translate |
| `-o <file>` | Output SQL to a specified file |
| `--list` | List all supported language codes |

## Workflow

1. **Read Local Data First**: The script first searches `data/i18n/region_i18n_data.json` for existing data in the target language
2. **Auto Translation**: If the target language is not available locally, it auto-translates from the English source data using the Google Translate API
3. **Generate SQL**: Formats the data into standard `INSERT INTO` SQL statements

## Supported Languages (Partial List)

English, Chinese, Japanese, Korean, Arabic, Uzbek, Russian, French, German, Spanish, Portuguese, Italian, Dutch, Swedish, Danish, Finnish, Norwegian, Polish, Czech, Hungarian, Romanian, Bulgarian, Ukrainian, Turkish, Greek, Thai, Vietnamese, Hindi, Persian, Hebrew, Burmese, Khmer, Lao, Mongolian, and 80+ more languages.

## Database Table Structure Reference

```sql
-- Internationalized country names table
CREATE TABLE region_i18n_data (
    iso2 VARCHAR(5) NOT NULL,
    language VARCHAR(10) NOT NULL,
    value VARCHAR(255) NOT NULL,
    PRIMARY KEY (iso2, language)
);

-- Country basic information table
CREATE TABLE region_data (
    iso2 VARCHAR(5) PRIMARY KEY,
    iso3 VARCHAR(5),
    continent VARCHAR(30),
    native_country_name VARCHAR(255),
    country_zh_name VARCHAR(255),
    country_en_name VARCHAR(255),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    phone_code VARCHAR(20),
    phone_format VARCHAR(50),
    capital VARCHAR(100),
    tld VARCHAR(20),
    flag_emoji VARCHAR(10),
    currency_code VARCHAR(10),
    language_code VARCHAR(10),
    timezones TEXT
);
```

## Notes

- The Google Translate API may have rate limits. The script includes a throttle of 0.5 seconds every 5 requests
- Auto-translated results should be reviewed manually, especially for technical terms and less common languages
- Some languages may fail if not supported by Google Translate. Refer to the `--list` output for supported languages
- When offline, only languages with local data available can be used

## License

MIT License