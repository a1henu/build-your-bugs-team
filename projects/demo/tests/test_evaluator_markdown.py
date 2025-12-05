#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Evaluator使用markdown格式
"""

from model import Evaluator


def test_evaluator_markdown():
    """测试Evaluator使用markdown格式"""
    print("=" * 60)
    print("测试Evaluator使用Markdown格式")
    print("=" * 60)

    # 测试使用question_id
    print("\n1. 使用question_id (44):")
    print("-" * 60)
    evaluator = Evaluator(question_id="44")
    test_answer = "This is a test answer for evaluation."
    prompt = evaluator.generate_prompt(test_answer)

    print("Prompt结构:")
    print(f"  System messages: {len([m for m in prompt if m['role'] == 'system'])}")
    print(f"  User messages: {len([m for m in prompt if m['role'] == 'user'])}")
    print(
        f"  Assistant messages (few-shot): {len([m for m in prompt if m['role'] == 'assistant'])}"
    )

    print("\n最后的User message内容:")
    print("-" * 60)
    user_content = prompt[-1]["content"]
    print(user_content)

    # 验证是否使用了markdown格式
    if "**Instruction:**" in user_content and "**Professor" in user_content:
        print("\n✓ 成功使用了markdown格式！")
    else:
        print("\n✗ 未使用markdown格式")

    # 测试使用question_file（兼容旧格式）
    print("\n\n2. 使用question_file (兼容旧格式):")
    print("-" * 60)
    try:
        evaluator_old = Evaluator(question_file="test.yaml")
        prompt_old = evaluator_old.generate_prompt(test_answer)
        user_content_old = prompt_old[-1]["content"]
        print("最后的User message内容（前300字符）:")
        print(user_content_old[:300] + "...")
        print("\n✓ 兼容旧格式正常工作")
    except FileNotFoundError:
        print("⚠ test.yaml文件不存在，跳过旧格式测试")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_evaluator_markdown()
