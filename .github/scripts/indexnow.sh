#!/usr/bin/env bash
# IndexNow 알림: 새로 올리거나 고친 페이지를 빙·네이버 등 IndexNow 검색엔진에 바로 알립니다.
# IndexNow에 제출한 주소는 참여 검색엔진(빙, 네이버, Yandex, Seznam, Yep)끼리 자동으로 공유됩니다.
#
# 환경 변수
#   SITE_HOST      사이트 주소 (예: galclinic.co.kr)
#   INDEXNOW_KEY   IndexNow 키 (루트의 <키>.txt 파일 내용과 같아야 함)
#   MODE           auto = 이번 push에서 바뀐 페이지만, all = 사이트맵 전체
#   REPO, BEFORE, AFTER  GitHub 저장소 이름과 push 전후 커밋 (auto 모드에서 사용)
#   SITEMAP        사이트맵 경로 (기본 sitemap.xml)
#   WAIT_TIMEOUT   배포 완료를 기다리는 최대 시간(초, 기본 600)
#   DRY_RUN=1      실제 제출 없이 목록만 출력 (테스트용)
#   CHANGES_FILE   (테스트용) GitHub API 대신 "상태<TAB>파일<TAB>이전파일" 목록 파일 사용

set -euo pipefail

SITE_HOST="${SITE_HOST:?SITE_HOST가 필요합니다}"
INDEXNOW_KEY="${INDEXNOW_KEY:?INDEXNOW_KEY가 필요합니다}"
MODE="${MODE:-auto}"
SITEMAP="${SITEMAP:-sitemap.xml}"
WAIT_TIMEOUT="${WAIT_TIMEOUT:-600}"
DRY_RUN="${DRY_RUN:-0}"
ENDPOINT="https://api.indexnow.org/indexnow"
KEY_FILE="${INDEXNOW_KEY}.txt"
KEY_URL="https://${SITE_HOST}/${KEY_FILE}"
CACHE_BUST="${AFTER:-$(date +%s)}"

# 이 파일들이 바뀐 push(= 설정을 처음 넣거나 고친 때)에는 사이트맵 전체를 한 번 제출합니다.
SETUP_FILES=(".github/workflows/indexnow.yml" ".github/scripts/indexnow.sh" "$KEY_FILE")

log() { printf '%s\n' "$*"; }
summary() { [ -n "${GITHUB_STEP_SUMMARY:-}" ] && printf '%s\n' "$*" >> "$GITHUB_STEP_SUMMARY" || true; }

# 저장소 안의 파일 경로 → 실제 주소
path_to_url() {
  local p="$1"
  case "$p" in
    index.html)   printf 'https://%s/\n' "$SITE_HOST" ;;
    */index.html) printf 'https://%s/%s\n' "$SITE_HOST" "${p%index.html}" ;;
    *.html)       printf 'https://%s/%s\n' "$SITE_HOST" "$p" ;;
    *)            return 1 ;;
  esac
}

# 사이트맵에 있는 주소 목록
mapfile -t SITEMAP_URLS < <(grep -o '<loc>[^<]*</loc>' "$SITEMAP" | sed -e 's#<loc>##' -e 's#</loc>##' | sed 's/[[:space:]]//g')
declare -A IN_SITEMAP=()
for u in "${SITEMAP_URLS[@]}"; do IN_SITEMAP["$u"]=1; done
log "사이트맵 주소: ${#SITEMAP_URLS[@]}개"

declare -A SEEN=()
URLS=()      # 제출할 주소
NEW_URLS=()  # 새로 생긴 주소 (배포 완료 확인용)

add_url() {
  local u="$1"
  [ -z "$u" ] && return 0
  [ -n "${SEEN[$u]:-}" ] && return 0
  SEEN["$u"]=1
  URLS+=("$u")
}

# 바뀐 파일 목록 가져오기: "상태<TAB>파일<TAB>이전파일"
list_changes() {
  if [ -n "${CHANGES_FILE:-}" ]; then
    cat "$CHANGES_FILE"
    return
  fi
  local jq_files='.files[] | [.status, .filename, (.previous_filename // "")] | @tsv'
  if [ -z "${BEFORE:-}" ] || [[ "$BEFORE" =~ ^0+$ ]]; then
    # 새 브랜치 등 이전 커밋이 없을 때는 마지막 커밋만 봅니다.
    gh api "repos/${REPO}/commits/${AFTER}" --jq "$jq_files"
  else
    gh api --paginate "repos/${REPO}/compare/${BEFORE}...${AFTER}?per_page=100" --jq "$jq_files"
  fi
}

if [ "$MODE" != "all" ]; then
  CHANGES="$(list_changes)"
  while IFS=$'\t' read -r status file prev; do
    [ -z "${file:-}" ] && continue
    for s in "${SETUP_FILES[@]}"; do
      if [ "$file" = "$s" ]; then MODE="all"; fi
    done
  done <<< "$CHANGES"
fi

