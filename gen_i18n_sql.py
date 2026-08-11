# -*- coding: utf-8 -*-
"""
国际化 SQL 生成工具（支持谷歌翻译自动生成）
用法：
  python gen_i18n_sql.py <语言代码>            # 优先从现有 JSON 读取，缺失时自动谷歌翻译
  python gen_i18n_sql.py <语言代码> --force    # 强制用谷歌翻译覆盖现有数据
  python gen_i18n_sql.py --list               # 列出支持的语言代码
示例：
  python gen_i18n_sql.py zh        # 使用本地中文数据
  python gen_i18n_sql.py uz        # 自动翻译生成乌兹别克语 SQL
  python gen_i18n_sql.py ar        # 自动翻译生成阿拉伯语 SQL
"""

import json
import sys
import os
import time
import urllib.request
import urllib.parse


def escape_sql_string(value: str) -> str:
    if value is None:
        return 'NULL'
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


# ISO 639-1 语言代码 → 谷歌翻译语言代码映射
GOOGLE_LANG_MAP = {
    'ko': 'ko', 'zh': 'zh-CN', 'pt': 'pt', 'ms': 'ms', 'tl': 'tl',
    'hi': 'hi', 'ur': 'ur', 'fa': 'fa', 'ar': 'ar', 'he': 'he',
    'th': 'th', 'vi': 'vi', 'id': 'id', 'ru': 'ru', 'ja': 'ja',
    'de': 'de', 'fr': 'fr', 'es': 'es', 'it': 'it', 'nl': 'nl',
    'sv': 'sv', 'da': 'da', 'fi': 'fi', 'nb': 'no', 'pl': 'pl',
    'cs': 'cs', 'sk': 'sk', 'hu': 'hu', 'ro': 'ro', 'bg': 'bg',
    'uk': 'uk', 'tr': 'tr', 'el': 'el', 'sr': 'sr', 'hr': 'hr',
    'sl': 'sl', 'lt': 'lt', 'lv': 'lv', 'et': 'et', 'is': 'is',
    'ga': 'ga', 'cy': 'cy', 'mt': 'mt', 'sq': 'sq', 'mk': 'mk',
    'hy': 'hy', 'az': 'az', 'eu': 'eu', 'ca': 'ca', 'gl': 'gl',
    'bs': 'bs', 'sw': 'sw', 'am': 'am', 'ha': 'ha', 'yo': 'yo',
    'ig': 'ig', 'zu': 'zu', 'xh': 'xh', 'af': 'af', 'st': 'st',
    'tn': 'tn', 'ts': 'ts', 'ss': 'ss', 'nd': 'nd',
    've': 've', 'si': 'si', 'my': 'my', 'km': 'km', 'lo': 'lo',
    'ne': 'ne', 'gu': 'gu', 'pa': 'pa', 'bn': 'bn', 'ta': 'ta',
    'te': 'te', 'ml': 'ml', 'kn': 'kn', 'mr': 'mr', 'uz': 'uz',
    'ky': 'ky', 'kk': 'kk', 'tg': 'tg', 'mn': 'mn', 'ka': 'ka',
    'la': 'la', 'ps': 'ps', 'ku': 'ku', 'so': 'so', 'aa': 'aa',
    'om': 'om', 'ti': 'ti', 'mg': 'mg', 'gn': 'gn', 'qu': 'qu',
    'ay': 'ay', 'ty': 'ty', 'fj': 'fj', 'sm': 'sm', 'to': 'to',
    'nr': 'nr', 'tv': 'tv', 'fm': 'fm', 'mh': 'mh', 'pw': 'pw',
    'ki': 'ki', 'en': 'en',
}

