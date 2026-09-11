# PSNOVA エージェントガイド

## 最優先ルール：問題を検知したら即時停止する

**作業中に問題を1つでも検知した場合は、直ちに停止し、次のファイル、項目、確認、回避策、実装手順へ進んではならない。** 問題には、想定外の結果、検証またはテストの失敗、参照元と公開ページの不一致、データの欠落または曖昧さ、ツール/API/ネットワーク障害、編集競合、破損の疑い、説明できない差分、意図しない整形変更、ページ破損、停止または信頼できない自動処理、その他正しさを検証できない状態を含むが、これらに限らない。問題を黙って回避したり、方法を切り替えたり、まとめて先へ進めたり、進捗のために追加のリポジトリ変更を行ってはならない。唯一の例外は、すでに導入した変更によってリポジトリを既知の破損状態に残さないために厳密に必要な最小限の処置である。その処置後は停止する。何が起きたか、何を変更したかまたは変更していないか、現在の正確な状態を報告する。ユーザーがその報告後に新しい指示を出すまで作業を再開してはならない。

- **差分がテキストファイル末尾の単一改行（EOF newline）の追加または削除だけであり、内容・構文・動作へ影響しないことをread-only diffで確認できた場合は、問題または意図しない整形変更として扱わない。** この場合はEOF改行だけを戻すための追加commitを作成せず、停止せずに作業を継続する。EOF改行以外の差分が同時に存在する場合は、この例外を拡張解釈せず通常の停止判定を行う。

## 最優先ルール：HEADの停止判定に古い基準を使わない

**過去の引き継ぎ資料、古い会話、古いメモに記載されたHEADを、現在の停止判定基準として使用してはならない。** 停止判定に使える基準HEADは、直前の正常な書き込み、または直前のread-only確認で取得した最新HEADだけとする。自分自身がその後に正常なcommitを作成した場合は、そのcommit後のHEADを新しい基準HEADとして扱い、それ以前のHEADへ比較基準を戻してはならない。

- HEAD不一致だけを理由に即停止してはならない。まず、不一致が自分自身の直前の正常commitによる既知の変化か、未認識の外部変更かをread-onlyで確認する。
- 自分自身が作成し、正常に検証済みのcommitによるHEAD変化は異常扱いしてはならない。
- HEAD差分による停止は、未認識の外部変更、親commit不一致、想定外branch変更、想定外file差分など、説明できない変更を確認した場合に限る。
- 正常なcommitまたはHEAD確認のたびに、その最新HEADを以後の基準として扱う。より古いHEADを後続sessionやhandoverから復活させ、停止判定へ使ってはならない。

## 最優先ルール：JavaScriptは凍結する

**このリポジトリのJavaScriptを編集してはならない。** `.js` ファイルの作成、変更、削除、改名、移動、再生成、置換、その他あらゆる変更を禁止し、インラインJavaScriptの追加・変更も禁止する。既存JavaScriptは現在の監査後に凍結されたものとして扱う。要求された変更にJavaScriptが必要に見える場合は、JavaScriptを変更しない静的HTML/CSSまたはリポジトリツールで解決する。誤った静的マークアップ、データ、メタデータ、スタイル、アセットを補正する回避策としてJavaScriptを使ってはならない。JavaScriptを変更できるのは、ユーザーがこのルールを明示的に撤回し、JavaScript編集を直接許可した場合だけである。

## 最優先ルール：リポジトリをcloneしない

**`git clone`、`gh repo clone`、その他このリポジトリの新しいローカルcloneを作成する操作を実行してはならない。** 既存のローカルworktreeがある場合はそれを使い、それ以外では接続済みGitHubリポジトリツールを使って読み書きする。一時、バックアップ、検証、使い捨て、回避策目的のcloneを禁止し、ツール制約やネットワーク問題を回避するためのcloneも禁止する。新しいcloneを作成できるのは、その特定作業についてユーザーが明示的に許可した場合だけである。

## 最優先ルール：実行可能な編集方法がある場合は代替手段を探さない

