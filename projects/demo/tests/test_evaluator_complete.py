#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整测试Evaluator使用markdown格式的流程
"""

from model import Evaluator
from question_bank import get_question_bank


def test_complete_flow():
    """测试完整流程"""
    print("=" * 60)
    print("完整测试：Evaluator使用Markdown格式")
    print("=" * 60)

    # 1. 验证题库中有题目
    print("\n1. 验证题库:")
    print("-" * 60)
    bank = get_question_bank()
    question = bank.get_question("44")
    if question:
        print(f"✓ 题目44存在")
        print(f"  - 教师: {question.teacher}")
        print(f"  - 学生数: {len(question.students)}")
        md_str = question.to_markdown_string()
        print(f"  - Markdown字符串长度: {len(md_str)} 字符")
    else:
        print("✗ 题目44不存在")
        return

    # 2. 测试Evaluator初始化
    print("\n2. 测试Evaluator初始化:")
    print("-" * 60)
    try:
        evaluator = Evaluator(question_id="44")
        print("✓ Evaluator初始化成功")
        print(f"  - question_id: {evaluator.question_id}")
        print(
            f"  - question_markdown存在: {hasattr(evaluator, 'question_markdown') and evaluator.question_markdown is not None}"
        )
        if evaluator.question_markdown:
            print(f"  - question_markdown长度: {len(evaluator.question_markdown)} 字符")
    except Exception as e:
        print(f"✗ Evaluator初始化失败: {e}")
        return

    # 3. 测试生成prompt
    print("\n3. 测试生成Prompt:")
    print("-" * 60)
    test_answer = "I believe the biggest mistake people make when buying tech products is not researching enough before purchasing."
    prompt = evaluator.generate_prompt(test_answer)

    print(f"✓ Prompt生成成功")
    print(f"  - Prompt消息数: {len(prompt)}")
    print(f"  - System消息: {len([m for m in prompt if m['role'] == 'system'])}")
    print(f"  - User消息: {len([m for m in prompt if m['role'] == 'user'])}")
    print(
        f"  - Assistant消息（few-shot）: {len([m for m in prompt if m['role'] == 'assistant'])}"
    )

    # 检查最后的user消息是否使用了markdown格式
    last_user_msg = [m for m in prompt if m["role"] == "user"][-1]
    user_content = last_user_msg["content"]

    print(f"\n最后的User消息内容预览:")
    print("-" * 60)
    print(user_content[:400] + "...")

    # 验证markdown格式
    has_instruction = "**Instruction:**" in user_content
    has_professor = "**Professor" in user_content
    has_student = "**Student" in user_content
    has_response_section = "**[Student's Response to Evaluate]**" in user_content

    print(f"\n格式验证:")
    print(
        f"  - 包含Instruction: {has_instruction} ✓"
        if has_instruction
        else f"  - 包含Instruction: {has_instruction} ✗"
    )
    print(
        f"  - 包含Professor: {has_professor} ✓"
        if has_professor
        else f"  - 包含Professor: {has_professor} ✗"
    )
    print(
        f"  - 包含Student: {has_student} ✓"
        if has_student
        else f"  - 包含Student: {has_student} ✗"
    )
    print(
        f"  - 包含Response部分: {has_response_section} ✓"
        if has_response_section
        else f"  - 包含Response部分: {has_response_section} ✗"
    )

    if has_instruction and has_professor and has_student and has_response_section:
        print("\n✓ 所有格式验证通过！")
    else:
        print("\n✗ 格式验证失败")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_complete_flow()
