# Vendored front-end libraries (RPG skill tree)

Downloaded for offline / stable use by `/skills/book/`.

| File | Package | License |
|---|---|---|
| `cytoscape.min.js` | cytoscape@3.30.4 | MIT |
| `elk.bundled.js` | elkjs@0.9.3 | EPL-2.0 |
| `cytoscape-elk.js` | cytoscape-elk@2.2.0 | MIT |
| `pixi.min.js` | pixi.js@8.6.6 | MIT |

Re-download:

```text
# from repo root (PowerShell)
Invoke-WebRequest https://cdn.jsdelivr.net/npm/cytoscape@3.30.4/dist/cytoscape.min.js -OutFile docs/skills/book/vendor/cytoscape.min.js
Invoke-WebRequest https://cdn.jsdelivr.net/npm/elkjs@0.9.3/lib/elk.bundled.js -OutFile docs/skills/book/vendor/elk.bundled.js
Invoke-WebRequest https://cdn.jsdelivr.net/npm/cytoscape-elk@2.2.0/dist/cytoscape-elk.js -OutFile docs/skills/book/vendor/cytoscape-elk.js
Invoke-WebRequest https://cdn.jsdelivr.net/npm/pixi.js@8.6.6/dist/pixi.min.js -OutFile docs/skills/book/vendor/pixi.min.js
```