**利用可能なリポジトリ操作で要求された変更を完了できる場合、その操作が不便、大規模、または全文置換を必要とするという理由だけで別の編集方法を探してはならない。** 特に、ツールが大きなテキストファイルの全文置換を要求する場合は、その既知の実行可能な方法を直接使い、無関係な内容を完全に保持する。既知の方法が実際に失敗した、または安全に変更を完了できない場合を除き、patch API、Git data/tree API、workflow、一時branch、ローカルclone回避策、その他の代替手段を調査してはならない。実行可能な実装経路が判明した後は、方法探索そのものを禁止し、実行と検証を優先する。

## 最優先ルール：Agent.mdは日本語で記述する

**`Agent.md` の見出し、説明文、ルール本文、注記は日本語で記述し、英語の説明文へ変更してはならない。** 新規ルール追加、既存ルール修正、全体整理のいずれでも日本語を維持する。例外は、コマンド、ファイルパス、API名、コード識別子、クラス名、正式な製品・技術名称、テスト名、URL、実装上正確な文字列一致に必要なリテラルなど、翻訳すると意味または動作が変わる技術要素だけである。技術要素を除き、英語だけの見出し、段落、箇条書き、説明を新たに記載してはならない。

## 最優先ルール：Agent.mdの自然言語をテスト契約にしない

**テストコードから `Agent.md` を読み込み、その自然言語、見出し、語順、翻訳表現、特定の部分文字列が存在することをテスト契約としてはならない。** テストはHTML、CSS、JavaScript、生成結果、ファイル構成、実行結果、その他の実装状態そのものを検証する。ルールの存在確認を目的として `Agent.md` の特定文言を `assert`、完全一致、部分一致、正規表現等で固定してはならない。`Agent.md` の翻訳、表現改善、文章整理だけで実装テストがFAILする構造を禁止する。既存の `tests/test_no_agent_text_contracts.py` による再発防止を維持する。ただし、ファイルのbyte数や行数など自然言語の内容に依存しない構造的な破損検知は許可する。

## 最優先ルール：Agent.mdを破壊的に全文置換しない

**`Agent.md` を編集するときは、現在の全文を正として無関係な内容を保持し、要約や再構成による全文置換を行ってはならない。** 書き込み前にcurrent `master`のblobをread-onlyで取得し、変更対象の箇所と置換内容を確定する。全文置換型APIを使う場合でも、取得したcurrent全文を基礎に対象箇所だけを変更し、記憶や要約からファイル全体を再生成してはならない。

- ユーザーが`Agent.md`全体の再設計・大幅整理を明示要求していない限り、予定差分が20行を超える削除、または変更前比10%以上のbyte数減少になる場合は書き込まず、最優先の即時停止ルールに従う。
- `Agent.md`変更をcommitした直後は、次の実装項目へ進む前に親commitとの差分をread-onlyで確認する。想定外のsection削除、説明不能な大量差分、意図しない全文整形を検知した場合は、既知の正常HEADへ戻すための最小復旧だけを行って停止する。
- `Agent.md`の安全性確認を省略する理由として、documentation-only変更、単純な表現修正、全文置換APIしかないことを使ってはならない。

## 最優先ルール：人が読む文章は日本語で記述する

**このリポジトリで人が読むことを目的とする文章は、原則として日本語で記述する。** commit message、PR・issueのtitle/body/comment、release note、changelog、repository documentation、運用メモ、ユーザー向けCLI出力・テスト失敗メッセージ、公開UI文言、説明文、その他利用者や開発者が読む文章を日本語にする。英語だけのcommit messageや説明文を新たに作成してはならない。例外は、コマンド、ファイルパス、API名、コード識別子、クラス名、正式な製品・技術名称、URL、外部仕様で固定された文字列、実装上正確な一致が必要なリテラル、その他翻訳すると意味または動作が変わる技術要素だけである。ユーザーが特定の文章について別言語を明示指定した場合、または外部システムが別言語・固定形式を必須とする場合のみ、その対象に限って例外とする。

## 最優先ルール：推測値・ダミー値でツールやAPIを呼び出さない

