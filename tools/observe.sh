#!/usr/bin/env bash
set -euo pipefail

run_id="${1:-${RUN_ID:-}}"
if [[ -z "$run_id" ]]; then
  echo "ERROR: RUN_ID is required. Usage: make awareness RUN_ID=<RUN_ID> or tools/observe.sh <RUN_ID>" >&2
  exit 2
fi

repo_root="${AWARENESS_REPO_ROOT:-.}"
reports_dir="${AWARENESS_REPORTS_DIR:-${repo_root}/reports}"
state_file="${AWARENESS_STATE_FILE:-${repo_root}/TASKS/STATE.md}"
queue_file="${AWARENESS_QUEUE_FILE:-${repo_root}/TASKS/QUEUE.md}"
mistakes_dir="${AWARENESS_MISTAKES_DIR:-${repo_root}/MISTAKES}"
out_dir="${AWARENESS_OUT_DIR:-${reports_dir}/${run_id}}"
out_file="${out_dir}/awareness.md"

mkdir -p "$out_dir"

tmp_runs="$(mktemp)"
tmp_week="$(mktemp)"
tmp_mistakes="$(mktemp)"
tmp_process_mistakes="$(mktemp)"
tmp_risks="$(mktemp)"
tmp_suggest="$(mktemp)"
cleanup() {
  rm -f "$tmp_runs" "$tmp_week" "$tmp_mistakes" "$tmp_process_mistakes" "$tmp_risks" "$tmp_suggest"
}
trap cleanup EXIT

# Collect runs by scanning decision/summary files.
if [[ -d "$reports_dir" ]]; then
  find "$reports_dir" -maxdepth 2 -type f \( -name "decision.md" -o -name "summary.md" \) \
    | awk -F/ '
        {
          rid="";
          for (i=1; i<=NF; i++) {
            if ($i ~ /^run-/) rid=$i;
          }
          if (rid != "") print rid;
        }
      ' \
    | sort -u > "$tmp_runs"
fi

current_week="$(date +%G-%V)"
if [[ -s "$tmp_runs" ]]; then
  while IFS= read -r rid; do
    d="$(echo "$rid" | awk -F- '{print $2 "-" $3 "-" $4}')"
    if date -d "$d" +%G-%V >/dev/null 2>&1; then
      rid_week="$(date -d "$d" +%G-%V)"
      if [[ "$rid_week" == "$current_week" ]]; then
        echo "$rid" >> "$tmp_week"
      fi
    fi
  done < "$tmp_runs"
fi

# Optional mistakes patterns (simple frequency on "symptom:" lines).
if [[ -d "$mistakes_dir" ]]; then
  find "$mistakes_dir" -maxdepth 1 -type f -name "*.md" \
    | while IFS= read -r f; do
        awk -F':' 'tolower($1) ~ /symptom/ {sub(/^[[:space:]]+/, "", $2); if ($2 != "") print $2}' "$f"
      done \
    | awk '{count[$0]++} END {for (k in count) printf "%d\t%s\n", count[k], k}' \
    | sort -nr > "$tmp_mistakes"
fi

# Process mistakes from ship/runtime logs (reports/*/mistake_log.jsonl).
if [[ -d "$reports_dir" ]]; then
  find "$reports_dir" -maxdepth 2 -type f -name "mistake_log.jsonl" -exec cat {} + 2>/dev/null \
    | awk '
        {
          cat = ""; step = ""
          if (match($0, /"category":"[^"]+"/)) {
            cat = substr($0, RSTART + 12, RLENGTH - 13)
          }
          if (match($0, /"step":"[^"]+"/)) {
            step = substr($0, RSTART + 8, RLENGTH - 9)
          }
          if (cat != "" && step != "") {
            key = cat " / " step
            count[key]++
          }
        }
        END {
          for (k in count) {
            printf "%d\t%s\n", count[k], k
          }
        }
      ' \
    | sort -nr > "$tmp_process_mistakes"
fi

# Current risk from STATE.
if [[ -f "$state_file" ]]; then
  awk '
    BEGIN { in_risk = 0; emitted = 0 }
    /^## / {
      if (in_risk == 1) exit
      if (tolower($0) ~ /risk/) { in_risk = 1; next }
    }
    in_risk == 1 {
      if ($0 ~ /^[[:space:]]*$/) next
      print "- " $0
      emitted++
      if (emitted >= 5) exit
    }
  ' "$state_file" > "$tmp_risks"
fi

# Suggestions from the top unfinished queue items.
if [[ -f "$queue_file" ]]; then
  awk '
    BEGIN { c = 0 }
    /^- \[ \] TODO Title:/ {
      title = $0
      sub(/^- \[ \] TODO Title:[[:space:]]*/, "", title)
      print "- TASK: " title
      c++
      if (c >= 5) exit
    }
  ' "$queue_file" > "$tmp_suggest"
fi

{
  echo "# Awareness Digest"
  echo
  echo "RUN_ID: \`$run_id\`"
  echo "Generated At: $(date -Iseconds)"
  echo
  echo "## 本周 shipped runs"
  if [[ -s "$tmp_week" ]]; then
    while IFS= read -r rid; do
      echo "- $rid"
    done < "$tmp_week"
  else
    echo "- 无（本周未检出 shipped runs）"
  fi
  echo
  echo "## 重复失败模式"
  if [[ -s "$tmp_mistakes" ]]; then
    head -n 5 "$tmp_mistakes" | while IFS=$'\t' read -r cnt msg; do
      echo "- ${msg} (x${cnt})"
    done
  else
    echo "- 无（未检出 MISTAKES 模式）"
  fi
  echo
  echo "## 过程错题（执行/思考）"
  if [[ -s "$tmp_process_mistakes" ]]; then
    head -n 5 "$tmp_process_mistakes" | while IFS=$'\t' read -r cnt item; do
      echo "- ${item} (x${cnt})"
    done
  else
    echo "- 无（未检出 process mistake logs）"
  fi
  echo
  echo "## 当前风险"
  if [[ -s "$tmp_risks" ]]; then
    cat "$tmp_risks"
  else
    echo "- 未在 TASKS/STATE.md 中检出风险段落"
  fi
  echo
  echo "## 下一枪建议"
  if [[ -s "$tmp_suggest" ]]; then
    head -n 5 "$tmp_suggest"
  else
    echo "- TASK: 从 QUEUE 增加一个可执行 TODO 条目并补齐任务证据"
  fi
} > "$out_file"

echo "AWARENESS_FILE: $out_file"
