# TeacherPalette Resources 구현 보고

2026-10-06 · 로컬 구현 및 검증 완료. 아직 배포하지 않았습니다.

## Architecture

기존 프로젝트는 프레임워크나 package.json 없이 HTML·CSS·JavaScript를 직접 제공하는
정적 사이트입니다. 홈은 `/`에서 쿼리와 `tp.lang`으로 9개 언어를 전환하고, 기존
실용 가이드는 언어별 디렉터리에 있습니다. `/guides/`에는 별도의 기존 콘텐츠
컬렉션과 클라이언트 번역·헤더가 있어 모두 보존했습니다.

- 새 Resources도 `/{locale}/resources/{article-id}/index.html` 정적 파일로 제공합니다.
- 메타데이터·카테고리·관련 글·언어별 본문 경로: `resources/content/articles.json`
- 실제 영어 본문: `resources/content/en/*.html`
- 현지어 UI·기존 가이드 경로: `resources/content/locales.json`
- 공통 HTML: `resources/templates/page.html`
- 생성: `scripts/build_resources.py` — Python 표준 라이브러리만 사용합니다.
- 검증: `scripts/verify_resources.py`

빌드 결과를 저장소에 함께 두므로 기존 호스팅 설정을 바꿀 필요가 없습니다.
홈 메뉴·하단 카드·푸터는 명시적으로 표시한 관리 구간만 생성기가 갱신합니다.
본문은 JavaScript 없이도 읽고 검색할 수 있습니다. 새로운 CMS·의존성을 추가하지 않았습니다.

## Pages Created

배포 후 사용할 canonical URL은 다음과 같습니다. 현재는 같은 경로를
`http://127.0.0.1:8765` 로컬 서버에서 확인할 수 있습니다.

| 페이지 | URL |
|---|---|
| EN Resources | https://teacherpalette.com/en/resources/ |
| JA ガイド | https://teacherpalette.com/ja/resources/ |
| KO 가이드 | https://teacherpalette.com/ko/resources/ |
| Presentify Alternative for Mac | https://teacherpalette.com/en/resources/presentify-alternative-mac/ |
| How to Annotate Your Screen on Mac | https://teacherpalette.com/en/resources/annotate-screen-mac/ |
| Screen Annotation for Teachers on Mac | https://teacherpalette.com/en/resources/screen-annotation-teachers-mac/ |

EN 인덱스는 새 기사 3개와 기존 영어 실용 가이드 5개를 연결합니다.
JA·KO 인덱스는 각 언어의 기존 가이드 5개를 연결합니다.

## Content and product evidence

현재 홈·FAQ·기존 실용 가이드·기존 `/guides/` 글을 근거로 작성했습니다.
화면 주석 도구, Spotlight·Laser·Magnifier·커서 도구, 다중 페이지 Whiteboard와
저장된 세션, PDF 가져오기·내보내기, 사용자 팔레트와 단축키, Sidecar를 통한
Apple Pencil 필압 지원, 휴식 타이머를 확인했습니다.

PDF는 Whiteboard의 PDF 가져오기 기능으로 설명하며, PDF 드래그 앤 드롭을
지원한다고 주장하지 않습니다. 화면 오버레이와 원본 문서 편집·PDF 저장을
구분합니다. 무료 체험은 기존 사이트의 신규 구독자 7일 체험 조건과 일치시켰습니다.

Presentify의 기능·가격·정책을 저장소에서 검증할 수 없어 경쟁 제품의 기능
유무를 단정하는 체크표를 만들지 않았습니다. 대신 같은 설명을 두 도구에서
시험하는 평가 방법과 TeacherPalette에서 확인된 작업 흐름을 비교표로 제공합니다.
기존 Kim의 강사·개발자 소개를 짧게 재사용했으며 가짜 리뷰나 추천사를 추가하지 않았습니다.

## SEO

- 6개 페이지에 고유 title·description과 self-canonical을 제공합니다.
- OG title·description·URL, Twitter title·description, 기존 공식 소셜 이미지를 사용합니다.
- 기사 title은 각각 `Presentify Alternative for Mac | TeacherPalette`,
  `How to Annotate Your Screen on Mac | TeacherPalette`,
  `Screen Annotation for Teachers on Mac | TeacherPalette`입니다.
- 기사에는 실제 내용에 맞는 `Article`과 `BreadcrumbList`, 인덱스에는
  `CollectionPage`와 `ItemList`를 제공합니다.
- 존재하지 않는 author·날짜·rating·review를 만들어 넣지 않았습니다.
- 인덱스는 EN·JA·KO를 상호 hreflang으로 연결합니다. 기사 hreflang은 실제
  출판된 언어만 포함하며 현재는 EN과 영어 x-default만 있습니다.
- 정적 sitemap에 새 URL 6개를 추가했습니다. 기존 URL 48개와 robots.txt를 보존했습니다.
- 홈 메뉴·푸터·하단 카드 → Resources → 기사 → 관련 기사 → 공식 App Store
  흐름을 연결했습니다. 기존 EN 화면·데모·PDF 가이드와 JA·KO 화면 가이드에도
  관련 Resources 링크를 추가했습니다.

