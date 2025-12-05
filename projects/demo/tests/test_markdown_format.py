#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试markdown格式功能
"""

from question_bank import get_question_bank


def test_markdown_format():
    """测试markdown格式功能"""
    print("=" * 60)
    print("测试Markdown格式功能")
    print("=" * 60)

    bank = get_question_bank()
    question = bank.get_question("44")

    if not question:
        print("题目不存在")
        return

    print("\n1. 测试 to_markdown_format() - 字典格式:")
    print("-" * 60)
    md_dict = question.to_markdown_format()
    print(f"Instruction: {md_dict['instruction'][:80]}...")
    print(f"\nTeacher: {md_dict['teacher'][:100]}...")
    print(f"\nStudents ({len(md_dict['students'])}个):")
    for i, student in enumerate(md_dict["students"], 1):
        print(f"  {i}. {student[:80]}...")

    print("\n\n2. 测试 to_markdown_string() - 完整字符串格式:")
    print("-" * 60)
    md_str = question.to_markdown_string()
    print(md_str[:500] + "...")

    print("\n\n3. 测试 get_question_markdown() - 通过QuestionBank获取:")
    print("-" * 60)
    md_dict_result = bank.get_question_markdown("44", as_string=False)
    print(f"Teacher: {md_dict_result['teacher'][:100]}...")

    md_str_result = bank.get_question_markdown("44", as_string=True)
    print(f"\n完整字符串长度: {len(md_str_result)} 字符")
    print(md_str_result)

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_markdown_format()
