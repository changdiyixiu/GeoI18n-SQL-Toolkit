# GeoI18n SQL Toolkit 地理国际化 SQL 工具包

[中文](README.md) | [English](README.en.md)

国家/地区国际化数据 SQL 生成工具包。基于 ISO 3166-1标准，提供全球国家/地区的基础信息、货币、语言及多语言名称数据，支持通过谷歌翻译 API 自动生成 80+ 种语言的国际化 SQL 数据。

## 功能特性

- 🌍 **全球覆盖**：包含全球 250+ 个国家/地区的数据
- 🌐 **多语言支持**：内置 80+ 种语言的国家名称翻译
- 🤖 **自动翻译**：通过谷歌翻译免费 API 自动生成缺失语言数据
- 📊 **多维度数据**：国家基础信息、货币、语言、国际化名称
- 💾 **SQL 生成**：一键生成标准 INSERT SQL 语句
- 🔄 **多格式输出**：支持 JSON、CSV、SQL 三种数据格式

## 项目结构

```
GeoI18n-SQL-Toolkit/
├── gen_i18n_sql.py              # 核心脚本：国际化 SQL 生成器（支持谷歌翻译）
├── README.md                    # 中文说明
├── README.en.md                 # English README
├── gen_i18n_sql_usage.md        # gen_i18n_sql 使用方法
├── region_data.json             # 国家/地区基础数据（JSON）
├── region_data.csv              # 国家/地区基础数据（CSV）
├── region_data.sql              # 国家/地区基础数据（SQL）
└── data/
    ├── currency/                # 货币数据
    │   ├── region_currency_data.json
    │   ├── region_currency_data.csv
    │   └── region_currency_data.sql
    ├── language/                # 语言数据
    │   ├── region_language_data.json
    │   ├── region_language_data.csv
    │   └── region_language_data.sql
    └── i18n/                    # 多语言国家名称数据
        ├── region_i18n_data.json
        ├── region_i18n_data.csv
        └── region_i18n_data.sql
```

## 数据说明

### region_data — 国家/地区基础信息

| 字段 | 说明 | 示例 |
|------|------|------|
| iso2 | ISO 3166-1 alpha-2 国家代码 | CN |
| iso3 | ISO 3166-1 alpha-3 国家代码 | CHN |
| continent | 所属大洲 | Asia |
| native_country_name | 本国语言国名 | 中国 |
| country_zh_name | 中文国名 | 中国 |
| country_en_name | 英文国名 | China |
| latitude | 纬度 | 35.86166 |
| longitude | 经度 | 104.195397 |
| phone_code | 国际区号 | +86 |
| phone_format | 电话格式 | ### #### #### |
| capital | 首都 | Beijing |
| tld | 顶级域名 | .cn |
| flag_emoji | 国旗 Emoji | 🇨🇳 |
| currency_code | 货币代码 | CNY |
| currency_zh_name | 货币中文名 | 人民币 |
| currency_en_name | 货币英文名 | Chinese Yuan |
| currency_symbol | 货币符号 | ¥ |
| language_code | 官方语言代码 | zh |
| timezones | 时区信息（JSON数组） | ... |

### region_i18n_data — 国际化国家名称

| 字段 | 说明 | 示例 |
|------|------|------|
| iso2 | ISO 国家代码 | CN |
| language | 语言代码 | zh |
| value | 对应语言的国家名称 | 中国 |

### region_currency_data — 货币信息

| 字段 | 说明 | 示例 |
|------|------|------|
| iso2 | ISO 国家代码 | CN |
| currency_code | 货币代码 | CNY |
| native_currency_name | 货币本地名称 | Chinese Yuan |
| currency_zh_name | 货币中文名 | 人民币 |
| currency_en_name | 货币英文名 | Chinese Yuan |
| currency_symbol | 货币符号 | ¥ |
| decimal_place | 小数位数 | 2 |
| thousand_separator | 千位分隔符 | , |
| decimal_separator | 小数点符号 | . |

### region_language_data — 语言信息

| 字段 | 说明 | 示例 |
|------|------|------|
| iso2 | ISO 国家代码 | CN |
| language_code | 语言代码 | zh |
| native_language_name | 语言本地名称 | 中文 |
| language_zh_name | 语言中文名 | 中文 |
| language_en_name | 语言英文名 | Chinese |

## 快速开始

### 环境要求

- Python 3.7+
- 无需额外依赖（仅使用标准库）

### 安装

```bash
git clone https://github.com/your-username/GeoI18n-SQL-Toolkit.git
cd GeoI18n-SQL-Toolkit
```

### 使用方法

#### 1. 生成指定语言的国际化 SQL

```bash
# 使用本地已有数据（如中文）
python gen_i18n_sql.py zh

# 自动翻译生成乌兹别克语 SQL
python gen_i18n_sql.py uz

# 自动翻译生成阿拉伯语 SQL
python gen_i18n_sql.py ar
```

#### 2. 强制重新翻译覆盖现有数据

```bash
# 强制用谷歌翻译覆盖现有日语数据
python gen_i18n_sql.py ja --force
```

#### 3. 输出到指定文件

```bash
# 翻译并保存到文件
python gen_i18n_sql.py ar -o ar.sql
```

#### 4. 查看支持的语言列表

```bash
python gen_i18n_sql.py --list
```

### 命令行参数

| 参数 | 说明 |
|------|------|
| `<语言代码>` | ISO 639-1 语言代码（必填） |
| `--force` | 强制使用谷歌翻译覆盖现有数据 |
| `-o <文件>` | 将 SQL 输出到指定文件 |
| `--list` | 列出所有支持的语言代码 |

## 工作流程

1. **优先读取本地数据**：脚本首先从 `data/i18n/region_i18n_data.json` 中查找目标语言的已有数据
2. **自动翻译补全**：如果本地不存在目标语言数据，则从英语源数据出发，通过谷歌翻译 API 自动翻译
3. **生成 SQL**：将数据格式化为标准的 `INSERT INTO` SQL 语句

## 支持的语言（部分）

英语、中文、日语、韩语、阿拉伯语、乌兹别克语、俄语、法语、德语、西班牙语、葡萄牙语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、乌克兰语、土耳其语、希腊语、泰语、越南语、印度语、波斯语、希伯来语、缅甸语、高棉语、老挝语、蒙古语等 80+ 种语言。

## 数据库表结构参考

```sql
-- 国际化国家名称表
CREATE TABLE region_i18n_data (
    iso2 VARCHAR(5) NOT NULL,
    language VARCHAR(10) NOT NULL,
    value VARCHAR(255) NOT NULL,
    PRIMARY KEY (iso2, language)
);

-- 国家基础信息表
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

## 注意事项

- 谷歌翻译 API 可能有频率限制，脚本已内置每 5 条暂停 0.5 秒的节流策略
- 自动翻译结果建议人工审核，特别是对于专业术语和小语种
- 部分语言可能因谷歌翻译不支持而失败，请参考 `--list` 输出的支持列表
- 互联网连接不可用时，只能使用本地已有数据的语言

## 许可证

MIT License