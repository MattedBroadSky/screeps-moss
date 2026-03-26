#!/usr/bin/env python3
import os
import re
from pathlib import Path

def extract_scores_from_file(file_path):
    """从评审报告中提取评分信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    module_name = Path(file_path).stem.replace('_REVIEW', '')
    layer = Path(file_path).parent.name
    
    # 尝试多种模式匹配总分
    patterns = [
        r'总体评分[：:]\s*(\d+)/100',
        r'总体得分[：:]\s*(\d+)/100',
        r'总分[：:]\s*(\d+)/100',
        r'\*\*总计\*\*\s*\|\s*\*\*(\d+)/100\*\*',
        r'评分为(\d+)分',
        r'得分(\d+)分',
        r'得分为(\d+)分',
        r'总体评价.*得分为(\d+)分'
    ]
    
    total_score = None
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            total_score = int(match.group(1))
            break
    
    # 提取各维度分数
    dimension_scores = {}
    dimension_patterns = {
        '架构': r'架构符合性.*?(\d+)/20',
        '接口': r'接口规范性.*?(\d+)/20',
        '算法': r'算法合理性.*?(\d+)/20',
        '错误处理': r'错误处理.*?(\d+)/20',
        '文档': r'文档完整性.*?(\d+)/10',
        '可行性': r'实现可行性.*?(\d+)/10'
    }
    
    for dim, pattern in dimension_patterns.items():
        match = re.search(pattern, content)
        if match:
            dimension_scores[dim] = int(match.group(1))
    
    # 确定等级
    grade = "未知"
    if total_score:
        if total_score >= 90:
            grade = "✅ 优秀"
        elif total_score >= 70:
            grade = "⭐ 良好"
        elif total_score >= 60:
            grade = "⚠️ 合格"
        else:
            grade = "❌ 不合格"
    
    return {
        'module': module_name,
        'layer': layer,
        'total_score': total_score,
        'grade': grade,
        'dimension_scores': dimension_scores
    }

def main():
    base_dir = Path("docs/design/detailed/modules")
    review_files = list(base_dir.glob("*/*_REVIEW.md"))
    
    print("📊 模块评审得分汇总")
    print("=" * 50)
    
    all_scores = []
    for file_path in sorted(review_files):
        scores = extract_scores_from_file(file_path)
        all_scores.append(scores)
        
        if scores['total_score']:
            print(f"{scores['module']:20} ({scores['layer']:10}): {scores['total_score']:3}/100 {scores['grade']}")
        else:
            print(f"{scores['module']:20} ({scores['layer']:10}): 评分未找到")
    
    # 计算平均分
    valid_scores = [s['total_score'] for s in all_scores if s['total_score']]
    if valid_scores:
        avg_score = sum(valid_scores) / len(valid_scores)
        print(f"\n📈 平均分: {avg_score:.1f}/100")
        
        # 等级分布
        grade_counts = {
            "✅ 优秀": 0,
            "⭐ 良好": 0,
            "⚠️ 合格": 0,
            "❌ 不合格": 0
        }
        
        for s in all_scores:
            if s['grade'] in grade_counts:
                grade_counts[s['grade']] += 1
        
        print("\n📋 等级分布:")
        for grade, count in grade_counts.items():
            if count > 0:
                print(f"  {grade}: {count}个模块")

if __name__ == "__main__":
    main()