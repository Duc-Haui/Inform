#!/bin/bash
# =============================================================
# Script fix tất cả lỗi tương thích cho InFoRM project
# Chạy từ thư mục gốc: bash fix_inform.sh
# =============================================================

set -e
echo ">>> Đang chạy từ: $(pwd)"

# ---- Fix 1: from_scipy_sparse_matrix → from_scipy_sparse_array ----
echo ""
echo "=== [1/3] Fix from_scipy_sparse_matrix trong các file .py ==="
for f in load_graph.py utils.py method/debias_model.py method/debias_graph.py; do
    if [ -f "$f" ]; then
        sed -i 's/nx\.from_scipy_sparse_matrix/nx.from_scipy_sparse_array/g' "$f"
        echo "  ✓ $f"
    else
        echo "  ✗ Không tìm thấy $f — bỏ qua"
    fi
done

# ---- Fix 2: np.int deprecated → int trong demo_LINE.ipynb ----
echo ""
echo "=== [2/3] Fix np.int deprecated + sparse_matrix trong demo_LINE.ipynb ==="
python3 - << 'PYEOF'
import json

with open('demo_LINE.ipynb', 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['source'] = [
            s.replace('dtype=np.int)', 'dtype=int)')
             .replace('dtype=np.int,', 'dtype=int,')
             .replace('nx.from_scipy_sparse_matrix', 'nx.from_scipy_sparse_array')
            for s in cell['source']
        ]
        cell['outputs'] = []
        cell['execution_count'] = None

with open('demo_LINE.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("  ✓ demo_LINE.ipynb")
PYEOF

# ---- Fix 3: Clear old error outputs trong 2 notebook còn lại ----
echo ""
echo "=== [3/3] Clear error outputs cũ trong PageRank + spectral_clustering ==="
for nb in demo_PageRank.ipynb demo_spectral_clustering.ipynb; do
python3 - "$nb" << 'PYEOF'
import json, sys

path = sys.argv[1]
with open(path, 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

with open(path, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"  ✓ {path}")
PYEOF
done

# ---- Verify ----
echo ""
echo "=== Kiểm tra lại — không được có kết quả nào ==="
echo "  from_scipy_sparse_matrix còn sót:"
grep -rn "from_scipy_sparse_matrix" --include="*.py" . 2>/dev/null || echo "  (không còn)"
echo "  dtype=np.int còn sót trong notebook:"
grep -n "dtype=np.int)" demo_LINE.ipynb 2>/dev/null || echo "  (không còn)"

echo ""
echo "========================================="
echo " Tất cả đã được fix! Restart kernel Jupyter"
echo " và chạy lại từ đầu từng notebook."
echo "========================================="
