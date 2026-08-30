#!/usr/bin/env bash
# Usage: ./new_problem.sh <number> <slug> <topic> <difficulty>
# Example: ./new_problem.sh 1 two-sum arrays Easy

set -e

NUMBER=$1
SLUG=$2
TOPIC=$3
DIFFICULTY=$4

if [ -z "$NUMBER" ] || [ -z "$SLUG" ] || [ -z "$TOPIC" ] || [ -z "$DIFFICULTY" ]; then
  echo "Usage: ./new_problem.sh <number> <slug> <topic> <difficulty>"
  echo "Example: ./new_problem.sh 1 two-sum arrays Easy"
  exit 1
fi

PADDED=$(printf "%04d" "$NUMBER")
DIR="${TOPIC}/${PADDED}-${SLUG}"
TITLE=$(echo "$SLUG" | sed -E 's/(^|-)([a-z])/\1\U\2/g; s/-/ /g')
URL="https://leetcode.com/problems/${SLUG}/"

mkdir -p "$DIR"

sed -e "s/{NUMBER}/${NUMBER}/g" \
    -e "s/{TITLE}/${TITLE}/g" \
    -e "s|{LEETCODE_URL}|${URL}|g" \
    -e "s/{DIFFICULTY}/${DIFFICULTY}/g" \
    -e "s/{TOPIC}/${TOPIC}/g" \
    "_template/README.md" > "${DIR}/README.md"

sed -e "s/{NUMBER}/${NUMBER}/g" \
    -e "s/{TITLE}/${TITLE}/g" \
    -e "s|{LEETCODE_URL}|${URL}|g" \
    "_template/solution.py" > "${DIR}/solution.py"

echo "Created ${DIR}/"
echo ""
echo "Add this row to the index table in README.md:"
echo "| ${NUMBER} | ${TITLE} | ${DIFFICULTY} | ${TOPIC} | [link](${DIR}) |"
