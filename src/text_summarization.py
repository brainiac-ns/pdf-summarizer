from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import List


def summarize_text(
    text: List[str],
    tokenizer=T5Tokenizer.from_pretrained("t5-base"),
    model=T5ForConditionalGeneration.from_pretrained("t5-base"),
):
    inputs = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, min_length=30)

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary


def not_sum(text: str) -> bool:
    total = 0
    for lines in text.split("\n"):
        if len(lines) < 10 and len(lines.strip()) == 1:
            total += 1
    return total < 3 and total != 0


def to_summarize(text_to_summarize: str) -> list:
    summarized = []
    for block in text_to_summarize:
        if not_sum(block):
            summarized.append(block)
        else:
            summary = summarize_text(block)
            summarized.append(summary)
    return summarized
