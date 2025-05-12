from transformers import pipeline

def filter_data(titles: list[str]) -> list[dict]:

    data_filter_model = pipeline("zero-shot-classification",
    model="knowledgator/comprehend_it-base")
    
    candidate_labels=[
        "relevant to economics or finance",
        "irrelevant to economics or finance"
    ]

    output = data_filter_model(titles, candidate_labels)

    filtered_titles = []

    for title, result in zip(titles, output):
        if result["labels"][0] == "relevant to economics or finance":
            filtered_titles.append(title)

    return filtered_titles
