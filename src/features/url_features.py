"""url_lexical_v1: deterministic features from explicit HTTP(S) URL text.

No DNS, HTTP, WHOIS or certificate requests. Original text is never trimmed,
decoded or rewritten. Counts include path, query and fragment. Parsed hostname
length uses Python's lowercase hostname without IPv6 brackets. Grouping alone
uses IDNA and strips a trailing dot. These are new features, not reproductions
of the dataset's undocumented recorded features.
"""
import ipaddress
import re
from urllib.parse import urlsplit

SCHEMA_VERSION = 'url_lexical_v1'
FEATURE_NAMES = (
    'url_length', 'hostname_length', 'has_at_symbol', 'has_dash', 'count_dots',
    'has_https', 'digit_count', 'digit_ratio', 'path_length', 'query_length',
    'count_query_parameters', 'count_percent_escapes', 'hostname_is_ip', 'has_explicit_port',
)


def _parse(url):
    if not isinstance(url, str) or not url:
        raise ValueError('URL must be a nonempty string.')
    if any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url):
        raise ValueError('Whitespace and control characters are not accepted.')
    try:
        p = urlsplit(url)
        if p.scheme.lower() not in {'http', 'https'} or not p.hostname:
            raise ValueError('Explicit HTTP(S) scheme and hostname required.')
        port = p.port  # Validates numeric ports and range.
        if port == 0 or p.netloc.endswith(':'):
            raise ValueError('Explicit port must be between 1 and 65535.')
        if '\\' in p.netloc or '%' in p.hostname:
            raise ValueError('Backslash or encoded/scoped hostname is unsupported.')
        try:
            ipaddress.ip_address(p.hostname)
            is_ip = 1
        except ValueError:
            is_ip = 0
            ascii_host = p.hostname.rstrip('.').encode('idna').decode('ascii')
            if len(ascii_host) > 253 or any(not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?', label) for label in ascii_host.split('.')):
                raise ValueError('Invalid hostname.')
        return p, is_ip
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f'Invalid URL: {exc}') from exc


def hostname_group(url: str) -> str:
    """Observed host key matching the EDA split; not a registered domain."""
    p, _ = _parse(url)
    return p.hostname.rstrip('.').encode('idna').decode('ascii').lower()


def extract_url_features(url: str) -> dict[str, int | float]:
    """Return finite predictors in FEATURE_NAMES order, or raise ValueError.

    HTTPS means scheme only. Digits are ASCII 0-9. Query field count is the
    number of nonempty ampersand-separated pieces, not distinct parameter names.
    Percent escapes count syntactically valid %HH sequences without decoding.
    Userinfo and valid ports are accepted. Unicode is counted in code points.
    """
    p, is_ip = _parse(url)
    digits = sum(c in '0123456789' for c in url)
    values = (len(url), len(p.hostname), int('@' in url), int('-' in url),
              url.count('.'), int(p.scheme.lower() == 'https'), digits,
              digits / len(url), len(p.path), len(p.query),
              sum(bool(x) for x in p.query.split('&')),
              len(re.findall(r'%[0-9a-fA-F]{2}', url)), is_ip, int(p.port is not None))
    return dict(zip(FEATURE_NAMES, values, strict=True))


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    args = parser.parse_args()
    try:
        print(json.dumps(extract_url_features(args.url), indent=2))
    except ValueError as exc:
        parser.error(str(exc))
