import os

# 项目根目录（固定为你的路径）
ROOT_DIR = "/root/quant-factory-os"
# 输出文件路径（整合后的文件）
OUTPUT_FILE = "/root/quant-factory-os/project_all_files.txt"

# 需要排除的文件规则
EXCLUDE_FILE_PATTERNS = [
    "__init__.py",          # 排除所有__init__.py
    "Copy1",                # 排除含Copy1的文件
    "Copy2",                # 排除含Copy2的文件
    "write.py",
    ".pyc",
    ".png",                 # 排除png图片
 "githubcli.txt","project_all_files.txt","总纲清单（可复制）.md"
]

# 需要排除的目录规则（直接跳过这些目录的遍历）
EXCLUDE_DIR_PATTERNS = [
    "__pycache__",          # 排除所有__pycache__目录
    ".ipynb_checkpoints",   # 排除所有.ipynb_checkpoints目录
    ".git" ,                 # 排除.git目录
       ".pytest_cache"        # 新增：排除pytest缓存目录

]

def get_clean_directory_structure(root_dir):
    """生成清理后的目录结构字符串（排除指定目录和文件）"""
    structure = []
    structure.append(f"项目目录结构（{root_dir}）:")
    structure.append("="*50)
    
    for root, dirs, files in os.walk(root_dir):
        # 移除需要排除的目录（直接从dirs中删除，不会遍历这些目录）
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIR_PATTERNS]
        
        # 计算当前目录的缩进
        level = root.replace(root_dir, "").count(os.sep)
        indent = "    " * level
        # 写入目录名（排除根目录重复显示）
        if root != root_dir:
            dir_name = os.path.basename(root)
            structure.append(f"{indent}{dir_name}/")
        
        # 写入文件（排除规则内的文件）
        sub_indent = "    " * (level + 1)
        for file in files:
            # 跳过排除规则的文件
            if any(pattern in file for pattern in EXCLUDE_FILE_PATTERNS):
                continue
            structure.append(f"{sub_indent}{file}")
    
    return "\n".join(structure)

def read_file_content(file_path):
    """读取单个文件内容（处理编码异常）"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # 处理非UTF-8编码文件
        with open(file_path, "r", encoding="gbk", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"【读取失败】{str(e)}"

def main():
    # 新增：执行前先删除旧的输出文件（如果存在）
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"🗑️  已删除旧的输出文件: {OUTPUT_FILE}")
    
    # 1. 生成目录结构
    dir_structure = get_clean_directory_structure(ROOT_DIR)
    
    # 2. 遍历所有文件，收集符合条件的文件内容
    file_contents = []
    file_contents.append("\n\n" + "="*80)
    file_contents.append("所有目标文件内容:")
    file_contents.append("="*80 + "\n")
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # 跳过排除的目录（直接修改dirs，不遍历子目录）
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIR_PATTERNS]
        
        for file in files:
            # 跳过排除规则的文件
            if any(pattern in file for pattern in EXCLUDE_FILE_PATTERNS):
                continue
            
            file_path = os.path.abspath(os.path.join(root, file))
            # 写入文件绝对路径 + 内容
            file_contents.append(f"\n{'#'*60}")
            file_contents.append(f"文件路径: {file_path}")
            file_contents.append(f"{'#'*60}\n")
            file_contents.append(read_file_content(file_path))
    
    # 3. 写入最终文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # 开头写入输出文件的绝对路径
        f.write(f"整合文件绝对路径: {os.path.abspath(OUTPUT_FILE)}\n")
        # 写入目录结构
        f.write(dir_structure)
        # 写入文件内容
        f.write("\n".join(file_contents))
    
    print(f"✅ 操作完成！整合文件已保存至: {OUTPUT_FILE}")
    print(f"📄 该文件包含：")
    print(f"   - 清理后的项目目录结构（排除指定目录/文件）")
    print(f"   - 所有符合条件文件的完整内容")

if __name__ == "__main__":
    main()