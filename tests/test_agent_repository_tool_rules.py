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