**API、リポジトリツール、外部ツールに、推測、仮置き、ダミー、合成、その他未検証の識別子や引数を渡してはならない。** `0`、`1` など実在確認していないPR/issue/commit/job/run ID、推測したファイルパス、branch名、SHA、URL、resource identifierを使ってはならない。既存resourceの識別子が必要な場合は、ユーザーが明示した値、または直前までの成功したread/search/list結果から取得した値だけを使う。必要な識別子が不明なら、現在の作業に本当に必要な場合だけ適切なdiscovery/read操作で取得し、不要なら呼び出し自体を行わない。tool health check、probe call、dummy request、動作確認だけを目的とした無関係なAPI callは、ユーザーがtool/API diagnosticsを明示要求した場合を除き禁止する。

## 最優先ルール：GitHub書き込み操作を試行・プローブに使わない

**GitHubへの書き込み系操作は、実際に適用することが確定したリポジトリ変更のためにだけ使用し、動作確認、疎通確認、試行、プローブ、API仕様確認、エラー確認、tool health checkその他の実験目的で実行してはならない。** `update_file`、`create_file`、`delete_file`、`create_blob`、`create_tree`、`create_commit`、`update_ref` その他のwrite操作を、実際の修正以外の目的で呼び出してはならない。

- `x`、空文字、`dummy`、`test`、`placeholder`、仮ファイル、仮データ、その他実際に適用しない内容を書き込んではならない。
- 存在確認されていないSHA、推測したSHA、仮のSHA、未検証のbranch、path、resource identifierをwrite操作へ渡してはならない。必要な識別子は、ユーザーが明示した値または直前の成功したread/list/fetch結果から取得した実在値だけを使う。
- branchまたは実際に適用するcommitから参照されない孤立blob、孤立tree、孤立commitを意図的に作成してはならない。`create_blob` を単独で使用することを禁止する。`create_blob` は、同一実装項目として直後に `create_tree`、`create_commit`、`update_ref` まで適用することが事前に確定し、必要なtree・parent・target refをread-only操作で確認済みの場合に限り使用できる。
- APIのschema、引数仕様、利用可能なoperation、resourceの存在、現在状態を確認する場合は、`list_resources`、`fetch`、`fetch_file`、`fetch_blob`、`compare_commits` その他のread-only操作だけを使う。write操作の失敗結果から仕様を推測するためのprobeを禁止する。
- 実際のrepository変更を行う前に、変更対象、変更内容、current `master` HEAD、必要なfile/blob SHAその他writeに必要な識別子をread-only操作で確認する。実際に適用する変更内容が確定するまでwrite操作を呼び出してはならない。
- 安全な編集方法が確認できない、または既知の編集経路で正しさを保証できない場合は、repositoryへ実験的なwriteを行ったり別write APIを順番に試したりせず、最優先の即時停止ルールに従って停止して報告する。
- 本番repositoryをAPI実験、tool diagnostics、疎通試験、エラー再現の場として使用してはならない。ユーザーがdiagnosticsを明示要求した場合でも、read-onlyで完結できない診断を本番repositoryへwriteして実施してはならない。

## 最優先ルール：GitHub `update_file` は取得済みschemaどおりに呼び出す

**既存UTF-8 text fileをGitHubコネクタの `update_file` で更新する場合は、実行直前に利用可能なaction schemaをread-onlyで確認し、その正式なfield名と型だけを使って1回で呼び出す。** 現在の `update_file` では必須fieldとして `repository_full_name`、`path`、`content`、`message`、`sha` を渡し、このrepositoryでは対象branchを明示する場合は `branch: "master"` を使う。`repository_full_name` を `repo_full_name` など別actionのfield名へ置換してはならず、必須fieldの欠落、schema外fieldの追加、field名の推測、型の不一致、引数objectの余分なnest、object全体のJSON文字列化を禁止する。

- `content` にはpatch、diff、部分断片ではなく、直前に取得したcurrent fileを基礎とする完全なUTF-8 replacement textを渡す。
- `sha` には同じ対象fileを直前の `fetch_file` で取得したcurrent blob SHAを使い、古いSHA、commit SHA、tree SHA、推測値を渡してはならない。
- schemaを未確認のままwriteを試して `argument_binding` やvalidation errorから正しい引数形式を推測してはならない。schema確認はwrite前のread-only discoveryで完了させる。
- `argument_binding` が発生した場合、そのwriteは適用されていないものとして扱うが、引数を推測修正して連続再試行してはならない。原因となったfield名・型・構造をread-only schemaと照合して確定し、ユーザーの指示または既存の停止ルールに従う。

