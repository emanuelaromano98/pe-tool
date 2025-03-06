from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json


def filter_reports(model, threshold):
    model = SentenceTransformer(model)

    reports = json.load(open("backend/output_files/reports.json", "r"))
    report_texts = [report['report'] for report in reports]

    embeddings = model.encode(report_texts, convert_to_tensor=True)
    removed_reports_idx = []

    for i in range(len(report_texts)):
        if i in removed_reports_idx:
            continue
        
        for j in range(i + 1, len(report_texts)):
            if j in removed_reports_idx:
                continue
            
            similarity = cosine_similarity(
                embeddings[i].cpu().numpy().reshape(1, -1),
                embeddings[j].cpu().numpy().reshape(1, -1)
            )[0][0]
            
            if similarity > threshold:
                removed_reports_idx.append(j)

    reports = [report for i, report in enumerate(reports) if i not in removed_reports_idx]

    with open("backend/output_files/reports.json", "w") as f:
        json.dump(reports, f, indent=4)

    print(f"Removed {len(removed_reports_idx)} reports due to similarity")