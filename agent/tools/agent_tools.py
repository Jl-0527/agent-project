# encoding:utf-8
import os.path

from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
from utils.logger_hander import logger

rag = RagSummarizeService()
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
external_data = {}


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气，以字符串形式返回")
def get_weather(city: str) -> str:
    return f"{city}的天气的晴天小风，25度左右"


@tool(description="获取用户所在的城市，以字符串形式返回")
def get_user_location() -> str:
    return "用户所在的城市是阜阳"


@tool(description="获取用户的ID，以字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前的月份，以字符串形式返回")
def get_current_month() -> str:
    return "当前是2025年11月"


def get_external_data():
    """
    {
    "user_id":{
        "month":{"特征":"xxx","效率":"xxx"},
        "month":{"特征":"xxx","效率":"xxx"},
        "month":{"特征":"xxx","效率":"xxx"},
        ...
    },
    "user_id":{
        "month":{"特征":"xxx","效率":"xxx"},
        "month":{"特征":"xxx","效率":"xxx"},
        "month":{"特征":"xxx","效率":"xxx"},
        ...
    },
    "user_id":{
        "month":{"特征":"xxx","效率":"xxx"},
        "month":{"特征":"xxx","效率":"xxx"},
        "month":{"特征":"xxx","效率":"xxx"},
        ...
    },
    ...
    }
    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统获取指定用户在指定月份的使用记录，以字符串形式返回，如果检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    get_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录")
        return ""


@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已经调用"


if __name__ == '__main__':
    print(fetch_external_data("1004", "2025-11"))