## 最優先ルール：GitHub write gateを必ず通過する

**GitHubへのwrite操作は、実行直前に次の4条件をすべて満たした場合だけ実行する。1つでも満たさない場合はwrite actionを呼び出してはならない。**

1. 使用するwrite actionが、現在の実装項目で事前に確定したwrite allowlistに含まれていること。既存file更新で `update_file` が利用可能かつ要件を満たす場合、その実装項目のwrite allowlistは `update_file` のみとし、途中で `create_blob`、`create_tree`、`create_commit`、`update_ref` その他のwrite経路へ切り替えてはならない。
2. writeへ渡すrepository、branch、path、SHA、IDその他の識別子が、ユーザーの明示値または直前の成功したread-only結果から取得した実在値であり、推測値、ダミー値、仮値を1つも含まないこと。
3. 使用するwrite actionの現在のschemaをread-onlyで確認済みであり、正式なfield名、必須field、型、nest構造と完全に一致すること。
4. 現在の目的を満たす既知のより単純なwrite経路を迂回していないこと。schema確認、疎通確認、tool動作確認、失敗再現だけを目的とするwriteではないこと。

- gate判定のためにwriteを実行してはならない。4条件の確認はread-only情報だけで完了させる。
- 4条件のどれかを確認できない場合、別write actionを試さず、最優先の即時停止ルールに従う。

## 最優先ルール：現在の作業に直接必要なツールだけを使う

**すべてのtool callは、現在実行中の実装または検証手順を完了するために直接必要でなければならない。** `master` 上のfile直接編集が現在の目的である場合、その作業に具体的に必要でないPR、issue、workflow、branch、release、artifact、その他のAPIを呼び出してはならない。利用可能なツールを試すこと自体を目的に呼び出したり、現在の作業と関係のないresourceを探索してはならない。必要性を説明できないtool callは実行しない。

## 最優先ルール：GitHubファイルはGitHubコネクタで取得する

**このリポジトリのGitHub上のファイルを取得・閲覧する場合は、接続済みGitHubコネクタの `fetch_file`、`fetch_blob`、`fetch` などGitHub用read操作だけを使う。** `container.download`、汎用download tool、外部HTTP downloader、raw URLを別ツールへ渡す方法、その他GitHubコネクタ外の経路へ迂回してはならない。GitHubコネクタで取得できるファイルについて、別経路を試すためのprobe、tool-health check、事前URL閲覧、download workaroundを行ってはならない。GitHubコネクタのreadが実際に失敗した場合は最優先の即時停止ルールに従って停止し、ユーザーの新しい指示なしに別取得手段へ切り替えない。

## 最優先ルール：未対応のGitHub REST endpointを自作URLで代用しない

**接続済みGitHubコネクタに目的のresourceを取得・操作する専用actionが提供されていない場合、その不足を補うためにGitHub REST endpointのURLを推測・組み立てて `fetch` その他の汎用GitHub readへ渡してはならない。** 利用可能な専用action、またはすでに仕様上対応が確認できているrepository/file/commit/branch等のread操作だけを使用する。必要なread経路が提供されていない場合は、その状態を未確認として扱い、別endpointを順番に試したりallowlistの境界を探るprobeを行わず、最優先の即時停止ルールに従う。

## 最優先ルール：GitHubへの直接HTTP接続・Code Search・ブラウザ経由取得を禁止する

**このリポジトリのコードやrepository contentへアクセスするために、`curl`、`Invoke-WebRequest`、その他のHTTP clientからGitHub API、`raw.githubusercontent.com`、GitHub raw URLへ直接接続してはならない。** GitHub Code Searchも使用してはならず、検索結果、0件、件数、index状態をcurrent repository stateの確認や探索に使ってはならない。Web検索、Webブラウザ、通常のWeb fetchを使ってGitHubページやraw URLからrepository contentを取得・確認することも禁止する。ただし、**ユーザーがその特定作業でGitHubのブラウザ/Web経由アクセスを明示的に指定した場合に限り、Web検索・ブラウザ経由のGitHub閲覧だけを例外として許可する。** この例外は `curl`、`Invoke-WebRequest`、GitHub Code Searchの使用許可を意味しない。通常は接続済みGitHubコネクタのread操作、または既存local worktreeの直接ファイル読取を使用する。

