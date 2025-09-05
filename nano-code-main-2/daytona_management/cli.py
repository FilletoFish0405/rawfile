import sys
from .proxy import NanoCodeProxy

def parse_arguments() -> dict:
    """解析命令行参数"""
    # 需要两个参数：JSON文件路径 和 uploadfolder 目录
    if len(sys.argv) < 3:
        return {"show_help": True}
    
    # 获取JSON文件路径
    json_file_path = sys.argv[1]
    
    # 第二个参数为需要上传的本地文件夹（uploadfolder）
    uploadfolder = sys.argv[2]
    
    return {
        "json_file_path": json_file_path,
        "uploadfolder": uploadfolder,
        "show_help": False
    }


def main():
    """主入口函数"""
    try:
        args = parse_arguments()
        if args.get("show_help"):
            print("Usage: python -m daytona_management.cli <json_file_path> <uploadfolder>")
            sys.exit(2)
        
        proxy = NanoCodeProxy()
        proxy.setup_daytona()
        
        print("=" * 60)
        print("🎯 nano-code JSON任务执行")
        print(f"📋 JSON文件路径: {args['json_file_path']}")
        if args.get("uploadfolder"):
            print(f"🗂️  外部资源上传目录: {args['uploadfolder']}")
        print("=" * 60)
        
        proxy.start_nano_code_json(args["json_file_path"], args.get("uploadfolder")) 
        
    except KeyboardInterrupt:
        print("\n👋 程序被中断")
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