# 语言代码 → 中文名
LANG_NAMES = {
    'en': '英语', 'zh': '中文', 'ko': '韩语', 'ja': '日语',
    'de': '德语', 'fr': '法语', 'es': '西班牙语', 'pt': '葡萄牙语',
    'it': '意大利语', 'nl': '荷兰语', 'sv': '瑞典语', 'da': '丹麦语',
    'fi': '芬兰语', 'nb': '挪威语', 'pl': '波兰语', 'cs': '捷克语',
    'sk': '斯洛伐克语', 'hu': '匈牙利语', 'ro': '罗马尼亚语', 'bg': '保加利亚语',
    'uk': '乌克兰语', 'ru': '俄语', 'tr': '土耳其语', 'el': '希腊语',
    'sr': '塞尔维亚语', 'hr': '克罗地亚语', 'sl': '斯洛文尼亚语',
    'lt': '立陶宛语', 'lv': '拉脱维亚语', 'et': '爱沙尼亚语',
    'is': '冰岛语', 'ga': '爱尔兰语', 'cy': '威尔士语', 'mt': '马耳他语',
    'sq': '阿尔巴尼亚语', 'mk': '马其顿语', 'hy': '亚美尼亚语',
    'az': '阿塞拜疆语', 'eu': '巴斯克语', 'ca': '加泰罗尼亚语',
    'gl': '加利西亚语', 'bs': '波黑语', 'sw': '斯瓦希里语',
    'am': '阿姆哈拉语', 'ha': '豪萨语', 'yo': '约鲁巴语',
    'zu': '祖鲁语', 'xh': '科萨语', 'af': '南非荷兰语',
    'st': '塞索托语', 'si': '僧伽罗语', 'my': '缅甸语',
    'km': '高棉语', 'lo': '老挝语', 'ne': '尼泊尔语',
    'gu': '古吉拉特语', 'pa': '旁遮普语', 'bn': '孟加拉语',
    'ta': '泰米尔语', 'te': '泰卢固语', 'ml': '马拉雅拉姆语',
    'kn': '卡纳达语', 'mr': '马拉地语', 'uz': '乌兹别克语',
    'ky': '吉尔吉斯语', 'kk': '哈萨克语', 'tg': '塔吉克语',
    'mn': '蒙古语', 'vi': '越南语', 'ka': '格鲁吉亚语',
    'la': '拉丁语', 'ps': '普什图语', 'ku': '库尔德语',
    'so': '索马里语', 'mg': '马达加斯加语', 'gn': '瓜拉尼语',
    'qu': '奇楚瓦语', 'ay': '艾马拉语', 'fj': '斐济语',
    'sm': '萨摩亚语', 'to': '汤加语', 'ar': '阿拉伯语',
    'he': '希伯来语', 'th': '泰语', 'id': '印尼语',
    'ms': '马来语', 'tl': '他加禄语', 'hi': '印地语',
    'ur': '乌尔都语', 'fa': '波斯语',
}


def google_translate(text: str, dest_lang: str, src_lang: str = 'en') -> str:
    """
    使用谷歌翻译免费 API 翻译文本
    API: https://translate.googleapis.com/translate_a/single
    """
    mapped_dest = GOOGLE_LANG_MAP.get(dest_lang, dest_lang)
    mapped_src = GOOGLE_LANG_MAP.get(src_lang, src_lang)

    params = urllib.parse.urlencode({
        'client': 'gtx',
        'sl': mapped_src,
        'tl': mapped_dest,
        'dt': 't',
        'q': text
    })
    url = f'https://translate.googleapis.com/translate_a/single?{params}'

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            # 解析翻译结果
            if result and result[0]:
                translated = ''.join([item[0] for item in result[0] if item[0]])
                return translated
            return text
    except Exception as e:
        print(f'  翻译失败 [{text}]: {e}')
        return text


def check_translate_available() -> bool:
    """检测谷歌翻译 API 是否可用"""
    try:
        result = google_translate('test', 'zh', 'en')
        return result != 'test' and len(result) > 0
    except Exception:
        return False