## 目的

このリポジトリは、GitHub Pagesで公開するPSNOVA攻略サイトのソースである。
近代化作業では、既存データとURLを保持しながら、使いやすさ、保守性、SEO、アクセシビリティ、収益化への準備を改善する。

## 絶対遵守ワークフロー

1. 実装項目は1件ずつ変更する。
2. データ量の多いページを変更する前に、その作業が明示的にデータ変更を求めていない限り、既存ゲームデータを正とする。
3. 自動確認できる変更では、可能な限りテストを追加または拡張する。
4. 完了した実装項目ごとに、内容が分かるコミットメッセージで別々にコミットする。
5. 機能変更と無関係なリファクタリングを混在させない。
6. ユーザーが明示的にURL変更を指示しない限り、`/PSNOVA/` 配下の既存公開URLを維持する。
7. 変更によって回帰が発生した、または検証中にその他の問題が見つかった場合は、最優先の即時停止ルールに従って直ちに停止する。問題を報告し、ユーザーが新しい指示を出すまで別項目へ進んだり追加修正を試みてはならない。
8. GitHub Actionsのテストは手動実行のみとする。各コミット後には実行しない。予定した実装バッチを完了してから、最終検証として `workflow_dispatch` で `tests` workflowを1回だけ実行する。
9. このプロジェクトでは画像生成ツールを使用しない。視覚的変更は、リポジトリ内のHTML/CSSと既存の承認済みアセットだけで実装する。JavaScriptは上記最優先ルールにより凍結されている。
10. 過去資料の確認に `reference/` を再作成・復元したり、依存先として使ってはならない。過去資料の確認が必要な場合は、現存するrepository contentまたはユーザーが明示的に提供した資料を使用する。
11. migration専用のprogram、workflow、request file、testを再導入してはならない。公開ページの保守はcurrent public sourceと通常の回帰テストを直接更新して行う。
12. **ページ固有の静的HTMLまたはゲームデータをruntime JavaScriptで補正してはならない。** 決定的なcontentやmarkupは生HTMLまたはそのgeneratorを直接修正する。既存JavaScriptが提供する本質的なruntime behaviorやsitewide shared componentはこの禁止の対象外だが、page HTML編集の回避策として使用してはならない。
13. **ユーザーが報告した回帰によって修正仕様が確定した場合、作業手順・安全策・判断基準としてエージェントが実行時に参照する必要がある恒久ルールだけをこのガイドへ記録する。HTML、CSS、JavaScript、ファイル構成その他の実装状態を自動判定できる仕様は、サイト横断であってもregression testへ記録し、`Agent.md`と二重管理しない。** ユーザーが明示的に誤りとした挙動を後から再導入してはならない。
14. **公開UI文言には、developer-facingなfield名、camelCase、internal identifier、説明のないmixed-language abbreviationではなく、読者向けの明確な日本語を使う。** HP、GP、DLC、PSNOVAなど一般化したゲーム用語やofficial nameは、文脈上標準的で直ちに理解できる場合は使用してよい。
16. **guide pageとdata pageは、通常3文程度の簡潔なreader-facing introductionから始める。** pageが扱う範囲、比較・確認できる内容、情報の実用的な使い方を説明する。placeholder的な1行説明やコピーされたWiki断片を避ける。
21. **active developmentおよびpublishing branchは `master` のみとする。ユーザーがこのルールを明示的に撤回しない限り、feature branch、work branch、temporary implementation branch、PR branchを作成、切替、使用してはならない。通常の実装、commit、pushは `master` へ直接行う。既存backup/archive branchはread-onlyな歴史的recovery pointとして残してよいが、active workには使用しない。**
22. **保存資料から現在の公開ページを検証する場合は、読者に有用なgameplay fact、table row/value、note、requirement、exception、acquisition condition、password/code、quest detail、explanatory guide pointを意図せず捨ててはならない。** 完全な重複、保存Wiki/Waybackの外枠、analytics/ads/edit/comment UI、または別途根拠がある事実訂正を除き、有用な内容を保持する。可能ならcurrent public regressionまたはsentinel coverageを追加し、意図しない欠落を自動検知する。
23. **保存Wiki/Wayback pageやその他legacy pageを公開ページの代替として扱わず、読者に有用なgameplay contentを現在siteのstatic HTMLへ直接統合する。** 保存navigation、search box、edit control、ads、analytics、Wayback外枠、legacy page shellなど公開siteに不要な外枠は持ち込まない。
24. **同一page上で同じcolumn structureを持つtableは、原則として対応columnが縦に揃うよう同じcolumn widthを使う。** 各tableを個別に自動配分させるのではなく、そのpage周辺のtableをvisual referenceとする。ただし、同じwidthにすると重大なwrapping、clipping、読めないほど狭いcell、不要なhorizontal overflowが発生して明確にtableを壊す場合だけ、このconsistency requirementよりreadabilityを優先する。例外が必要なら、readabilityを保持し、実用的な範囲でpage-specific reasonを文書化またはtestする。width consistencyはstatic markupまたはCSSで実装し、runtime JavaScript repairでは実装しない。
25. **信頼できる範囲では効率的な実行を優先するが、batching、bulk automation、optimizationによって長時間停止したり進捗が不透明になってはならない。長時間かかりそうなtaskは停止する前にstrict sequential executionへ切り替え、1file/itemを確認し、その1変更を行い、検証し、必要に応じてcommitしてから次へ進む。実際に処理が停止した、またはbulk automationが信頼できなくなった場合、それは問題であり、方法を切り替えて継続するのではなく最優先の即時停止ルールに従って直ちに停止する。**

