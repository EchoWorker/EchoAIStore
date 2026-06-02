#!/bin/sh
# EchoCode installer — downloads the latest release binary for your platform.
# Usage: curl -fsSL https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoCode/install.sh | sh
set -e

REPO="EchoWorker/EchoAIStore"
INSTALL_DIR="${ECHOCODE_INSTALL_DIR:-$HOME/.echoai/bin}"

# Detect platform
OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
  Darwin) os_name="darwin" ;;
  Linux)  os_name="linux" ;;
  *)      echo "Unsupported OS: $OS"; exit 1 ;;
esac

case "$ARCH" in
  x86_64|amd64) arch_name="x64" ;;
  arm64|aarch64) arch_name="arm64" ;;
  *)             echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

ARCHIVE="echocode-${os_name}-${arch_name}.tar.gz"

# Get latest EchoCode release (filter by echocode- tag prefix)
echo "Fetching latest release..."
VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases" | \
  grep '"tag_name"' | grep '"echocode-' | head -1 | cut -d'"' -f4)
if [ -z "$VERSION" ]; then
  echo "Error: Could not find any EchoCode release"
  exit 1
fi

URL="https://github.com/$REPO/releases/download/$VERSION/$ARCHIVE"
echo "Downloading EchoCode $VERSION ($os_name/$arch_name)..."

# Download and extract
TMPDIR=$(mktemp -d)
curl -fsSL "$URL" -o "$TMPDIR/$ARCHIVE"
tar xzf "$TMPDIR/$ARCHIVE" -C "$TMPDIR"

# Install
mkdir -p "$INSTALL_DIR"
mv "$TMPDIR/echo-code" "$INSTALL_DIR/echo-code"
chmod +x "$INSTALL_DIR/echo-code"
rm -rf "$TMPDIR"

echo ""
echo "✅ EchoCode $VERSION installed to $INSTALL_DIR/echo-code"

# Check PATH
case ":$PATH:" in
  *":$INSTALL_DIR:"*) ;;
  *)
    echo ""
    echo "⚠️  $INSTALL_DIR is not in your PATH. Add it:"
    echo "   export PATH=\"$INSTALL_DIR:\$PATH\""
    echo ""
    echo "Or add to your shell profile (~/.bashrc, ~/.zshrc, etc.)"
    ;;
esac

echo ""

# Copy example config if no config exists
CONFIG_DIR="$HOME/.echoai"
mkdir -p "$CONFIG_DIR"

if [ ! -f "$CONFIG_DIR/echocode.toml" ]; then
  EXAMPLE_URL="https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoCode/echocode.example.toml"
  if curl -fsSL "$EXAMPLE_URL" -o "$CONFIG_DIR/echocode.toml" 2>/dev/null; then
    echo "📝 Created $CONFIG_DIR/echocode.toml from example."
  else
    echo "⚠️  Could not download example config. Create $CONFIG_DIR/echocode.toml manually."
  fi
fi

echo ""
echo "Get started:"
echo "  1. Edit ~/.echoai/echocode.toml — set your API key and model"
echo "  2. echo-code                     # Start interactive session"
