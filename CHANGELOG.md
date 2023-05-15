# Changelog

<!--next-version-placeholder-->

## v2.1.1 (2023-05-15)
### Fix
* **cache:** Fix bug in variable args ([`3dce0e7`](https://github.com/taylorhakes/python-redis-cache/commit/3dce0e774ee00b914bbbf5aaac6b5cce3589968f))

## v2.1.0 (2023-05-11)
### Breaking Fixes!
All cache keys will change to accommodate for the following fixes
* Update key names to prevent bug ([`c9efd2d`](https://github.com/taylorhakes/python-redis-cache/commit/c9efd2de7247fe4974bd6e29e790b3011e9b9581))
* Update to get consistent values from args and kwarg
* Base64 encode keys to fix {} being interpreted by redis as hash

### Feature
* Fix caching to work on cluster ([`69c1377`](https://github.com/taylorhakes/python-redis-cache/commit/69c13775aeec21e8994228d61e22482a0c12a324))

### Documentation
* **readme:** Update docs to specify Python 3.7 ([`145693d`](https://github.com/taylorhakes/python-redis-cache/commit/145693d07b83ac1ecc046841c8a82aba2ec6e6f4))

## v1.2.0 (2021-10-22)
### Feature
* Key_serializer for custom serialization ([`1d4d1eb`](https://github.com/taylorhakes/python-redis-cache/commit/1d4d1eb24e2830a2c0cee509d65c9e9b772f08ff))

## v1.1.2 (2021-09-02)
### Fix
* Add newline to pyproject.toml ([`d6677a4`](https://github.com/taylorhakes/python-redis-cache/commit/d6677a4eb3890f384c4d7aeef9b1ebe8593636e1))
