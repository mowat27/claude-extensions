#!/bin/bash

input=$(cat)

# Extract model name
MODEL=$(echo "$input" | jq -r '.model.display_name')

# Calculate context window usage percentage
CONTEXT_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size')
CURRENT_TOKENS=$(echo "$input" | jq '[.context_window.current_usage.input_tokens, .context_window.current_usage.cache_creation_input_tokens, .context_window.current_usage.cache_read_input_tokens] | add')
PERCENT_USED=$((CURRENT_TOKENS * 100 / CONTEXT_SIZE))

# Extract directory
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
DIR_NAME="${DIR##*/}"

# Get git status
STAGED=0
UNSTAGED=0
UNTRACKED=0

if git rev-parse --git-dir > /dev/null 2>&1; then
    # Count staged files
    STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')

    # Count unstaged files
    UNSTAGED=$(git diff --name-only 2>/dev/null | wc -l | tr -d ' ')

    # Count untracked files
    UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
fi

# Color codes
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
LIGHT_MAGENTA='\033[0;95m'
ORANGE='\033[0;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Color code the percent based on usage
if [ "$PERCENT_USED" -lt 40 ]; then
    PERCENT_COLORED="${GREEN}${PERCENT_USED}%${RESET}"
elif [ "$PERCENT_USED" -le 50 ]; then
    PERCENT_COLORED="${ORANGE}${PERCENT_USED}%${RESET}"
else
    PERCENT_COLORED="${RED}${PERCENT_USED}%${RESET}"
fi

# Color code the numbers based on values
STAGED_COLORED="${GREEN}${STAGED}${RESET}"
UNSTAGED_COLORED="${YELLOW}${UNSTAGED}${RESET}"
UNTRACKED_COLORED="${RED}${UNTRACKED}${RESET}"
DIR_COLORED="${CYAN}${DIR_NAME}${RESET}"
MODEL_COLORED="${YELLOW}${MODEL}${RESET}"

# Get git branch if in a repo
GIT_INFO=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    if [ -n "$BRANCH" ]; then
        BRANCH_COLORED="${LIGHT_MAGENTA}${BRANCH}${RESET}"
        GIT_INFO=" | $BRANCH_COLORED (S: $STAGED_COLORED, U: $UNSTAGED_COLORED, A: $UNTRACKED_COLORED)"
    fi
fi

echo -e "$MODEL_COLORED | $PERCENT_COLORED | $DIR_COLORED$GIT_INFO"
