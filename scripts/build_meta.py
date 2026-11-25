# -*- coding: utf-8 -*-
"""各 generator 共用嘅 build 中繼資料：cache-busting 版本字串單一來源。"""
from __future__ import annotations

from datetime import datetime


def ver() -> str:
    """Build 時間戳（YYYYMMDDHHMM）。行為有變自動 bump，唔使人手改。"""
    return datetime.now().strftime("%Y%m%d%H%M")
