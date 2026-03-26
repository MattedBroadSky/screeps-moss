#!/bin/bash

echo "模块评审得分汇总："
echo "=================="

for review_file in docs/design/detailed/modules/*/*_REVIEW.md; do
    module_name=$(basename "$review_file" "_REVIEW.md")
    layer=$(dirname "$review_file" | xargs basename)
    
    # 提取评分
    score=$(grep -o "总体评分.*[0-9]\+/[0-9]\+" "$review_file" | head -1 | grep -o "[0-9]\+/[0-9]\+" || \
            grep -o "总体得分.*[0-9]\+/[0-9]\+" "$review_file" | head -1 | grep -o "[0-9]\+/[0-9]\+" || \
            grep -o "总分.*[0-9]\+/[0-9]\+" "$review_file" | head -1 | grep -o "[0-9]\+/[0-9]\+" || \
            echo "未找到")
    
    # 提取等级
    grade=$(grep -o "评级.*[✅⭐⚠️❌]" "$review_file" | head -1 | grep -o "[✅⭐⚠️❌]" || \
            grep -o "等级.*[✅⭐⚠️❌]" "$review_file" | head -1 | grep -o "[✅⭐⚠️❌]" || \
            echo "未找到")
    
    echo "$module_name ($layer): $score $grade"
done