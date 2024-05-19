#!/bin/bash

VERSION=$(cat setup.py | grep version | cut -d '"' -f 2)
git fetch --tags

if ! git rev-parse v${VERSION} >/dev/null 2>&1; then
  git tag v${VERSION}
  git push origin v${VERSION} && echo "Created tag v${VERSION}"
else
  echo "Version not bumped. Skipping tag creation."
fi