def generate_i18n_sql(
    language: str,
    input_file: str = 'data/i18n/region_i18n_data.json',
    source_lang: str = 'en',
    force_translate: bool = False
) -> str:
    """
    生成指定语言的 i18n SQL
    优先使用本地 JSON 数据，缺失时使用谷歌翻译自动生成
    """
    if not os.path.exists(input_file):
        print(f'错误：找不到输入文件 {input_file}')
        print('请确保 data/i18n/ 目录下存在 region_i18n_data.json')
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 过滤已有该语言的数据
    existing = [r for r in data if r.get('language') == language]

    if existing and not force_translate:
        print(f'从本地数据读取到 {len(existing)} 条 "{language}" 语言记录')
        return _build_sql(existing, language)

    # 需要翻译：从源语言提取国家列表
    source_data = [r for r in data if r.get('language') == source_lang]
    if not source_data:
        print(f'错误：本地没有 "{source_lang}" 源语言数据，无法翻译')
        print('请确保 data/i18n/region_i18n_data.json 中包含英语(en)数据')
        sys.exit(1)

    # 检测谷歌翻译是否可用
    print('检测谷歌翻译连接...')
    if not check_translate_available():
        print(f'谷歌翻译不可用，且本地无 "{language}" 数据')
        print(f'可用语言：{sorted(set(r["language"] for r in data))}')
        sys.exit(0)

    print(f'使用谷歌翻译将 {len(source_data)} 条记录从 "{source_lang}" 翻译为 "{language}"...')
    print('-' * 50)

    # 翻译每条记录
    translated = []
    failed = 0
    for idx, record in enumerate(source_data):
        iso2 = record['iso2']
        value = record['value']

        print(f'  [{idx+1}/{len(source_data)}] {iso2}: {value} → ', end='', flush=True)
        translated_value = google_translate(value, dest_lang=language, src_lang=source_lang)
        if translated_value == value:
            failed += 1
        print(translated_value)

        translated.append({
            'iso2': iso2,
            'language': language,
            'value': translated_value,
        })

        # 每 5 条暂停一下，避免被限流
        if (idx + 1) % 5 == 0:
            time.sleep(0.5)

    print('-' * 50)
    print(f'翻译完成：{len(translated)} 条，失败：{failed} 条')

    return _build_sql(translated, language)


def _build_sql(records: list, language: str) -> str:
    """构建 INSERT SQL 语句"""
    lines = [
        f'-- region_i18n_data 数据（语言: {language}）',
        f'-- 共 {len(records)} 条记录',
        '',
        'INSERT INTO region_i18n_data (',
        '    "iso2",',
        '    "language",',
        '    "value"',
        ') VALUES',
    ]

    for i, record in enumerate(records):
        iso2 = record.get('iso2', '')
        lang = record.get('language', '')
        value = record.get('value', '')

        values = ', '.join([
            escape_sql_string(iso2),
            escape_sql_string(lang),
            escape_sql_string(value),
        ])

        suffix = ';' if i == len(records) - 1 else ','
        lines.append(f'({values}){suffix}')

    return '\n'.join(lines)


def list_supported_languages():
    """列出支持的语言代码"""
    print('支持的 ISO 639-1 语言代码（谷歌翻译）：')
    print('-' * 40)
    for code in sorted(LANG_NAMES.keys()):
        print(f'  {code:6s} {LANG_NAMES[code]}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法：')
        print('  python gen_i18n_sql.py <语言代码>                  # 生成 SQL（缺失时自动翻译）')
        print('  python gen_i18n_sql.py <语言代码> --force          # 强制用谷歌翻译覆盖')
        print('  python gen_i18n_sql.py <语言代码> -o output.sql    # 输出到文件')
        print('  python gen_i18n_sql.py --list                     # 列出支持的语言')
        print('')
        print('示例：')
        print('  python gen_i18n_sql.py uz                  # 翻译生成乌兹别克语')
        print('  python gen_i18n_sql.py ar -o ar.sql        # 翻译并保存到文件')
        print('  python gen_i18n_sql.py zh                  # 使用本地中文数据')
        sys.exit(1)

    if sys.argv[1] == '--list':
        list_supported_languages()
        sys.exit(0)

    lang = sys.argv[1].strip().lower()
    force = '--force' in sys.argv

    # 查找 -o 参数
    output_file = None
    for i, arg in enumerate(sys.argv):
        if arg == '-o' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            break

    sql = generate_i18n_sql(lang, force_translate=force)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql)
        print(f'\nSQL 已保存到: {output_file}')
    else:
        print(sql)