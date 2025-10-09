#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"
SOURCE_DIR="${DOCS_DIR}/source"
API_DIR="${SOURCE_DIR}/api"
BUILD_DIR="${DOCS_DIR}/_build/html"

mkdir -p "${API_DIR}"
rm -rf "${API_DIR:?}/"*

poetry run sphinx-apidoc \
  --force \
  --output-dir "${API_DIR}" \
  --module-first \
  "${ROOT_DIR}/chat2query"

poetry run sphinx-build \
  -b html \
  "${SOURCE_DIR}" \
  "${BUILD_DIR}"

echo "Documentation generated at ${BUILD_DIR}"
