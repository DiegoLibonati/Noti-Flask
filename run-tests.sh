#!/usr/bin/env bash

# ─── CONFIG ──────────────────────────────────────────────────────────────────
NAMES=("Backend" "Frontend")
DIRS=("." "src/static/ts")
COMMANDS=("python -m pytest" "npm test")
# ─────────────────────────────────────────────────────────────────────────────

ROOT="$(cd "$(dirname "$0")" && pwd)"

C_RESET="\033[0m"
C_BOLD="\033[1m"
C_RED="\033[31m"
C_GREEN="\033[32m"
C_YELLOW="\033[33m"
C_CYAN="\033[36m"
C_MAGENTA="\033[35m"

PKG_COLORS=("$C_CYAN" "$C_YELLOW" "$C_MAGENTA" "$C_GREEN")

TMPDIR_BASE="$(mktemp -d)"
PIDS=()
EXIT_CODES=()

printf "\n${C_BOLD}%s${C_RESET}\n" "$(printf '═%.0s' {1..64})"
printf "${C_BOLD}Running tests for %d suite(s) in parallel${C_RESET}\n" "${#NAMES[@]}"
printf "${C_BOLD}%s${C_RESET}\n\n" "$(printf '═%.0s' {1..64})"

for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"
  dir="${DIRS[$i]}"
  cmd="${COMMANDS[$i]}"
  color="${PKG_COLORS[$((i % ${#PKG_COLORS[@]}))]}"
  outfile="$TMPDIR_BASE/$i.out"

  printf "${color}${C_BOLD}[%s]${C_RESET} Starting... (%s)\n" "$name" "$cmd"

  (
    cd "$ROOT/$dir" || exit 1
    eval "$cmd" > "$outfile" 2>&1
    echo $? > "$TMPDIR_BASE/$i.exit"
  ) &

  PIDS+=($!)
done

START_TIME=$SECONDS

for i in "${!PIDS[@]}"; do
  wait "${PIDS[$i]}"
done

ELAPSED=$((SECONDS - START_TIME))

RESULTS=()

for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"
  color="${PKG_COLORS[$((i % ${#PKG_COLORS[@]}))]}"
  outfile="$TMPDIR_BASE/$i.out"
  exitfile="$TMPDIR_BASE/$i.exit"
  code=$(cat "$exitfile" 2>/dev/null || echo 1)
  EXIT_CODES+=("$code")

  if [ "$code" -eq 0 ]; then
    status="${C_GREEN}${C_BOLD}PASSED${C_RESET}"
    RESULTS+=("pass")
  else
    status="${C_RED}${C_BOLD}FAILED${C_RESET}"
    RESULTS+=("fail")
  fi

  line=$(printf "${color}%s${C_RESET}" "$(printf '─%.0s' {1..64})")
  printf "\n%b\n" "$line"
  printf "${color}${C_BOLD}[%s]${C_RESET}  %b\n" "$name" "$status"
  printf "%b\n" "$line"
  cat "$outfile"
  printf "%b\n\n" "$line"
done

rm -rf "$TMPDIR_BASE"

printf "${C_BOLD}%s${C_RESET}\n" "$(printf '═%.0s' {1..64})"
printf "${C_BOLD}SUMMARY${C_RESET}  (%ds)\n" "$ELAPSED"
printf "${C_BOLD}%s${C_RESET}\n" "$(printf '═%.0s' {1..64})"

ALL_PASSED=true
for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"
  if [ "${RESULTS[$i]}" = "pass" ]; then
    printf "  ${C_GREEN}✓${C_RESET}  %s\n" "$name"
  else
    printf "  ${C_RED}✗${C_RESET}  %s\n" "$name"
    ALL_PASSED=false
  fi
done

if $ALL_PASSED; then
  printf "\n${C_GREEN}${C_BOLD}All tests passed!${C_RESET}\n\n"
  exit 0
else
  printf "\n${C_RED}${C_BOLD}Some tests failed.${C_RESET}\n\n"
  exit 1
fi