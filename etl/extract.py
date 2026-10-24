"""
Module: extract.py
Mô tả: Trích xuất dữ liệu từ các tệp nguồn CSV (mô phỏng) vào Pandas DataFrame.
Tuân thủ: Section 4.1 và 5 của Hiến pháp Dự án (.specify/memory/constitution.md)
"""

import os
import logging
from typing import Dict, Optional
import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_FILES = [
    "orders.csv",
    "shipments.csv",
    "returns.csv",
    "return_costs.csv",
    "products.csv",
    "regions.csv",
    "carriers.csv",
]


def extract_data(data_dir: str = "data/sample") -> Dict[str, pd.DataFrame]:
    """
    Đọc toàn bộ file CSV nguồn từ thư mục chỉ định và trả về từ điển DataFrame.

    :param data_dir: Đường dẫn đến thư mục chứa các tệp CSV.
    :return: Dict[tên_thực_thể, pd.DataFrame]
    """
    logger.info("Bắt đầu quá trình trích xuất dữ liệu từ: %s", data_dir)
    extracted_data: Dict[str, pd.DataFrame] = {}

    if not os.path.exists(data_dir):
        logger.warning("Thư mục dữ liệu '%s' chưa tồn tại.", data_dir)
        return extracted_data

    for filename in REQUIRED_FILES:
        entity_name = os.path.splitext(filename)[0]
        filepath = os.path.join(data_dir, filename)

        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath, encoding="utf-8")
                extracted_data[entity_name] = df
                logger.info(
                    "Đã trích xuất '%s' thành công: %d dòng, %d cột.",
                    entity_name,
                    len(df),
                    len(df.columns),
                )
            except Exception as e:
                logger.error("Lỗi khi đọc file '%s': %s", filepath, str(e))
                raise
        else:
            logger.warning(
                "Tệp dữ liệu mẫu '%s' không tồn tại tại '%s'.", filename, data_dir
            )

    return extracted_data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = extract_data()
    for name, df in data.items():
        print(f"Loaded {name}: {len(df)} records")
