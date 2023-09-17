# CHANGELOG



## v2.2.5 (2023-09-17)

### Fix

* fix(build): update release order ([`db88117`](https://github.com/taylorhakes/python-redis-cache/commit/db88117f060fb6fc0515cbf2ee3485377d5e95a8))


## v2.2.4 (2023-09-16)

### Fix

* fix(release): fix version change ([`d434cb6`](https://github.com/taylorhakes/python-redis-cache/commit/d434cb6dacae29022eb7176f59777225f8b2c782))


## v2.2.3 (2023-09-16)

### Fix

* fix(build): fetch depth ([`18fd8af`](https://github.com/taylorhakes/python-redis-cache/commit/18fd8af81759c4e94b772bd8360b42c107da786c))


## v2.2.2 (2023-09-16)

### Fix

* fix(release): fix missing permission ([`d4136e1`](https://github.com/taylorhakes/python-redis-cache/commit/d4136e1c6768fd7b635186aca0cd4b1f7011470b))


## v2.2.1 (2023-09-16)

### Documentation

* docs: remove version badge ([`f0810d2`](https://github.com/taylorhakes/python-redis-cache/commit/f0810d2ca42325592aa4b98c01608f022fcd900d))

* docs: update readme badge ([`bdbe5e1`](https://github.com/taylorhakes/python-redis-cache/commit/bdbe5e17ccd3926c58ffd69b58b6775ca71bbc56))

* docs(readme): add exception_handler into signature ([`8bb9193`](https://github.com/taylorhakes/python-redis-cache/commit/8bb9193014c2b556b547871aeb572ea3ec447505))

* docs(readme): add note about decode_responses ([`9471fb0`](https://github.com/taylorhakes/python-redis-cache/commit/9471fb0b660820cbf7a3a00b3ce8e75d7a50a79b))

* docs(readme): update docs about exception_handler parameter ([`70d48c1`](https://github.com/taylorhakes/python-redis-cache/commit/70d48c1cf89505915972fae3bae57e8b07945e4c))

### Fix

* fix(build): Permissions ([`0e45716`](https://github.com/taylorhakes/python-redis-cache/commit/0e457165b2d7b48178ae3c2fed521e507ef6ae51))

* fix(release): add pypi distribution ([`508f5a8`](https://github.com/taylorhakes/python-redis-cache/commit/508f5a87c73adf90da337ce9aad7791d33f24742))


## v2.2.0 (2023-07-25)

### Feature

* feat(exceptions): add ability to handle redis exceptions ([`dad5ac0`](https://github.com/taylorhakes/python-redis-cache/commit/dad5ac03253f7b3fd5b7bf725f549beebda09f09))

### Test

* test: update python versions in tests ([`3e4afdb`](https://github.com/taylorhakes/python-redis-cache/commit/3e4afdb976e99c56d9e1f660b23f024d77ed3406))

* test: bump redis from 3.5.3 to 4.4.4 (#22)

Bumps [redis](https://github.com/redis/redis-py) from 3.5.3 to 4.4.4.
- [Release notes](https://github.com/redis/redis-py/releases)
- [Changelog](https://github.com/redis/redis-py/blob/master/CHANGES)
- [Commits](https://github.com/redis/redis-py/compare/3.5.3...v4.4.4)

---
updated-dependencies:
- dependency-name: redis
  dependency-type: direct:development
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`3c3674f`](https://github.com/taylorhakes/python-redis-cache/commit/3c3674f44983f2a95f401cec85f7aeabd09750c6))

* test: change name of test ([`0ee3e81`](https://github.com/taylorhakes/python-redis-cache/commit/0ee3e818eb64793699517eba29b468cc221fddeb))


## v2.1.2 (2023-05-15)

### Fix

* fix(perf): update list to set ([`a4984bb`](https://github.com/taylorhakes/python-redis-cache/commit/a4984bb980ed40bb7c0cf077a69ece823becf3e2))


## v2.1.1 (2023-05-15)

### Fix

* fix(cache): Fix bug in variable args ([`3dce0e7`](https://github.com/taylorhakes/python-redis-cache/commit/3dce0e774ee00b914bbbf5aaac6b5cce3589968f))

### Test

* test: add test for args, kwargs mix ([`68f09ba`](https://github.com/taylorhakes/python-redis-cache/commit/68f09bab88bca27a3565c1360cb75c464ddc7d31))


## v2.1.0 (2023-05-11)

### Documentation

* docs(readme): update docs to specify Python 3.7 ([`145693d`](https://github.com/taylorhakes/python-redis-cache/commit/145693d07b83ac1ecc046841c8a82aba2ec6e6f4))

### Feature

* feat: fix caching to work on cluster ([`69c1377`](https://github.com/taylorhakes/python-redis-cache/commit/69c13775aeec21e8994228d61e22482a0c12a324))


## v2.0.0 (2023-01-12)

### Breaking

* fix: update key names to prevent bug

BREAKING CHANGE: changes key algorithm to avoid bug with name conflict

Use `copy_old_keys` to migrate data. ([`c9efd2d`](https://github.com/taylorhakes/python-redis-cache/commit/c9efd2de7247fe4974bd6e29e790b3011e9b9581))

### Build

* build(actions): add commit message validation on PRs ([`f2f8f35`](https://github.com/taylorhakes/python-redis-cache/commit/f2f8f356cdae1b7fea085e7f8dcc04a2e541b28d))

* build(workflow): update cron to run once every 10 days ([`f8c086d`](https://github.com/taylorhakes/python-redis-cache/commit/f8c086d7e4b8e9579cca1d1e1bf82ff5d353f8e2))

* build(workflow): add stale github issue closer ([`90b9358`](https://github.com/taylorhakes/python-redis-cache/commit/90b9358c353b8cde6ab26146def9a0e03c2c86a8))

### Unknown

* doc(README): update readme mget ([`1401856`](https://github.com/taylorhakes/python-redis-cache/commit/14018568b4cc80cf22584ce22313e6d1294e3c89))

* Merge pull request #9 from AdrianDeAnda/python-310

Add Python 3.10 tests to Github Actions ([`1c4e6c1`](https://github.com/taylorhakes/python-redis-cache/commit/1c4e6c1e9b62e6978f8e82169dfefd228d841621))

* Add Python 3.10 tests to Github Actions ([`fc8dbb5`](https://github.com/taylorhakes/python-redis-cache/commit/fc8dbb56b694e36f44eed3672795eea1469a0ba4))


## v1.2.0 (2021-10-22)

### Feature

* feat: key_serializer for custom serialization ([`1d4d1eb`](https://github.com/taylorhakes/python-redis-cache/commit/1d4d1eb24e2830a2c0cee509d65c9e9b772f08ff))


## v1.1.2 (2021-09-02)

### Fix

* fix: add newline to pyproject.toml ([`d6677a4`](https://github.com/taylorhakes/python-redis-cache/commit/d6677a4eb3890f384c4d7aeef9b1ebe8593636e1))

### Unknown

* bugfix: Add missing pyproject.toml ([`fd89d46`](https://github.com/taylorhakes/python-redis-cache/commit/fd89d462c71d9988df22f4523d1be892a5f87eaf))

* bugfix: correct release.yml format ([`7b37dfd`](https://github.com/taylorhakes/python-redis-cache/commit/7b37dfd800137006c6b72cff38224327b73303d9))

* bugfix: add release.yml ([`0df737c`](https://github.com/taylorhakes/python-redis-cache/commit/0df737c315f60aae5473769e27910ae62f7f20da))

* Change python_requires to &gt;3.6 ([`a6ca0f1`](https://github.com/taylorhakes/python-redis-cache/commit/a6ca0f1871636c5f1335e01a2335dcf21499373e))

* Merge pull request #6 from AdrianDeAnda/python-39

Add support for Python 3.9 ([`3f5334f`](https://github.com/taylorhakes/python-redis-cache/commit/3f5334f1d599ac88d144c480b5717c653d784b95))

* Add support for Python 3.9 ([`ce1768d`](https://github.com/taylorhakes/python-redis-cache/commit/ce1768dba1331b013366389b39aeeb3b1017b229))

* Commit new version ([`0f7d0d4`](https://github.com/taylorhakes/python-redis-cache/commit/0f7d0d4d40dacac75b98701ee0c9e0dec7a73210))

* Merge pull request #3 from lfvilella/master

Fixing invalidate_all ([`68132cb`](https://github.com/taylorhakes/python-redis-cache/commit/68132cbdca69feb17f9472fd8cf7b06c1beec892))

* fix review ([`e3a0f16`](https://github.com/taylorhakes/python-redis-cache/commit/e3a0f16d4a10501cf88d8a3bc721b51f1f079dc6))

* Code review changes

1) test in different redis versions
2) fixing invalidate_all ([`5335b70`](https://github.com/taylorhakes/python-redis-cache/commit/5335b700626cd315323df20a395b336c4140abe0))

* test in different redis versions ([`4cac5d8`](https://github.com/taylorhakes/python-redis-cache/commit/4cac5d8e810e50b3e2e216f1f44dc939cad61ee2))

* 1) Make zrange works by adding zadd
2) always clear the cache on tests ([`69e8815`](https://github.com/taylorhakes/python-redis-cache/commit/69e8815d429e5fffd4e23a97d1f5595b1d415739))

* CI test in different python versions (#1) ([`60e7c71`](https://github.com/taylorhakes/python-redis-cache/commit/60e7c712c417c5e28948c9e335399274911c6ad9))

* update readme and define py versions ([`c3ba154`](https://github.com/taylorhakes/python-redis-cache/commit/c3ba154c654395d527ac2d80f7b18097cc19d175))

* Create CI.yml ([`bb064c5`](https://github.com/taylorhakes/python-redis-cache/commit/bb064c58fba229f8e5980f454b380d97cd2099a9))

* refactoring tests ([`5d6be6c`](https://github.com/taylorhakes/python-redis-cache/commit/5d6be6c3a3716bdd3de3529215fb1cabfcf4d91e))

* refactoring tests ([`d2afb81`](https://github.com/taylorhakes/python-redis-cache/commit/d2afb81900de145414c6d48221b0af1314077fd7))

* Revert &#34;fixing invalidate_all&#34;

This reverts commit 3c8194c85c66d46209e09de3657530641503d408. ([`c6c56ce`](https://github.com/taylorhakes/python-redis-cache/commit/c6c56cef06e044381da5bf0314abc796876d3190))

* fix cache key ([`f2b35f8`](https://github.com/taylorhakes/python-redis-cache/commit/f2b35f8ff9716fe3e9c2869c0e8291a95107f631))

* fixing invalidate_all ([`3c8194c`](https://github.com/taylorhakes/python-redis-cache/commit/3c8194c85c66d46209e09de3657530641503d408))

* Fix bug in calling cache twice ([`98c4daf`](https://github.com/taylorhakes/python-redis-cache/commit/98c4daf441a9e17445b571db4e18197ac70237dc))

* Fixed mget test to check values ([`4665045`](https://github.com/taylorhakes/python-redis-cache/commit/4665045a7dfb5d1ec63c2b44ae528761dbbd5534))

* Add basic multi get ([`2dc865e`](https://github.com/taylorhakes/python-redis-cache/commit/2dc865e7515ed45684cfee021a6dceb62e6bf60e))

* Remove hashing to avoid collisions on key values ([`8a89e7d`](https://github.com/taylorhakes/python-redis-cache/commit/8a89e7d750b6dedb34397afe7aee19cde17baaa7))

* Fixed bug for deserializer and serializer that returns bytes ([`4643c9e`](https://github.com/taylorhakes/python-redis-cache/commit/4643c9e0678f0ab80dddbf1f7f81de614e5fd1a3))

* Added link to pickle security issues ([`99d623b`](https://github.com/taylorhakes/python-redis-cache/commit/99d623b4ee295fe6bc7b4f9376bb7b276178761a))

* Add test for pickle and custom serializer ([`b1564d4`](https://github.com/taylorhakes/python-redis-cache/commit/b1564d44aea8dbdea0a8c1ea9cf6606b76e437b9))

* Changed the requirements to be clear the version could be higher ([`669fee9`](https://github.com/taylorhakes/python-redis-cache/commit/669fee974f11893a2d4e7d5b1195a5386adb2921))

* Add test.sh script to run docker tests ([`300dd48`](https://github.com/taylorhakes/python-redis-cache/commit/300dd4867c46f4757ca11aa571b14276d947644e))

* Update wording on readme ([`496bf6f`](https://github.com/taylorhakes/python-redis-cache/commit/496bf6fd97149e64e297f5dc396d6011d78087e2))

* Add explanation of how to call the function ([`f5dfc65`](https://github.com/taylorhakes/python-redis-cache/commit/f5dfc653e8a0b357ef8792e3eff7b14eecad6192))

* Fix formatting ([`c49d5b0`](https://github.com/taylorhakes/python-redis-cache/commit/c49d5b0237d3eea0751fa49144aaac86a4ae7f28))

* Updated readme to provide more detail on ttl and limit parmeters ([`238e5f0`](https://github.com/taylorhakes/python-redis-cache/commit/238e5f05da7a5a6ffade113469fa819b375bc6b8))

* Save values in cache if it doesn&#39;t exist ([`7855cdd`](https://github.com/taylorhakes/python-redis-cache/commit/7855cddab55b6b5d45cb01d961643966b86db319))

* Update readme formatting ([`8c31654`](https://github.com/taylorhakes/python-redis-cache/commit/8c31654c7ab92c98df0ae1f7601362128d29850f))

* Updated readme with invalidate API ([`0521037`](https://github.com/taylorhakes/python-redis-cache/commit/05210377e154243b3d42ff4761482a6a3cd775cc))

* Added invalidate and invalidate_all ([`75fba53`](https://github.com/taylorhakes/python-redis-cache/commit/75fba538fd5a92fd6a34597369790f3439d69fa1))

* Add lua updates ([`29693cd`](https://github.com/taylorhakes/python-redis-cache/commit/29693cd949839b56ff25cb3cccd203043e464141))

* Add tests against real redis ([`173dc01`](https://github.com/taylorhakes/python-redis-cache/commit/173dc01406da3ed2acc182e60e6ae8c8951323dd))

* Updated readme ([`100e3a0`](https://github.com/taylorhakes/python-redis-cache/commit/100e3a0c901a7a74554e740ebafad343c4d5f9da))

* Add API docs ([`0bd5786`](https://github.com/taylorhakes/python-redis-cache/commit/0bd578628d2f6f1050888287bc1330d5b7cddc4e))

* Update readme ([`933712b`](https://github.com/taylorhakes/python-redis-cache/commit/933712bd3ac6681bc4c4e23625ddf19f328b5502))

* Add python code ([`a033d79`](https://github.com/taylorhakes/python-redis-cache/commit/a033d79742a998c7a6ca2228d2c064294e55d4ec))

* Initial commit ([`5135a44`](https://github.com/taylorhakes/python-redis-cache/commit/5135a44e9e0dad996be3113dbbc09ac43d2206c0))
