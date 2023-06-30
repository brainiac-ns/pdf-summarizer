import concurrent.futures
from collections import defaultdict
from typing import List, Dict

from transformers import pipeline


def summarize_text(text: str):
    summarizer = pipeline(
        "summarization",
        model="t5-small",
        tokenizer="t5-small",
    )
    summarized = summarizer(
        text,
        max_length=100,
        min_length=30,
        do_sample=False,
    )
    return summarized[0]["summary_text"]


def summarize_strings(strings: str) -> List:
    summarized_strings = []
    for string in strings:
        summarized = summarize_text(string)
        summarized_strings.append(summarized)
    return summarized_strings


def process_paragraph(paragraph: str) -> str:
    if len(paragraph) > 10:
        return summarize_text(paragraph)
    else:
        return paragraph


def summarize_pdf(text: List[str], progress_bar) -> Dict:
    paragraphs = defaultdict(str)
    key = ""
    for t in text:
        try:
            int(t[0])
            if len(t) < 100:
                key = t.replace("\n", " ")
                paragraphs[key] = ""
        except Exception:
            paragraphs[key] += t.replace("\n", " ")

    summarized = {}  # Dictionary to store the summarized paragraphs

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the summarization tasks in parallel
        futures = [executor.submit(process_paragraph, v) for v in paragraphs.values()]

        for i, (k, future) in enumerate(zip(paragraphs.keys(), futures)):
            progress_bar.progress(i / len(paragraphs))

            # Get the result of each summarization task
            result = future.result()
            summarized[k] = result
    progress_bar.progress(1)
    return summarized
