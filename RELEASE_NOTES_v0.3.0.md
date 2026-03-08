# WebWatcher v0.3.0

This release makes WebWatcher much easier to try and more useful in real-world scenarios.

## Highlights

- Added **CSS selector-based monitoring**
- Added **Feishu webhook notifications**
- Added **Dockerfile** and **docker-compose** support
- Improved README examples and quick start experience

## Example

```bash
python app.py add --url https://news.ycombinator.com --selector '.titleline' --interval 600 --name "HN Titles"
python app.py check
```

## Good fit for

- job page monitoring
- announcement pages
- competitor price pages
- ranking pages
- documentation updates

## Notes

This is still a deliberately small release.
No user system, no SaaS panel, no overbuilt architecture.
Just a practical foundation for website change monitoring.
