from pathlib import Path
import re

path = Path('index.html')
s = path.read_text()

worker = 'https://duelcut-tmdb-proxy.kiah-harpool.workers.dev'
old_key = "const DEFAULT_API_KEY = 'aa8d690a98a62069774ffbaf2cdc2479';"

if old_key in s:
    s = s.replace(old_key, "const DEFAULT_API_KEY = 'proxy';", 1)

s = s.replace('https://api.themoviedb.org', worker)

old_settings = '''    <h2 class="display">TMDB API Key <span style="color:var(--text-dim);font-weight:400;">(optional)</span></h2>
    <p>Duel Cut already works out of the box. If you'd rather use your own TMDB key instead of the built-in one, grab a free key from
      <a href="https://www.themoviedb.org/settings/api" target="_blank">themoviedb.org/settings/api</a>
      and paste it below. Leave blank to use the default.</p>
    <input id="api-key-input" type="text" placeholder="Optional — paste your own TMDB API key">
    <div class="row">
      <button class="cancel" id="settings-cancel">Cancel</button>
      <button class="save" id="settings-save">Save</button>
    </div>
'''
new_settings = '''    <h2 class="display">Settings</h2>
    <div class="row">
      <button class="cancel" id="settings-cancel">Close</button>
    </div>
'''
if old_settings in s:
    s = s.replace(old_settings, new_settings, 1)
    s = s.replace("  el('settings-save').onclick = saveApiKey;\n", "", 1)
    s = s.replace("  el('api-key-input').value = state.apiKeyOverride || '';\n", "", 1)
    s = re.sub(
        r"\nasync function saveApiKey\(\)\{.*?\n\}\n\nasync function runSearch",
        "\nasync function runSearch",
        s,
        count=1,
        flags=re.S,
    )

old_init = "  const key = await storageGet('duelcut:api-key');\n  state.apiKeyOverride = key || null;\n  state.apiKey = key || DEFAULT_API_KEY;\n"
new_init = "  state.apiKeyOverride = null;\n  state.apiKey = DEFAULT_API_KEY;\n  try{ localStorage.removeItem('duelcut:api-key'); }catch(e){}\n"
if old_init in s:
    s = s.replace(old_init, new_init, 1)

if 'aa8d690a98a62069774ffbaf2cdc2479' in s:
    raise SystemExit('Exposed TMDB key still present')
if 'https://api.themoviedb.org' in s:
    raise SystemExit('Direct TMDB host still present')
if worker not in s:
    raise SystemExit('Worker URL was not added')

path.write_text(s)
