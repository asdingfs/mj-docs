#!/usr/bin/env python3
"""Read-only link, publication-boundary, and mapped-source drift checks.

Run from any directory. Exit 0: checks pass; 1: review required; 2: bad input.
No network calls, Git writes, or fingerprint refreshes.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.missing_alt = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        key = 'src' if tag == 'img' else 'href' if tag == 'a' else None
        if key and data.get(key):
            self.targets.append(data[key])
        if tag == 'img' and not data.get('alt', '').strip():
            self.missing_alt += 1


def references(text):
    parser = References()
    parser.feed(text)
    targets = list(parser.targets)
    # Supports ordinary Markdown, angle-wrapped paths and optional link titles.
    pattern = r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)'
    targets += [m.group(1).strip('<>') for m in re.finditer(pattern, text)]
    targets += re.findall(r'{%\s*content-ref\s+url="([^"]+)"', text)
    return targets, parser.missing_alt


def check(root, code_root=None, source_ref=None, working_tree=False):
    manifest = json.loads((root/'context/source-map.json').read_text())
    errors, warnings = [], []
    publish_roots = [(root/name).resolve() for name in manifest['published_directories']]
    pages = list(root.rglob('*.md'))
    for page in pages:
        if '.git' in page.relative_to(root).parts:
            continue
        name = page.relative_to(root).as_posix()
        text = page.read_text()
        targets, missing_alt = references(text)
        public = any(page.is_relative_to(p) for p in publish_roots)
        for target in targets:
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            if parts.path.startswith('/'):
                warnings.append(f'{name}: site-relative link needs native preview: {target}')
                continue
            resolved = (page.parent/unquote(parts.path)).resolve()
            if public and not any(resolved.is_relative_to(p) for p in publish_roots):
                errors.append(f'{name}: public link escapes published roots: {target}')
            if not resolved.exists():
                errors.append(f'{name}: missing local target: {target}')
        if public and missing_alt:
            warnings.append(f'{name}: {missing_alt} image(s) lack descriptive alt text')
        if public and name.endswith('SUMMARY.md'):
            continue
        prose = re.sub(r'^#{1,6}.*$', '', text, flags=re.M).strip()
        if public and not prose:
            warnings.append(f'{name}: existing empty page needs owner content')

    config = root/'gitbook-docs.yaml'
    if digest(config) != manifest['gitbook_config_sha256']:
        errors.append('GitBook configuration changed: review space identities and publication roots before updating its baseline')
    for directory in manifest['published_directories']:
        for name in ['README.md', 'SUMMARY.md']:
            if not (root/directory/name).is_file():
                errors.append(f'{directory}/{name}: missing GitBook entry file')

    for name, expected in manifest['pages'].items():
        path = root/name
        if not path.is_file() or digest(path) != expected:
            errors.append(f'{name}: documentation changed since evidence review; re-check prose and mapping')

    if code_root is not None:
        if not code_root.is_dir():
            raise ValueError(f'Code reference directory not found: {code_root}')
        revision = None
        if not working_tree:
            ref = source_ref or manifest['source_ref']
            result = subprocess.run(['git', '-C', str(code_root), 'rev-parse', '--verify', ref + '^{commit}'], capture_output=True)
            if result.returncode:
                raise ValueError(f'Cannot resolve source ref {ref}; no working-tree fallback. Supply an isolated reference copy with this object.')
            revision = result.stdout.decode().strip()
            print(f'Source reference: {ref} at {revision}')
            if revision != manifest['code_revision']:
                warnings.append('Source revision differs from the reviewed commit; also inspect changes outside mapped files')
        else:
            print('Diagnostic mode: comparing working-tree files, not the designated development branch.')
        changed = set()
        for name, expected in manifest['sources'].items():
            if revision:
                result = subprocess.run(['git', '-C', str(code_root), 'show', f'{revision}:{name}'], capture_output=True)
                actual = hashlib.sha256(result.stdout).hexdigest() if result.returncode == 0 else None
            else:
                path = code_root/name
                actual = digest(path) if path.is_file() else None
            if actual != expected:
                changed.add(name)
        for group in manifest['groups']:
            triggers = sorted(changed.intersection(group['sources']))
            if triggers:
                errors.append('Source drift: ' + ', '.join(triggers) + '\n  Review pages: ' + ', '.join(group['pages']))
        print(f'Compared {len(manifest["sources"])} source files without writing to the code repository.')
    else:
        warnings.append('Source drift was not checked; supply --code-root to include it')

    for item in errors:
        print('REVIEW:', item)
    for item in warnings:
        print('NOTE:', item)
    print(f'{len(pages)} Markdown files checked; {len(errors)} review issue(s), {len(warnings)} note(s).')
    print('Limits: no network/anchor checks, deployment verification, or native GitBook render; unmapped semantic changes need manual review.')
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--docs-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--code-root', type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--source-ref', help='Git reference to inspect; defaults to source-map.json source_ref')
    mode.add_argument('--working-tree', action='store_true', help='Explicit diagnostic comparison of checked-out files')
    args = parser.parse_args()
    try:
        if (args.source_ref or args.working_tree) and not args.code_root:
            parser.error('--source-ref and --working-tree require --code-root')
        return check(args.docs_root.resolve(), args.code_root.resolve() if args.code_root else None, args.source_ref, args.working_tree)
    except (OSError, ValueError, KeyError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
