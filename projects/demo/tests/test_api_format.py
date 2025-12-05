#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试API返回格式
"""

import json
from question_bank import get_question_bank


def test_api_format():
    """测试API返回格式"""
    print("=" * 60)
    print("测试API返回格式")
    print("=" * 60)

    bank = get_question_bank()
    questions, total = bank.get_question_list(only_valid=True, limit=5)

    # 模拟API返回格式
    files = [q["id"] for q in questions]
    result = {"files": files}

    print("\n返回格式:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print(f"\n验证:")
    print(f"  - files是列表: {isinstance(result['files'], list)}")
    print(f"  - files长度: {len(result['files'])}")
    print(f"  - files元素类型: {[type(f).__name__ for f in result['files']]}")
    print(f"  - files内容: {result['files']}")

    # 验证是否符合前端期望
    if isinstance(result.get("files"), list) and all(
        isinstance(f, str) for f in result["files"]
    ):
        print("\n✓ 格式符合前端期望！")
    else:
        print("\n✗ 格式不符合前端期望")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_api_format()