if [ "$MODE" = "all" ]; then
  log "모드: 사이트맵 전체 제출"
  for u in "${SITEMAP_URLS[@]}"; do add_url "$u"; done
else
  log "모드: 이번에 바뀐 페이지만 제출"
  while IFS=$'\t' read -r status file prev; do
    [ -z "${file:-}" ] && continue
    case "$status" in
      removed)
        # 지운 페이지도 알려서 검색 결과에서 빨리 빠지게 합니다.
        [ "$file" = "404.html" ] && continue
        if u="$(path_to_url "$file")"; then add_url "$u"; fi
        ;;
      added|modified|changed|copied|renamed)
        if [ "$status" = "renamed" ] && [ -n "${prev:-}" ] && [ "$prev" != "404.html" ]; then
          if u="$(path_to_url "$prev")"; then add_url "$u"; fi
        fi
        if u="$(path_to_url "$file")"; then
          # 사이트맵에 있는 페이지만 (404, 개인정보처리방침 등 제외)
          if [ -n "${IN_SITEMAP[$u]:-}" ]; then
            add_url "$u"
            case "$status" in added|copied|renamed) NEW_URLS+=("$u") ;; esac
          fi
        fi
        ;;
    esac
  done <<< "$CHANGES"
fi

if [ "${#URLS[@]}" -eq 0 ]; then
  log "알릴 페이지가 없습니다."
  summary "### IndexNow: 알릴 페이지 없음"
  exit 0
fi

if [ "${#URLS[@]}" -gt 10000 ]; then
  log "주의: 한 번에 10,000개까지만 제출할 수 있어 앞의 10,000개만 보냅니다."
  URLS=("${URLS[@]:0:10000}")
fi

log "제출할 주소 ${#URLS[@]}개:"
printf '  %s\n' "${URLS[@]}"

if [ "$DRY_RUN" = "1" ]; then
  log "(DRY_RUN: 실제 제출은 하지 않았습니다)"
  exit 0
fi

# GitHub Pages 배포가 끝날 때까지 기다리기: 키 파일과 새 페이지가 실제로 열리는지 확인
deadline=$(( $(date +%s) + WAIT_TIMEOUT ))
log "키 파일 확인: $KEY_URL"
until [ "$(curl -fsS "${KEY_URL}?v=${CACHE_BUST}" 2>/dev/null | tr -d '[:space:]')" = "$INDEXNOW_KEY" ]; do
  if [ "$(date +%s)" -ge "$deadline" ]; then
    log "오류: 키 파일이 사이트에서 열리지 않습니다. 루트에 ${KEY_FILE} 파일이 있는지 확인하세요."
    summary "### IndexNow: 실패 — 키 파일(${KEY_FILE})이 사이트에서 열리지 않음"
    exit 1
  fi
  sleep 15
done
log "키 파일 확인됨"

for u in "${NEW_URLS[@]}"; do
  log "새 페이지 배포 확인: $u"
  until [ "$(curl -s -o /dev/null -w '%{http_code}' "${u}?v=${CACHE_BUST}")" = "200" ]; do
    if [ "$(date +%s)" -ge "$deadline" ]; then
      log "주의: 배포 확인 시간이 지나 그대로 제출합니다: $u"
      break
    fi
    sleep 15
  done
done

payload="$(mktemp)"
response="$(mktemp)"
printf '%s\n' "${URLS[@]}" | jq -R . | jq -s \
  --arg host "$SITE_HOST" --arg key "$INDEXNOW_KEY" --arg loc "$KEY_URL" \
  '{host: $host, key: $key, keyLocation: $loc, urlList: .}' > "$payload"

code="000"
for attempt in 1 2 3; do
  code="$(curl -sS -o "$response" -w '%{http_code}' -X POST "$ENDPOINT" \
    -H 'Content-Type: application/json; charset=utf-8' \
    --data-binary @"$payload" || true)"
  case "$code" in
    200|202) break ;;
    429|5*|000) log "응답 ${code}, 30초 후 다시 시도합니다 (${attempt}/3)"; sleep 30 ;;
    *) break ;;
  esac
done

case "$code" in
  200) result="성공 (200: 접수됨)" ;;
  202) result="성공 (202: 접수됨, 키 확인 대기)" ;;
  400) result="실패 (400: 요청 형식 오류)" ;;
  403) result="실패 (403: 키가 맞지 않음 — 키 파일 내용 확인 필요)" ;;
  422) result="실패 (422: 주소가 사이트와 맞지 않거나 키 형식 오류)" ;;
  429) result="실패 (429: 너무 자주 제출함)" ;;
  *)   result="실패 (응답 ${code})" ;;
esac

log "IndexNow 결과: $result"
[ -s "$response" ] && { log "응답 내용:"; cat "$response"; echo; }

summary "### IndexNow: $result"
summary ""
summary "제출한 주소 ${#URLS[@]}개 (빙·네이버 등 참여 검색엔진에 공유됨)"
summary ""
for u in "${URLS[@]}"; do summary "- $u"; done

case "$code" in 200|202) exit 0 ;; *) exit 1 ;; esac
