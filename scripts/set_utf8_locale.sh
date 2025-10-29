#!/usr/bin/env bash
set -euo pipefail

# Helper to ensure LANG and LC_ALL are set to UTF-8 in common shell startup files.
# It will back up any files it modifies and avoid duplicating lines.

# POSIX-style shells (bash/zsh)
FILES_SH=("$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.profile" "$HOME/.bash_profile" "$HOME/.bashrc")
EXPORT_LINE1='export LANG=en_US.UTF-8'
EXPORT_LINE2='export LC_ALL=en_US.UTF-8'

for f in "${FILES_SH[@]}"; do
  # only consider a small set of likely files; skip empty entries
  [ -z "$f" ] && continue
  if [ -f "$f" ]; then
    echo "Processing $f"
    cp -a "$f" "$f.bak-utf8-$(date +%Y%m%d%H%M%S)"
    # Append the exports if they're not present
    if ! grep -q "^export LANG=" "$f"; then
      echo "$EXPORT_LINE1" >> "$f"
      echo "Added LANG to $f"
    else
      echo "LANG already set in $f"
    fi
    if ! grep -q "^export LC_ALL=" "$f"; then
      echo "$EXPORT_LINE2" >> "$f"
      echo "Added LC_ALL to $f"
    else
      echo "LC_ALL already set in $f"
    fi
  else
    # don't create every possible file; create only the primary ones
    case "$f" in
      "$HOME/.zprofile"|"$HOME/.zshrc")
        echo "$f does not exist ? creating with exports"
        cat > "$f" <<'EOF'
#!/usr/bin/env zsh
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
EOF
        chmod 644 "$f"
        echo "Created $f with LANG/LC_ALL exports"
        ;;
      *)
        # skip creating other shell files to avoid touching user's bash/profile too eagerly
        ;;
    esac
  fi
done

# csh/tcsh-style shells
FILES_CSH=("$HOME/.tcshrc" "$HOME/.cshrc")
SETENV_LINE1='setenv LANG en_US.UTF-8'
SETENV_LINE2='setenv LC_ALL en_US.UTF-8'

for f in "${FILES_CSH[@]}"; do
  [ -z "$f" ] && continue
  if [ -f "$f" ]; then
    echo "Processing $f"
    cp -a "$f" "$f.bak-utf8-$(date +%Y%m%d%H%M%S)"
    if ! grep -q "^setenv LANG" "$f"; then
      echo "$SETENV_LINE1" >> "$f"
      echo "Added LANG to $f (tcsh/csh style)"
    else
      echo "LANG already set in $f"
    fi
    if ! grep -q "^setenv LC_ALL" "$f"; then
      echo "$SETENV_LINE2" >> "$f"
      echo "Added LC_ALL to $f (tcsh/csh style)"
    else
      echo "LC_ALL already set in $f"
    fi
  else
    echo "$f does not exist ? creating with setenv lines"
    cat > "$f" <<'EOF'
# ~/.tcshrc (created by set_utf8_locale.sh)
setenv LANG en_US.UTF-8
setenv LC_ALL en_US.UTF-8
EOF
    chmod 644 "$f"
    echo "Created $f with setenv LANG/LC_ALL"
  fi
done

echo
echo "Done. Please restart VS Code (or open a new integrated terminal) to pick up the changes."
