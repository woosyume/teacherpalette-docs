# TeacherPalette Resources — Production SEO / Localization 개선 보고

2026-10-06 · 기존 production 구조를 확인한 뒤 로컬 수정·검증 완료.
이번 변경은 아직 production에 배포하지 않았습니다.

## A. SEO Consolidation

| 항목 | 결과 |
|---|---|
| Primary page | `/en/resources/annotate-screen-mac/` |
| Redirect source | `/en/draw-on-screen-mac/` |
| Redirect destination | `/en/resources/annotate-screen-mac/` — 최종 목적지를 직접 지정 |
| 실제 production HTTP status | 조사 시 **200**, `Server: GitHub.com`. 배포된 기존 본문이 반환됨 |
| 로컬 수정본 HTTP status | **200** — 정적 HTML fallback이며 HTTP 301이 아님 |
| 로컬 브라우저 이동 | `meta refresh` 0초로 새 대표 페이지에 바로 도착 |
| 기존 페이지 canonical | 이전 self-canonical에서 새 대표 페이지로 변경 |
| 새 대표 페이지 canonical | `https://teacherpalette.com/en/resources/annotate-screen-mac/` 그대로 유지 |

### HTTP 301 제약

production 응답은 GitHub Pages이며 저장소에는 서버·엣지 리디렉션 설정이 없습니다.
[GitHub Pages는 정적 HTML 호스팅](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)이므로
이 저장소의 HTML 수정만으로 HTTP `Location` 헤더와 301 상태를 설정할 수 없습니다.
실제 HTTP 301을 적용하려면 이를 지원하는 호스팅 또는 엣지 계층이 필요합니다.
이번 요청의 불필요한 인프라 추가 금지 원칙에 따라 호스팅·DNS를 바꾸지 않았습니다.

