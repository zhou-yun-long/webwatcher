# WebWatcher v0.3.0

This release makes WebWatcher more practical for real-world website monitoring, especially when pages rely on JavaScript rendering.

## Highlights

- Added **Playwright-based dynamic page monitoring**
- Added **CSS selector-based monitoring**
- Added **noise filtering** for unstable content
- Added **JSON config file support**
- Added **Feishu webhook notifications**
- Added **Dockerfile** and **docker-compose** support
- Improved README examples and quick start experience

## Example

```bash
cp webwatcher.example.json webwatcher.json
python app.py init
python app.py config-show

python app.py add \
  --url https://example.com/dashboard \
  --name "Dynamic Example" \
  --fetch-mode playwright \
  --wait-for-selector '#app' \
  --wait-after-load-ms 1500

python app.py check
```

## Config support

You can now configure:
- database path
- default fetch timeout
- default fetch mode
- default Playwright wait options
- Feishu webhook URL

## Good fit for

- job page monitoring
- announcement pages
- competitor price pages
- ranking pages
- documentation updates
- JavaScript-rendered dashboards or SPAs

## Notes

This is still a deliberately small release.
No user system, no SaaS panel, no overbuilt architecture.
Just a practical foundation for website change monitoring.

If you use Playwright mode, remember to install browser binaries:

```bash
python -m playwright install chromium
```
