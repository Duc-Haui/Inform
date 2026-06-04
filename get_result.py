import os
import json
import matplotlib.pyplot as plt
import numpy as np


def read_robust_json(file_path):
    """Hàm trị lỗi Extra Data"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    data_runs = []
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(content):
        while idx < len(content) and content[idx].isspace():
            idx += 1
        if idx >= len(content):
            break
        try:
            obj, end_idx = decoder.raw_decode(content[idx:])
            data_runs.append(obj)
            idx += end_idx
        except json.JSONDecodeError:
            break
    return data_runs[-1] if data_runs else {}


def extract_metric(data, target_key):
    """Hàm siêu cấp: Gắp được cả số lẻ, mảng (list) và từ điển (dict)"""
    if not data or not isinstance(data, dict):
        return 0.0

    target_key = target_key.lower()

    for k, v in data.items():
        if target_key in k.lower():

            # 1. Nếu dữ liệu là Mảng (VD: "roc-auc": [0.68, 0.63]) -> Lấy số cuối cùng (đã debias)
            if isinstance(v, list) and len(v) > 0:
                return float(v[-1])

            # 2. Nếu dữ liệu là Số bình thường
            elif isinstance(v, (int, float)):
                return float(v)

            # 3. Nếu dữ liệu là Từ điển (VD: "bias": {"test": [0.96]})
            elif isinstance(v, dict):
                # Ưu tiên lấy kết quả của tập 'test'
                if "test" in v:
                    val = v["test"]
                    if isinstance(val, list) and len(val) > 0:
                        return float(val[-1])
                    if isinstance(val, (int, float)):
                        return float(val)

                # Nếu không có tập 'test', moi bừa giá trị đầu tiên hợp lệ
                for sub_k, sub_v in v.items():
                    if isinstance(sub_v, list) and len(sub_v) > 0:
                        return float(sub_v[-1])
                    if isinstance(sub_v, (int, float)):
                        return float(sub_v)

    return 0.0


# Cấu hình đường dẫn và các thông số
base_dir = "result"
tasks = {
    "line": {"name": "LINE", "metric": "auc", "metric_name": "ROC-AUC"},
    "pagerank": {"name": "PageRank", "metric": "ndcg", "metric_name": "NDCG"},
    "sc": {"name": "Spectral Clustering", "metric": "nmi", "metric_name": "NMI"},
}
methods = ["graph", "model", "result"]
method_labels = ["Debias Graph", "Debias Model", "Debias Result"]

# Tạo khung biểu đồ 1 hàng, 3 cột
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (task_key, task_info) in enumerate(tasks.items()):
    ax1 = axes[idx]

    utility_scores = []
    bias_scores = []

    for method in methods:
        json_path = os.path.join(base_dir, task_key, method, "evaluation_cosine.json")

        if os.path.exists(json_path):
            data = read_robust_json(json_path)

            # Sử dụng hàm nhíp gắp số liệu thay vì lấy thô như trước
            u_score = extract_metric(data, task_info["metric"])
            b_score = extract_metric(data, "bias")

            utility_scores.append(u_score)
            bias_scores.append(b_score)
        else:
            utility_scores.append(0.0)
            bias_scores.append(0.0)

    x = np.arange(len(method_labels))
    width = 0.35

    color1 = "tab:blue"
    ax1.set_ylabel(
        f"Hiệu năng ({task_info['metric_name']})", color=color1, fontweight="bold"
    )
    ax1.bar(x - width / 2, utility_scores, width, label="Hiệu năng", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = "tab:red"
    ax2.set_ylabel("Bias Score", color=color2, fontweight="bold")
    ax2.bar(x + width / 2, bias_scores, width, label="Bias", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    ax1.set_title(f"Tác vụ: {task_info['name']}", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(method_labels)

fig.tight_layout()

# Lưu thẳng ra ảnh, bỏ plt.show() để tránh lỗi treo giao diện nếu chạy trên Ubuntu server
plt.savefig("All_Tasks_Evaluation.png", dpi=300)
print("Đã vẽ xong! Biểu đồ nét căng nằm trong file All_Tasks_Evaluation.png")
