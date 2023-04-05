from functools import reduce

from markdown import markdown

from format import (
    opening_tag,
    closing_tag, 
    self_closing_tag_no_space,
    self_closing_tag_space,
)

def get_html_tags() -> tuple[list[str], list[str]]:
    html_tags = [
        "abbr",
        "acronym",
        "address",
        "applet",
        "area",
        "article",
        "audio",
        "b",
        "base",
        "basefont",
        "bdi",
        "bdo",
        "big",
        "blink",
        "blockquote",
        "br",
        "button",
        "canvas",
        "caption",
        "center",
        "cite",
        "code",
        "col",
        "colgroup",
        "content",
        "data",
        "datalist",
        "dd",
        "del",
        "details",
        "dfn",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "element",
        "em",
        "embed",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frame",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hgroup",
        "hr",
        "html",
        "i",
        "input",
        "ins",
        "img",
        "isindex",
        "kbd",
        "keygen",
        "label",
        "legend",
        "li",
        "listing",
        "main",
        "map",
        "mark",
        "menu",
        "menuitem",
        "meter",
        "nav",
        "noembed",
        "noscript",
        "object",
        "ol",
        "optgroup",
        "option",
        "output",
        "p",
        "param",
        "plaintext",
        "pre",
        "progress",
        "q",
        "rp",
        "rt",
        "rtc",
        "ruby",
        "s",
        "samp",
        "script",
        "section",
        "select",
        "shadow",
        "small",
        "source",
        "spacer",
        "span",
        "strike",
        "strong",
        "style",
        "sub",
        "summary",
        "sup",
        "table",
        "tbody",
        "td",
        "template",
        "tfoot",
        "th",
        "thead",
        "time",
        "title",
        "tr",
        "track",
        "tt",
        "u",
        "ul",
        "v",
        "var",
        "video",
        "wbr",
        "xmp",
    ]
    telegram_supported_tags = [
        "b",
        "strong",
        "i",
        "em",
        "u",
        "ins",
        "s",
        "strike",
        "del",
        "span",
        "tg-spoiler",
        "a",
        "code",
    ]
    header_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    tags_to_remove = list(
        set(html_tags) - set(telegram_supported_tags) - set(header_tags),
    )

    return header_tags, tags_to_remove


def remove_tag(text: str, tag: str) -> str:
    replace_with = ""

    return (
        text.replace(opening_tag(tag=tag), replace_with)
        .replace(closing_tag(tag=tag), replace_with)
        .replace(self_closing_tag_no_space(tag=tag), replace_with)
        .replace(self_closing_tag_space(tag=tag), replace_with)
    )
    
    
def replace_header_tag(text: str, tag: str) -> str:
    return text.replace(
        opening_tag(tag=tag),
        opening_tag(tag="b"),
    ).replace(
        closing_tag(tag=tag),
        closing_tag(tag="b"),
    )
    
    
def remove_tags(text: str, tags: list[str]) -> str:
    return reduce(remove_tag, tags, text)
    
    
def replace_header_tags(text: str, header_tags: list[str]) -> str:
    return reduce(replace_header_tag, header_tags, text)


def markdown_to_html(text: str) -> str:
    html = markdown(text, extensions=["fenced_code"])
    headers_tags, tags_to_remove = get_html_tags()
    
    return replace_header_tags(
        text=remove_tags(text=html, tags=tags_to_remove),
        header_tags=headers_tags
    )
    