## セッション実行契約

- work session開始時に、そのsessionで実際に利用可能な現在のGit worktree、current branch、Git history、repository file、実行commandからbaselineを確立する。過去conversationからcurrent stateを推測してはならない。
- local worktreeが利用可能な場合、implementation work前に `git status`、`git branch --show-current`、`git log -5 --oneline`、`python tools/psnova_quality.py finish` を実行し、結果をsession baselineとして記録する。
- reflog、commit、deleted file、その他repository traceから以前の変更者を推測してはならない。current agentがそのsession中に実際に行ったoperationだけをcurrent agentの作業として帰属する。
- FAILまたはその他の問題を検知した場合は、最優先の即時停止ルールに従って直ちに停止する。報告では、その問題がsession開始前から存在したか、current sessionが導入したかを区別し、(1) current itemに直接関係する、(2) 後で明示的に予定されたitemに関係する、(3) current objective外、のいずれかに分類する。分類は報告目的のみであり、作業継続を許可するものではない。
- すでに導入した変更によってrepositoryを既知の破損状態に残さないため厳密に必要な最小処置を除き、同じrun中に検知した問題を修正、先送り、回避してはならない。問題を報告し、ユーザーの次の指示を待つ。
- objective、このguide、current code、testが十分な判断基準を提供している場合は、問題を検知していない間だけ次のplanned itemへ進む。質問するのは、product decisionが本当に曖昧な場合、irreversible/high-risk actionが必要な場合、利用できないexternal credential/informationが不可欠な場合、または最優先の即時停止ルールが発動した場合だけとする。
- 一時的なsession handover documentをremote repositoryへ作成・commitしてはならない。永続project ruleは `Agent.md` または別途明示承認されたpermanent documentへ記録し、一時handover noteはremote repository外に置く。

## サイト全体の不変条件

- 公開PSNOVA pageではspoiler-protection UXまたはspoiler warningを適用しない。plot detailを含む可能性があるという理由だけで、story/gameplay informationをspoiler専用の `<details>` / `<summary>`、`ネタバレを表示` control、masking、blur、spoiler caution、その他同様の処理で隠してはならない。ユーザーが特定の例外を明示要求しない限り、関連情報は直接表示する。

- ユーザー承認済みPSNOVA color paletteを保持する。automated contrast checkを満たすことだけを理由にsite colorを自動的にdarkenまたはreplaceしてはならない。ユーザーがcolor accessibility enforcementを明示要求した場合だけ、その対象について別途扱う。

- 通常のpost-fix quality gateには `python tools/psnova_quality.py finish` を使う。browser UI behaviorへ直接影響する変更だけ `targeted` を使い、残存static audit candidate一覧には `inventory` を使う。

- local Playwright UI health testのconnection-refusal failureをworker数削減で回避してはならず、shared test infrastructure側を修正する。
