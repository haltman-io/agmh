## Summary

- 

## Validation

- [ ] `python -m compileall -q src tests`
- [ ] `PYTHONPATH=src python -m unittest discover -s tests -v`
- [ ] `python -m pip install -e . --dry-run --no-deps`

## Checklist

- [ ] User-facing behavior is documented.
- [ ] Secrets are not logged or exposed.
- [ ] Source/destination terminology remains consistent.
- [ ] `CHANGELOG.md` is updated when behavior changes.

## Security

Do not include private vulnerability details in this pull request. Follow
`SECURITY.md` instead.