CTA 주소는 별도 복사본을 관리하지 않고 빌드 시 기존 홈의 primary App Store
링크에서 읽습니다. 모두 공식 앱 ID `6783567350`을 사용합니다.

기존 `/en/draw-on-screen-mac/`의 URL·메타데이터는 유지했습니다. 새 화면 주석
기사는 준비·도구 선택·필기·지우기·앱으로 복귀·공유 화면 확인을 다루는 긴
사용법이고, 기존 페이지는 제품 기능 소개로 남아 있습니다. 검색 결과의 실제
중복 경쟁 여부는 배포 후 Search Console 데이터로 판단해야 합니다.

## Localization

영어 기사 3개만 출판했습니다. 일본어·한국어 경로에 영어 기사를 복제하거나
미완성 기사 페이지를 생성하지 않았습니다. 두 현지어 인덱스와 홈 카드에는
이미 있는 현지어 가이드를 표시합니다. 영어 기사 상단의 언어 링크는 “Resource
libraries”로 명시하여 현지어 기사 번역과 혼동하지 않도록 했습니다.

추후 같은 article ID에 `locales.ja` 또는 `locales.ko` 메타데이터와 현지어 본문을
추가하면 해당 기사 URL·카드·관련 글·hreflang·사이트맵이 생성됩니다. 국가별로
별도 검색 의도를 공략하는 새 ID의 현지어 기사도 추가할 수 있습니다.
그 외 6개 홈 언어에서는 영어 라이브러리임을 메뉴와 섹션 제목에 명시합니다.

## Design and Performance

실제 홈에서 사용하는 네이티브 글꼴, 밝은 배경, 파란 액센트, 라운드 카드,
버튼과 `tp.theme` 테마 설정을 재사용했습니다. 기존 제품 Hero·가격·기능
섹션은 유지하고 작은 Resources 섹션을 시스템 요구 사항 뒤에 배치했습니다.

기존 영상과 포스터만 사용합니다. 네이티브 재생 컨트롤, `playsinline`,
`preload="none"`으로 사용자 재생 전 MP4 로딩을 유예하며 새 iframe·자동재생
영상을 추가하지 않았습니다. 영상 영역의 비율을 예약하고 텍스트로도 작업
방법을 설명합니다. 좁은 화면의 비교표는 자체 스크롤 영역 안에서 이동합니다.

새 메뉴 항목으로 긴 언어에서 발생한 넘침을 해결하기 위해 홈의 기존 접이식
메뉴를 1200px 이하에서도 사용합니다. 본래 언어·테마·가격·도움말 메뉴를 유지합니다.

## Verification

- 정적 production HTML 생성 및 `--check` 재현성 검사 성공.
- 6개 새 페이지의 로컬 HTTP 응답·메타데이터·구조화 데이터·CTA·사이트맵 검사 성공.
- 정적 HTML 62개의 내부 링크·앵커·미디어 경로 검사: 깨진 링크 0개.
- sitemap: 유효한 URL 54개. 기존 URL 48개 모두 유지.
- 수정된 기존 페이지의 meta·canonical·hreflang 선언이 이전과 동일함을 대조했습니다.
- 새 페이지 6개를 1280px 데스크톱·768px 태블릿·390px 모바일에서 확인했습니다.
- 홈 9개 언어를 1440·1280·1201·1024·768·390·320px에서 확인했습니다.
  총 63개 조합에서 메뉴 넘침 0건.
- 모바일 비교표: 페이지 밖 넘침 없이 내부 가로 스크롤 동작.
- 모바일 메뉴 펼침·Escape 닫기, 화면 테마 전환·복원, 목차 이동 확인.
- 태블릿 홈 메뉴에서 한국어 전환 후 `/ko/resources/` 이동 확인.
- 새 페이지 브라우저 경고·오류 로그 없음. 새 JavaScript 문법 검사와 diff 공백 검사 통과.

프레임워크 빌드가 없는 프로젝트라 `npm build`는 사용하지 않았습니다.
이 저장소의 배포 산출물인 정적 HTML을 생성·검증했습니다. 배포, 실제 검색 색인,
실사용 Core Web Vitals와 organic traffic 성과는 이번 로컬 검증 범위에 포함되지 않습니다.

## Future Content

다음 글을 추가할 때 `resources/content/en/<slug>.html`을 작성하고,
`resources/content/articles.json`에 메타데이터와 관련 글을 등록한 뒤
`python3 scripts/build_resources.py`와 `python3 scripts/verify_resources.py`를
실행하면 됩니다. 구체적인 JSON 예제와 현지화 방법은 `resources/README.md`에 있습니다.

다음 후보로 화면 발표 중 그리기, Magnifier 사용법, 교사용 PDF 설명, 코딩
튜토리얼 활용 사례를 같은 구조에서 추가할 수 있습니다. 비교 글은 경쟁 제품의
현행 공식 자료를 검증한 뒤 사실 범위에 맞게 작성해야 합니다.
