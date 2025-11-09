from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup

from python.tools.abc.LlmFunctionTool import LlmFunctionTool, FunctionInfo


FUNCTION_NAME: str = "web_search_duckduckgo"
FUNCTION_DESCRIPTION: str = """
使用DuckDuckGo搜索引擎从互联网搜索最新信息，包括新闻、知识、实时数据等。当用户询问需要最新信息、实时数据、新闻事件、未知知识或需要验证的信息时使用此功能。
"""


class DuckduckgoWebSearch(LlmFunctionTool):
    """
    互联网搜索工具
    """

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def get_tool_info(self) -> FunctionInfo:
        return FunctionInfo(FUNCTION_NAME, FUNCTION_DESCRIPTION, {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词或问题，要具体明确。例如：'2024年最新AI技术进展'、'今天北京天气'、'Python最新版本特性"
                },
                "search_type": {
                    "type": "string",
                    "enum": ["general", "news", "academic"],
                    "description": "搜索类型：general-综合搜索, news-新闻搜索, academic-学术搜索",
                    "default": "general"
                },
                "max_results": {
                    "type": "number",
                    "description": "返回的最大结果数量",
                    "default": 5
                }
            },
            "required": ["query"],
        })

    def execute(self, params: dict) -> str:
        query: str = params.get("query", "")
        if query is None or len(query) <= 0:
            return "查询失败，请输入正确的查询关键词！"
        search_type: str = params.get("search_type", "general")
        if search_type not in ["general", "news", "academic"]:
            search_type = "general"
        max_results: int = int(params.get("max_results", 5))
        return self.web_search(query, search_type, max_results)

    def web_search(self, query: str, search_type: str = "general", max_results: int = 5) -> str:
        """
        网络搜索功能 - 供模型调用的接口
        """
        print(f"🔍 正在搜索: {query} (类型: {search_type})")

        # 根据搜索类型调整查询（可选）
        if search_type == "news":
            query = f"{query} 最新新闻"
        elif search_type == "academic":
            query = f"{query} 学术论文 研究"

        results = self.duckduckgo_search(query, max_results)
        return self.format_search_results(results)

    def duckduckgo_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        使用 DuckDuckGo 搜索（免费，无需API Key）
        返回格式参考业界标准
        """
        try:
            # 使用 DuckDuckGo 的HTML接口
            url = "https://html.duckduckgo.com/html/"
            params = {
                "q": query,
                "kl": "wt-wt"  # 地区设置为无偏好
            }

            response = self.session.post(url, data=params, timeout=10)
            response.raise_for_status()

            # 解析搜索结果（简化版）
            soup = BeautifulSoup(response.text, "html.parser")

            results = []
            for result in soup.select(".result__body")[:max_results]:
                try:
                    title_elem = result.select_one(".result__title")
                    snippet_elem = result.select_one(".result__snippet")
                    link_elem = result.select_one(".result__url")

                    if title_elem and snippet_elem:
                        title = title_elem.get_text(strip=True)
                        snippet = snippet_elem.get_text(strip=True)
                        link = link_elem.get("href") if link_elem else "N/A"

                        # 清理链接
                        if link and link.startswith("//"):
                            link = "https:" + link

                        results.append({
                            "title": title,
                            "snippet": snippet,
                            "link": link,
                            "source": "DuckDuckGo"
                        })
                except Exception as e:
                    continue

            return results

        except Exception as e:
            return [{
                "title": "搜索失败",
                "snippet": f"搜索过程中出现错误: {str(e)}",
                "link": "N/A",
                "source": "Error"
            }]

    def format_search_results(self, results: List[Dict]) -> str:
        """
        将搜索结果格式化为模型易读的字符串
        参考业界标准格式
        """
        if not results:
            return "未找到相关搜索结果。"

        formatted_lines = ["🔍 搜索结果显示:"]

        for i, result in enumerate(results, 1):
            formatted_lines.append(f"\n{i}. **{result["title"]}**")
            formatted_lines.append(f"   📄 {result["snippet"]}")
            formatted_lines.append(f"   🔗 {result["link"]}")
            formatted_lines.append(f"   📍 来源: {result["source"]}")

        # 添加总结信息
        formatted_lines.append(f"\n--- 共找到 {len(results)} 个相关结果 ---")

        return "\n".join(formatted_lines)


# 搜索功能主函数
if __name__ == "__main__":
    print(DuckduckgoWebSearch().web_search("哈基咪娜美鲁多南北绿豆", "general", 5))
