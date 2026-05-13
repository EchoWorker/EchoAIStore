#!/bin/sh
# EchoAI installer — downloads the latest release binary for your platform.
# Usage: curl -fsSL https://raw.githubusercontent.com/EchoWorker/EchoAI/main/scripts/install.sh | sh
set -e

REPO="EchoWorker/EchoAIStore"
INSTALL_DIR="${ECHOAI_INSTALL_DIR:-$HOME/.local/bin}"

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

# Get latest version
echo "Fetching latest release..."
VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name"' | cut -d'"' -f4)
if [ -z "$VERSION" ]; then
  echo "Error: Could not determine latest version"
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
echo "Get started:"
echo "  echoai gateway    # Start the server"
echo "  echoai agent      # Interactive REPL"
