import json
from pathlib import Path
from typing import Union, Optional

from .proxy import NanoCodeProxy
from nanocode1.models.dissertation_plan import DissertationPlan
from nanocode1.models.output_format import ReportModel


def _extract_json_from_output(output: str) -> Optional[dict]:
    """从混杂输出中提取最后一个JSON对象并解析为dict。"""
    if not output:
        return None
    output = output.strip()
    # 先尝试直接解析
    try:
        return json.loads(output)
    except Exception:
        pass
    # 回退：从最后一个'{'开始尝试
    last_brace = output.rfind('{')
    if last_brace != -1:
        candidate = output[last_brace:]
        try:
            return json.loads(candidate)
        except Exception:
            pass
    return None


def generate_report(plan_json_path: str, uploadfolder: str) -> Union[ReportModel, DissertationPlan, dict]:
    """
    在Daytona容器中运行 Coding_agent.generate_report，并返回结果。

    Args:
        plan_json_path: 本地计划JSON路径
        uploadfolder:   本地外部资源根目录（整体上传到 /workspace/tmp）

    Returns:
        ReportModel 或 DissertationPlan（若无法解析为模型则返回dict）
    """
    proxy = NanoCodeProxy()
    proxy.setup_daytona()

    print("=" * 60)
    print(f"📋 计划文件: {plan_json_path}")
    print(f"🗂️  外部资源: {uploadfolder}")
    print("=" * 60)

    # 会话
    base_stage = proxy._infer_stage_from_plan(plan_json_path)
    session_id = proxy.workspace_manager.ensure_session(base_stage)
    proxy.workspace_manager.setup_secure_workspace(session_id)

    # 上传工作区与重写JSON
    proxy.file_transfer.upload_workspace_dir(uploadfolder)
    json_remote_path = proxy.file_transfer.process_json_and_rewrite_by_workspace(
        plan_json_path, workspace_local_dir=uploadfolder
    )

    # 执行
    result = proxy.task_executor.execute_json_task(session_id, json_remote_path)

    # 收集输出
    json_filename = Path(plan_json_path).name
    proxy.file_transfer.collect_output_files(session_id, [json_filename], copy=True)
    proxy.file_transfer.download_results(session_id)

    # 解析stdout中的JSON结果
    payload = _extract_json_from_output(result.output or "") if result else None
    if not payload:
        return {}

    # 尝试解析为模型
    try:
        if 'is_finish' in payload and 'report' in payload:
            return ReportModel(**payload)
        if 'is_first_time' in payload and 'experimental_requirements' in payload:
            return DissertationPlan(**payload)
    except Exception:
        pass
    return payload

