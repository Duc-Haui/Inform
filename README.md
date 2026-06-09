# InFoRM: Individual Fairness on Graph Mining
Dự án này thực hiện các thuật toán khử thiên vị trên đồ thị dựa trên nghiên cứu InFoRM (KDD 2020).

## 1. Cài đặt
1. Tạo môi trường ảo: `conda create -n inform_env python=3.9`
2. Cài đặt thư viện: `pip install -r requirements.txt`

## 2. Cách chạy thực nghiệm
- Bước 1: Chạy các notebook trong thư mục `notebooks/` theo thứ tự:
  1. `demo_LINE.ipynb`
  2. `demo_PageRank.ipynb`
  3. `demo_spectral_clustering.ipynb`
- Bước 2: Dữ liệu kết quả sẽ được lưu tự động vào `results/`.

## 3. Cấu trúc mã nguồn
- `methods/`: Chứa 3 chiến lược can thiệp (Debias Graph, Model, Result).
- `load_graph.py`: Xử lý việc nạp dữ liệu.





