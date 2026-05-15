#!/bin/sh
# EchoAI installer — downloads the latest release binary for your platform.
# Usage: curl -fsSL https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.sh | sh
set -e

REPO="EchoWorker/EchoAIStore"
INSTALL_DIR="${ECHOAI_INSTALL_DIR:-$HOME/.echoai/bin}"

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

ARCHIVE="echoai-${os_name}-${arch_name}.tar.gz"

# Get latest EchoAI release (filter by echoai- tag prefix)
echo "Fetching latest release..."
VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases" | \
  grep '"tag_name"' | grep '"echoai-' | head -1 | cut -d'"' -f4)
if [ -z "$VERSION" ]; then
  echo "Error: Could not find any EchoAI release"
  exit 1
fi

URL="https://github.com/$REPO/releases/download/$VERSION/$ARCHIVE"
echo "Downloading EchoAI $VERSION ($os_name/$arch_name)..."

# Download and extract
TMPDIR=$(mktemp -d)
curl -fsSL "$URL" -o "$TMPDIR/$ARCHIVE"
tar xzf "$TMPDIR/$ARCHIVE" -C "$TMPDIR"

# Install
mkdir -p "$INSTALL_DIR"
mv "$TMPDIR/echoai" "$INSTALL_DIR/echoai"
chmod +x "$INSTALL_DIR/echoai"
rm -rf "$TMPDIR"

echo ""
echo "✅ EchoAI $VERSION installed to $INSTALL_DIR/echoai"

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
  EXAMPLE_URL="https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/echocode.example.toml"
  if curl -fsSL "$EXAMPLE_URL" -o "$CONFIG_DIR/echocode.toml" 2>/dev/null; then
    echo "📝 Created $CONFIG_DIR/echocode.toml from example."
  else
    echo "⚠️  Could not download example config. Create $CONFIG_DIR/echocode.toml manually."
  fi
fi

echo ""
echo "Get started:"
echo "  1. Edit ~/.echoai/echocode.toml — set your API key and model"
echo "  2. echoai gateway    # Start the server"
echo "  3. echoai agent      # Interactive REPL"
