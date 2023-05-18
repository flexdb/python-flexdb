# Copyright (C) 2023 FlexDB <team@flexdb.co>
# Use of this source code is governed by the GPL-3.0
# license that can be found in the LICENSE file.

.PHONY: clean build publish test

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf flexdb.egg-info/

build: clean
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

test:
	pytest -s tests/
