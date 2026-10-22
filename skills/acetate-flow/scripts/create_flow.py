#!/usr/bin/env python3
"""Render workflow JSON into an offline, standalone HTML file."""
import argparse
import json
import math
from pathlib import Path
import re

KINDS = {'data', 'tool', 'ai', 'agent', 'rule', 'output', 'error'}
PORTS = {'left', 'right', 'top', 'bottom'}


def validate(config):
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def number(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    def identifier(value):
        return isinstance(value, str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', value)

    require(isinstance(config, dict), 'Config must be an object')
    require(isinstance(config.get('title', ''), str), 'title must be text')
    require(isinstance(config.get('readyText', ''), str), 'readyText must be text')
    board = config.get('board', {})
    require(isinstance(board, dict), 'board must be an object')
    for key in ('width', 'height', 'scale'):
        if key in board:
            require(number(board[key]) and board[key] > 0, f'board.{key} must be positive')
    nodes, edges, scenarios = (config.get(key) for key in ('nodes', 'edges', 'scenarios'))
    require(isinstance(nodes, list) and nodes, 'nodes must be a nonempty array')
    require(isinstance(edges, list), 'edges must be an array')
    require(isinstance(scenarios, list) and scenarios, 'scenarios must be a nonempty array')
    ids = set()
    for n in nodes:
        require(isinstance(n, dict), 'Each node must be an object')
        nid = n.get('id')
        require(identifier(nid) and nid not in ids, f'Invalid or duplicate node ID: {nid}')
        ids.add(nid)
        require(n.get('kind') in KINDS, f'Unknown kind for {nid}')
        require(number(n.get('x')) and number(n.get('y')), f'{nid}: x/y must be finite numbers')
        require(isinstance(n.get('title'), str) and n['title'], f'{nid}: title required')
        for key in ('subtitle', 'input', 'output', 'description', 'note', 'narration'):
            require(isinstance(n.get(key, ''), str), f'{nid}.{key} must be text')
            n.setdefault(key, '')
    pairs, keys, execution = set(), set(), set()
    for edge in edges:
        require(isinstance(edge, dict), 'Each edge must be an object')
        a, b = edge.get('from'), edge.get('to')
        require(isinstance(a, str) and isinstance(b, str) and a in ids and b in ids, 'Edge references unknown node')
        key = a + '-' + b
        require((a, b) not in pairs and key not in keys, f'Duplicate or ambiguous edge: {a} → {b}')
        pairs.add((a, b)); keys.add(key)
        require(edge.get('kind', '') in ('', 'payload', 'error'), 'Unsupported edge kind')
        if edge.get('kind') != 'payload':
            execution.add((a, b))
        for port in ('sourcePort', 'targetPort'):
            require(port not in edge or edge[port] in PORTS, f'Invalid {port}')
        require(isinstance(edge.get('via', []), list), 'via must be an array')
        for point in edge.get('via', []):
            require(isinstance(point, list) and len(point) == 2 and all(number(v) for v in point), 'via points must be [x,y]')
        if 'label' in edge:
            require(isinstance(edge['label'], str) and all(number(edge.get(k)) for k in ('labelX', 'labelY')), 'Edge labels require text and labelX/Y')
    scenario_ids = set()
    for scenario in scenarios:
        require(isinstance(scenario, dict), 'Each scenario must be an object')
        sid = scenario.get('id')
        require(identifier(sid) and sid not in scenario_ids, f'Invalid or duplicate scenario ID: {sid}')
        scenario_ids.add(sid)
        require(isinstance(scenario.get('label'), str) and scenario['label'], 'Scenario label required')
        path = scenario.get('path')
        require(isinstance(path, list) and path and all(isinstance(n, str) and n in ids for n in path), f'{sid}: invalid path')
        require(all((a, b) in execution for a, b in zip(path, path[1:])), f'{sid}: path contains disconnected steps')
        overrides = scenario.get('data', {})
        require(isinstance(overrides, dict) and set(overrides) <= ids, f'{sid}: invalid data override keys')
    require(isinstance(config.get('labels', []), list), 'labels must be an array')
    for label in config.get('labels', []):
        require(isinstance(label, dict) and isinstance(label.get('text'), str) and all(number(label.get(k)) for k in ('x', 'y')), 'Invalid canvas label')
    samples = config.get('samples', {})
    require(isinstance(samples, dict), 'samples must be an object')

    def check_refs(value, stack=()):
        if isinstance(value, list):
            for item in value:
                check_refs(item, stack)
        elif isinstance(value, dict):
            if set(value) == {'$ref'}:
                key = value['$ref']
                require(isinstance(key, str) and key in samples, 'Unknown sample reference')
                require(key not in stack, 'Circular sample reference')
                check_refs(samples[key], (*stack, key))
            else:
                for item in value.values():
                    check_refs(item, stack)

    for value in samples.values():
        check_refs(value)
    for n in nodes:
        check_refs(n.get('data'))
    for scenario in scenarios:
        check_refs(scenario.get('data', {}))
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--config', type=Path, help='Workflow JSON; defaults to the classification example')
    parser.add_argument('--force', action='store_true', help='Replace the requested output file')
    args = parser.parse_args()
    assets = Path(__file__).resolve().parents[1] / 'assets'
    try:
        config = validate(json.loads((args.config or assets / 'classification.json').read_text()))
        payload = json.dumps(config, ensure_ascii=True, allow_nan=False, separators=(',', ':'))
        # JSON is data, never executable; prevent closing the embedding script tag.
        payload = payload.replace('&', r'\u0026').replace('<', r'\u003c').replace('>', r'\u003e')
        template = (assets / 'renderer.html').read_text()
        if template.count('{{FLOW_JSON}}') != 1:
            raise ValueError('Renderer must contain exactly one JSON insertion slot')
        html = template.replace('{{FLOW_JSON}}', payload)
        with args.destination.open('w' if args.force else 'x') as output:
            output.write(html)
    except (OSError, ValueError, TypeError, RecursionError) as error:
        parser.exit(1, f'{error}\n')
    print(args.destination.resolve())


if __name__ == '__main__':
    main()
