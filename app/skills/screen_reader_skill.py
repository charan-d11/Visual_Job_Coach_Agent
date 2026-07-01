"""
screen_reader_skill.py
----------------------
ADK tool: format agent output to be optimally readable by screen readers.
Removes visual-only markup and structures content for text-to-speech.
"""


def format_for_screen_reader(text: str, announce_count: bool = True) -> dict:
    """
    Format text output for screen reader / TTS consumption.

    Transforms structured content into clean, linear spoken-word text:
    - Replaces bullets/dashes with numbered announcements
    - Removes markdown syntax
    - Adds natural pauses via punctuation

    Args:
        text: Raw text (may contain markdown, bullets, etc.).
        announce_count: If True and text contains a list, prepend item count.

    Returns:
        dict with 'formatted_text' (screen-reader-friendly string).
    """
    import re

    lines = text.split("\n")
    clean_lines = []
    list_items = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detect bullet points or numbered lists
        list_match = re.match(r"^[\-\*\•]\s+(.+)$", stripped) or re.match(r"^\d+\.\s+(.+)$", stripped)
        if list_match:
            list_items.append(list_match.group(1))
        else:
            # Flush pending list
            if list_items:
                if announce_count:
                    clean_lines.append(f"There are {len(list_items)} items.")
                for i, item in enumerate(list_items, 1):
                    clean_lines.append(f"Item {i}: {item}.")
                list_items = []
            # Remove markdown formatting
            stripped = re.sub(r"\*\*(.*?)\*\*", r"\1", stripped)  # bold
            stripped = re.sub(r"\*(.*?)\*", r"\1", stripped)       # italic
            stripped = re.sub(r"`(.*?)`", r"\1", stripped)         # code
            stripped = re.sub(r"#{1,6}\s+", "", stripped)          # headings
            clean_lines.append(stripped)

    # Flush any remaining list items
    if list_items:
        if announce_count:
            clean_lines.append(f"There are {len(list_items)} items.")
        for i, item in enumerate(list_items, 1):
            clean_lines.append(f"Item {i}: {item}.")

    formatted = " ".join(clean_lines)
    return {"formatted_text": formatted, "original_length": len(text), "formatted_length": len(formatted)}


def announce_section(section_name: str, content: str) -> dict:
    """
    Wrap content with a spoken section announcement.

    Args:
        section_name: e.g. "Job Results", "Resume Summary".
        content: The content for that section.

    Returns:
        dict with 'announcement' string.
    """
    announcement = f"Beginning {section_name} section. {content} End of {section_name}."
    return {"announcement": announcement}
