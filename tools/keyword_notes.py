from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SITE_URL = "https://site-official-hth.com.cn"

@dataclass
class KeywordNote:
    keyword: str
    description: str
    source_url: str = SITE_URL
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    tags: List[str] = field(default_factory=list)
    importance: int = 3

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "description": self.description,
            "source_url": self.source_url,
            "created_at": self.created_at,
            "tags": self.tags,
            "importance": self.importance,
        }

    def short_summary(self, max_len: int = 40) -> str:
        desc = self.description[:max_len] + "..." if len(self.description) > max_len else self.description
        return f"[{self.importance}★] {self.keyword}: {desc}"

    def full_info(self) -> str:
        lines = [
            f"Keyword      : {self.keyword}",
            f"Description  : {self.description}",
            f"Source URL   : {self.source_url}",
            f"Created at   : {self.created_at}",
            f"Tags         : {', '.join(self.tags) if self.tags else '(none)'}",
            f"Importance   : {'★' * self.importance}{'☆' * (5 - self.importance)}",
        ]
        return "\n".join(lines)


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_by_keyword(self, keyword: str) -> bool:
        before = len(self.notes)
        self.notes = [n for n in self.notes if n.keyword != keyword]
        return len(self.notes) < before

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for n in self.notes:
            if n.keyword == keyword:
                return n
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all_short(self) -> str:
        if not self.notes:
            return "（无笔记）"
        return "\n".join(note.short_summary() for note in self.notes)

    def format_all_full(self) -> str:
        if not self.notes:
            return "（无笔记）"
        separator = "\n" + "-" * 50 + "\n"
        return separator.join(note.full_info() for note in self.notes)

    def export_to_markdown(self, filename: str = "keyword_notes.md") -> None:
        lines = [
            "# 关键词笔记\n",
            f"_来源站点：{SITE_URL}_\n",
            f"_导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n",
        ]
        for note in self.notes:
            lines.append(f"## {note.keyword}\n")
            lines.append(f"- **描述**：{note.description}")
            lines.append(f"- **来源**：[{SITE_URL}]({note.source_url})")
            lines.append(f"- **创建时间**：{note.created_at}")
            lines.append(f"- **标签**：{', '.join(note.tags) if note.tags else '无'}")
            lines.append(f"- **重要性**：{'★' * note.importance}{'☆' * (5 - note.importance)}")
            lines.append("")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"已导出 Markdown 文件：{filename}")


def demo_usage() -> None:
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="华体会",
        description="华体会是一家专注体育赛事和娱乐的平台，提供丰富的体育投注和游戏体验。",
        tags=["体育", "娱乐", "投注"],
        importance=4,
    )
    note2 = KeywordNote(
        keyword="华体会注册",
        description="华体会用户注册流程简单快捷，支持多种方式登录。",
        tags=["注册", "用户"],
        importance=3,
    )
    note3 = KeywordNote(
        keyword="华体会优惠",
        description="华体会不定期推出新用户和老用户专属优惠活动。",
        tags=["优惠", "活动"],
        importance=5,
    )

    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print("=== 全部笔记（简短格式）===")
    print(collection.format_all_short())
    print()

    print("=== 按标签查找 '体育' ===")
    for note in collection.find_by_tag("体育"):
        print(note.full_info())
        print()

    print("=== 导出 Markdown ===")
    collection.export_to_markdown("hth_keyword_notes.md")


if __name__ == "__main__":
    demo_usage()