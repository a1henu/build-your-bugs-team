#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题库功能测试脚本
"""

from question_bank import get_question_bank
from model import Evaluator


def test_question_bank():
    """测试题库功能"""
    print("=" * 50)
    print("测试题库功能")
    print("=" * 50)

    # 获取题库实例
    bank = get_question_bank()

    # 测试统计信息
    print("\n1. 获取统计信息:")
    stats = bank.get_statistics()
    print(f"   总数: {stats['total']}")
    print(f"   有效: {stats['valid']}")
    print(f"   无效: {stats['invalid']}")

    # 测试获取题目列表
    print("\n2. 获取题目列表（前5个有效题目）:")
    questions, total = bank.get_question_list(only_valid=True, limit=5)
    print(f"   总数: {total}")
    for q in questions:
        print(f"   - ID: {q['id']}, 教师: {q['teacher']}, 学生数: {q['student_count']}")

    # 测试获取单个题目
    print("\n3. 获取单个题目（ID=44）:")
    question = bank.get_question("44", only_valid=True)
    if question:
        print(f"   ID: {question.id}")
        print(f"   教师: {question.teacher}")
        print(f"   学生数: {len(question.students)}")
        print(f"   是否有效: {question.is_valid}")
    else:
        print("   题目不存在或无效")

    # 测试无效题目
    print("\n4. 测试无效题目（ID=51）:")
    question = bank.get_question("51", only_valid=True)
    if question:
        print(f"   题目存在: {question.id}")
    else:
        print("   题目不存在或无效（符合预期）")

    # 测试Evaluator使用question_id
    print("\n5. 测试Evaluator使用question_id:")
    try:
        evaluator = Evaluator(question_id="44")
        print(f"   ✓ Evaluator初始化成功")
        print(f"   Instruction长度: {len(evaluator.instruction)}")
        print(f"   Teacher长度: {len(evaluator.teacher)}")
        print(f"   Students数量: {len(evaluator.students)}")
    except Exception as e:
        print(f"   ✗ Evaluator初始化失败: {e}")

    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    test_question_bank()