대신 기존 본문·구조화 데이터·alternate 선언을 제거하고, 즉시 이동과 새 목적지의
canonical, 직접 이동 링크만 남긴 작은 HTML 페이지로 교체했습니다.
[Google은 서버 이동이 불가능할 때 0초 meta refresh를 영구 이동 신호로 해석한다고 안내합니다.](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
그러나 **이 방식이 HTTP 301이라는 뜻은 아닙니다.** 해당 HTTP 요구사항은 현재
호스팅의 제약으로 충족하지 못했으며, production 이동은 배포 후 추가 확인해야 합니다.

### 검색 신호와 내부 링크

- sitemap에서 기존 영어 URL을 제외했습니다. 새 대표 URL만 포함합니다.
- 홈의 화면 주석 링크, FAQ의 초기 HTML 카드와 언어별 JavaScript 경로,
  기존 영어 커서·화이트보드·PDF 글의 관련 링크, 기존 `/guides/` 글을 직접 수정했습니다.
- 8개 기존 현지어 화면 글의 EN·x-default alternate와 영어 전환 링크를 새 대표 URL로 바꿨습니다.
- 새 대표 페이지에 기존 8개 현지어 화면 글을 실제 alternate로 연결해 상호 관계를 유지합니다.
- Resources 인덱스의 중복된 기존 영어 화면 카드와 해당 legacy route 등록을 제거했습니다.
- 서비스 HTML·JavaScript·콘텐츠 JSON·sitemap에 이전 URL을 가리키는 링크는 없습니다.
- 다른 언어의 화면 글은 본문·title·description·canonical을 유지했습니다.
- 새 영어 본문은 기존 H1·title·description을 유지하고, 기존 페이지에만 있던
  툴바·개인 HUD의 화면 공유 동작 설명 한 문단만 통합했습니다.

SEO 신호를 정리한 결과이며 실제 Google의 canonical 선택과 검색 경쟁 해소는
배포 후 Search Console에서 확인할 수 있습니다.

## B. Resources Navigation Localization

실제 홈의 지원 언어 배열은 EN·JA·KO·ZH·FR·DE·ES·PT·IT, 총 9개입니다.

| Locale | Existing Help/Tips Label | Final Resources Label |
|---|---|---|
| EN | Help & Tips | Resources |
| JA | ヘルプ＆ヒント | **活用情報** |
| KO | 도움말 & 팁 | **활용 자료** |
| ZH | 帮助与技巧 | 资源（英语） |
| FR | Aide et astuces | Ressources (anglais) |
| DE | Hilfe & Tipps | Ressourcen (Englisch) |
| ES | Ayuda y consejos | Recursos (inglés) |
| PT | Ajuda e dicas | Recursos (inglês) |
| IT | Aiuto e consigli | Risorse (inglese) |

KO·JA에는 요청한 표현을 적용했습니다. 나머지 6개 언어는 기존 표현이 자료
공간의 의미를 가지며 Help/Tips 표현과 구별되어 유지했습니다. 영어로 제공되는
라이브러리라는 표시도 그대로 남겼습니다. 어느 언어에서도 Resources 메뉴를
Help·Tips·Manual·Support 또는 Guide로 이름 붙이지 않았습니다.

메뉴·푸터·홈 섹션 제목이 같은 문자열을 사용합니다. EN·JA·KO 이름은 locale
데이터를 단일 원본으로 읽도록 했습니다. JA·KO 인덱스 제목·목록 안내·상위
자료 공간의 링크 명칭도 맞췄습니다. 내부 category인 Guides/使い方ガイド/사용
가이드는 별도의 글 유형이므로 유지했습니다. 기존 `/resources/` URL은 변경하지 않았습니다.

## C. Presentify Alternative Localization

각 URL은 `https://teacherpalette.com` 기준입니다.

| Locale | URL | H1 | SEO Title | Canonical |
|---|---|---|---|---|
| EN | `/en/resources/presentify-alternative-mac/` | Looking for a Presentify Alternative for Mac? | Presentify Alternative for Mac \| TeacherPalette | https://teacherpalette.com/en/resources/presentify-alternative-mac/ |
| JA | `/ja/resources/presentify-alternative-mac/` | Presentifyの代替アプリをお探しですか？ | Presentifyの代替アプリをお探しの方へ \| TeacherPalette | https://teacherpalette.com/ja/resources/presentify-alternative-mac/ |
| KO | `/ko/resources/presentify-alternative-mac/` | Presentify 대체 앱을 찾고 계신가요? | Presentify 대체 앱: Mac 화면 필기와 발표 도구 \| TeacherPalette | https://teacherpalette.com/ko/resources/presentify-alternative-mac/ |

### JA 검색 의도와 현지화

`Presentifyの代替`, Macの画面に書き込む, 画面への注釈, 授業・プレゼン의
맥락을 자연스럽게 연결했습니다. 수업·연수에서 작은 설정을 보여주고, 질문을
화이트보드로 풀며, PDF 배포 자료와 주석을 함께 남기는 상황을 중심으로 썼습니다.
문장과 소제목, 비교표의 질문, 설명문을 일본어로 별도 작성했습니다.

### KO 검색 의도와 현지화

`Presentify 대체 앱`을 입구로 맥 화면 필기·화면 주석, 강사의 수업과 소프트웨어
데모, 개발자의 코드 설명으로 이어갑니다. 자신의 슬라이드·앱·PDF를 사용해
도구를 비교하는 방법과 임시 주석·저장할 설명을 구분하는 기준을 중심으로 썼습니다.
일본어와 영어의 문장 구조를 그대로 복사하지 않고 한국어로 별도 작성했습니다.

세 언어의 포지셔닝은 화면 주석 → Spotlight/Magnifier → Whiteboard → PDF의
설명 흐름으로 동일합니다. 기존 사이트에서 검증한 기능과 Kim의 강사·개발자
소개만 사용했습니다. 경쟁 제품의 가격·기능을 추측하거나 가짜 리뷰·평점을
추가하지 않았습니다. 검색량이나 키워드 수요를 실측했다는 주장은 하지 않습니다.

CTA는 기존 locale 문자열을 그대로 재사용합니다.

- EN: `Try TeacherPalette Free for 7 Days`
- JA: `TeacherPaletteを7日間無料で試す`
- KO: `TeacherPalette 7일 무료 체험`

링크 관리도 기존 방식 그대로, 홈 primary CTA의 공식 App Store URL을 읽습니다.
모든 CTA는 앱 ID `6783567350`을 가리킵니다. 다른 6개 언어의 비교 글은 생성하지 않았습니다.

## D. SEO Infrastructure

| 항목 | 처리 |
|---|---|
| Sitemap | 54개 → 55개. 이전 영어 URL 1개 제외, JA·KO 비교 글 2개 추가 |
| Canonical | 모든 새 현지어 페이지가 자기 URL을 지정. EN canonical 유지 |
| Hreflang | Presentify EN·JA·KO와 영어 x-default가 상호 연결됨 |
| 영어 화면 글 alternates | 새 대표 EN + 기존 현지어 화면 글 8개. 상호 링크 검증 |
| Structured data | 기존 Article·BreadcrumbList 구조 사용. 현지어 headline·description·URL·inLanguage 제공 |
| Open Graph / Twitter | locale별 title·description·URL과 기존 공식 소셜 이미지 재사용 |
| Index / Home cards | JA·KO 비교 글을 각 언어의 카드로 추가. 홈은 새 글과 기존 현지어 자료로 3개 카드 유지 |
| Related articles | 번역된 Resources 글이 있으면 우선 표시. 현재 JA·KO는 각 언어의 기존 화면·화이트보드 글을 연결 |
| Language navigation | 라이브러리 이동과 별도로 동일 비교 글의 EN·JA·KO 전환 링크 제공 |
| Robots / analytics | 기존 robots.txt·홈 스크립트·분석 관련 동작 보존 |

## E. Verification

- 기존 production 홈·EN 인덱스·EN 비교 글·새 대표 화면 글·JA 인덱스·KO 인덱스·sitemap의
  HTTP 200 응답과 저장소 파일 일치를 수정 전에 확인했습니다.
- `python3 scripts/build_resources.py`: 정적 production HTML 8개 생성 성공.
- `python3 scripts/build_resources.py --check`: 생성 결과 재현성 통과.
- `python3 scripts/verify_resources.py`: HTML 64개의 내부 링크·앵커·미디어 경로 검사 통과.
  기존 및 새 broken internal link 모두 0개.
- 로컬 HTTP 검사: 새 페이지 응답·HTML 일치, 이전 URL의 HTTP 200 fallback 확인.
- 이전 URL을 브라우저에서 열어 새 대표 페이지로 직접 이동하는 것을 확인했습니다.
  **HTTP 301 검사는 통과로 표시하지 않았습니다.**
- sitemap의 유효한 URL 55개, 지정한 이전 EN URL 외의 기존 URL 보존 확인.
- 기존 EN 기사 3개의 H1·meta·canonical 보존, 8개 기존 현지어 화면 글의 meta·canonical 보존 확인.
- 인덱스 3개, Presentify 기사 3개, 대표 화면 글을 1280·768·390px에서 확인했습니다.
- 홈 9개 언어를 1280·1024·768·390px에서 확인하고, 태블릿·모바일에서는 메뉴를
  실제로 펼쳐 확인했습니다. 메뉴 넘침 없음, 메뉴와 홈 제목 명칭 일치, 홈 카드 3개 유지.
- KO의 긴 제목은 단어 중간에서 잘리지 않도록 작은 줄바꿈 스타일을 추가했습니다.
- 비교표는 좁은 화면에서 자체 영역 안에서 가로 스크롤합니다.
- 새 영상·이미지·의존성을 추가하지 않았습니다. 기존 controls·playsinline·preload=none 유지.

이 프로젝트는 프레임워크 빌드가 없는 정적 사이트입니다. 생성한 HTML이 기존
호스팅에 올릴 산출물이며, 별도 CMS·라우팅 인프라를 추가하지 않았습니다.
production 배포와 배포 후 HTTP/검색 색인 검증은 이번 로컬 수정 이후의 단계입니다.

### 변경 위치

- `resources/content/articles.json`: JA·KO 비교 글 등록과 화면 글의 기존 locale alternates.
- `resources/content/ja/presentify-alternative-mac.html`, `resources/content/ko/presentify-alternative-mac.html`: 현지어 본문.
- `resources/content/locales.json`: Resources 명칭과 기존 UI 문자열.
- `scripts/build_resources.py`: 실제 번역 전환, 현지어 관련 자료 fallback, 홈 카드 보충, sitemap에서 이전 EN URL 제외.
- `scripts/verify_resources.py`: 의도된 URL 통합 예외, 상호 alternate, 현지어 관련 글, fallback의 실제 상태 검증.
- `en/draw-on-screen-mac/index.html`: 이전 콘텐츠 대신 최소한의 즉시 이동 페이지.
- 기존 홈·FAQ·화면 글·관련 글: 목적지 링크와 alternate의 제한적인 변경.

새 글 추가 방식은 기존 `resources/README.md`에 유지하고 현재 동작에 맞게 갱신했습니다.
