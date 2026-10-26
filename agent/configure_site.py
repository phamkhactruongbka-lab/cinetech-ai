"""Generate absolute sitemap URLs only after a real deployment URL is known."""
import argparse
from xml.etree.ElementTree import Element, SubElement, ElementTree
try:
    from .common import ROOT, https_url
except ImportError:
    from common import ROOT, https_url
from urllib.parse import urlsplit
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--url', required=True)
    args = p.parse_args()
    if not https_url(args.url) or urlsplit(args.url).query or urlsplit(args.url).fragment:
        p.error('Use an absolute HTTPS deployment URL without query or fragment')
    base = args.url.rstrip('/') + '/'
    tree = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for page in ('', 'affiliate.html', 'quyen-rieng-tu.html', 'lien-he.html'):
        SubElement(SubElement(tree, 'url'), 'loc').text = base + page
    ElementTree(tree).write(ROOT/'docs/sitemap.xml', encoding='utf-8', xml_declaration=True)
    (ROOT/'docs/robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'sitemap.xml\n', encoding='utf-8')
