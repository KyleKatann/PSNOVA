from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "Agent.md"


def test_agent_requires_github_connector_for_repository_file_reads():
    agent = AGENT.read_text(encoding="utf-8")

    assert "## 最優先ルール：GitHubファイルはGitHubコネクタで取得する" in agent
    assert "接続済みGitHubコネクタ" in agent
    assert "`fetch_file`、`fetch_blob`、`fetch`" in agent
    assert "`container.download`" in agent
    assert "GitHubコネクタ外の経路へ迂回してはならない" in agent
    assert "ユーザーの新しい指示なしに別取得手段へ切り替えない" in agent


def test_agent_forbids_alternate_github_code_access_paths():
    agent = AGENT.read_text(encoding="utf-8")

    assert (
        "## 最優先ルール：GitHubへの直接HTTP接続・Code Search・ブラウザ経由取得を禁止する"
        in agent
    )
    assert "`curl`" in agent
    assert "`Invoke-WebRequest`" in agent
    assert "GitHub Code Searchも使用してはならず" in agent
    assert "Web検索、Webブラウザ、通常のWeb fetch" in agent
    assert "ユーザーがその特定作業でGitHubのブラウザ/Web経由アクセスを明示的に指定した場合" in agent
    assert "この例外は `curl`、`Invoke-WebRequest`、GitHub Code Searchの使用許可を意味しない" in agent
