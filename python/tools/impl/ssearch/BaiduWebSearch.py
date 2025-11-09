import re
from typing import List, Dict, Any
from urllib.parse import quote, unquote

import chardet
import requests

from python.tools.abc.LlmFunctionTool import LlmFunctionTool, FunctionInfo

FUNCTION_NAME: str = "web_search_baidu"
FUNCTION_DESCRIPTION: str = """
使用百度搜索引擎从互联网搜索最新信息，包括新闻、知识、实时数据等。当用户询问需要最新信息、实时数据、新闻事件、未知知识或需要验证的信息时使用此功能。
"""


class BaiduWebSearch(LlmFunctionTool):
    """
    互联网搜索工具
    """

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        })

    def get_tool_info(self) -> FunctionInfo:
        return FunctionInfo(FUNCTION_NAME, FUNCTION_DESCRIPTION, {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词或问题，要具体明确。例如：'2024年最新AI技术进展'、'今天北京天气'、'Python最新版本特性'"
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
        return self.web_search(params["query"], params.get("search_type", "general"), params.get("max_results", 5))

    def web_search(self, query: str, search_type: str = "general", max_results: int = 5) -> str:
        """
        网络搜索功能 - 供模型调用的接口
        """
        print(f"🔍 正在搜索: {query} (类型: {search_type})")

        # 根据搜索类型调整查询
        if search_type == "news":
            query = f"{query} 最新新闻"
        elif search_type == "academic":
            query = f"{query} 学术论文 研究"

        results = self.baidu_search(query, max_results)
        return self.format_search_results(results, query)

    def baidu_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        使用百度进行搜索 - 更新版解析
        """
        try:
            # 编码查询参数
            encoded_query = quote(query)
            url = f"https://www.baidu.com/s?ie=utf-8&tn=baidu&wd={encoded_query}&rqlang=cn"

            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            # response.encoding = 'utf-8'


            # ####################
            current_charset = chardet.detect(response.content)
            # ####################


            # 解析搜索结果
            return self.parse_baidu_results_v2(response.text, max_results)

        except Exception as e:
            print(f"百度搜索错误: {e}")
            return [{
                'title': '搜索失败',
                'snippet': f'百度搜索过程中出现错误: {str(e)}',
                'link': 'N/A',
                'source': 'Baidu Error'
            }]

    def parse_baidu_results_v2(self, html: str, max_results: int) -> List[Dict[str, Any]]:
        """
        新版百度搜索结果解析
        """
        results = []

        try:
            # 方法1：尝试新的CSS选择器模式
            # 百度现在的结构更复杂，我们尝试多种匹配方式

            # 匹配包含结果的容器
            result_blocks = re.findall(r'<div class="result[^"]*"[^>]*>.*?</div><!--s-result-->', html, re.DOTALL)

            if not result_blocks:
                # 方法2：尝试匹配标题和描述
                result_blocks = re.findall(r'<h3[^>]*>.*?</h3>.*?<div[^>]*class="[^"]*c-abstract[^"]*"[^>]*>.*?</div>',
                                           html, re.DOTALL)

            print(f"找到 {len(result_blocks)} 个结果块")

            for i, block in enumerate(result_blocks[:max_results]):
                try:
                    # 提取标题
                    title_match = re.search(r'<h3[^>]*>\s*<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', block, re.DOTALL)
                    if not title_match:
                        continue

                    link = title_match.group(1)
                    title_html = title_match.group(2)

                    # 清理标题
                    title = re.sub(r'<[^>]+>', '', title_html).strip()
                    title = re.sub(r'\s+', ' ', title)  # 合并多余空格

                    # 提取描述
                    desc_match = re.search(r'<div[^>]*class="[^"]*c-abstract[^"]*"[^>]*>(.*?)</div>', block, re.DOTALL)
                    snippet = ""
                    if desc_match:
                        snippet = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
                        snippet = re.sub(r'\s+', ' ', snippet)

                    # 处理百度跳转链接
                    real_link = self.resolve_baidu_link(link)

                    results.append({
                        'title': title or '无标题',
                        'snippet': snippet or '暂无描述',
                        'link': real_link,
                        'source': '百度搜索'
                    })

                    print(f"✅ 解析到结果 {i + 1}: {title}")

                except Exception as e:
                    print(f"解析单个结果失败: {e}")
                    continue

        except Exception as e:
            print(f"解析百度页面失败: {e}")

        # 如果还是没解析到结果，使用备用方案
        if not results:
            results = self.fallback_parse(html, max_results)

        return results

    def fallback_parse(self, html: str, max_results: int) -> List[Dict[str, Any]]:
        """
        备用解析方案 - 更宽松的匹配
        """
        results = []

        try:
            # 宽松匹配所有链接和文本
            links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)

            for link, title_html in links[:max_results * 3]:  # 多取一些进行筛选
                try:
                    # 过滤掉百度自己的链接
                    if 'baidu.com' in link and 'link?url=' not in link:
                        continue

                    title = re.sub(r'<[^>]+>', '', title_html).strip()
                    if len(title) < 10 or len(title) > 100:  # 过滤太短或太长的标题
                        continue

                    # 简单的关键词过滤
                    if any(word in title.lower() for word in ['百度', '设置', '登录', '下载', '首页']):
                        continue

                    real_link = self.resolve_baidu_link(link)

                    results.append({
                        'title': title,
                        'snippet': '点击链接查看详情',
                        'link': real_link,
                        'source': '百度搜索'
                    })

                    if len(results) >= max_results:
                        break

                except Exception:
                    continue

        except Exception as e:
            print(f"备用解析也失败: {e}")

        # 如果所有方法都失败，返回模拟数据
        if not results:
            results = [{
                'title': '解析失败，返回模拟结果',
                'snippet': '由于百度页面结构变化，无法正确解析搜索结果。建议：1. 检查网络 2. 使用其他关键词 3. 稍后重试',
                'link': 'https://www.baidu.com',
                'source': '系统提示'
            }]

        return results

    def resolve_baidu_link(self, link: str) -> str:
        """
        解析百度跳转链接
        """
        if link.startswith('http://www.baidu.com/link?url=') or link.startswith('https://www.baidu.com/link?url='):
            try:
                # 从链接中提取真实URL
                match = re.search(r'url=([^&]*)', link)
                if match:
                    encoded_url = match.group(1)
                    real_url = unquote(encoded_url)
                    return real_url
            except:
                pass
        return link

    def format_search_results(self, results: List[Dict], query: str) -> str:
        """
        格式化百度搜索结果
        """
        if not results:
            return f"在百度中未找到与\"{query}\"相关的搜索结果。"

        formatted_lines = [f"🔍 **百度搜索结果** - 查询: \"{query}\""]
        formatted_lines.append(f"📊 找到 {len(results)} 个相关结果\n")

        for i, result in enumerate(results, 1):
            formatted_lines.append(f"**{i}. {result['title']}**")
            formatted_lines.append(f"   📄 {result['snippet']}")
            formatted_lines.append(f"   🔗 {result['link']}")
            formatted_lines.append(f"   📍 来源: {result['source']}")
            formatted_lines.append("")

        formatted_lines.append("--- 搜索完成 ---")

        return "\n".join(formatted_lines)


# 测试函数
def debug_baidu_search():
    """调试百度搜索"""
    searcher = BaiduWebSearch()

    # 测试多个查询
    test_queries = [
        "人工智能",
        "Python编程",
        "今天的天气",
        "哈基咪娜美鲁多"
    ]

    for query in test_queries:
        print(f"\n{'=' * 50}")
        print(f"测试查询: {query}")
        print(f"{'=' * 50}")

        try:
            result = searcher.web_search(query, "general", 3)
            print(result)
        except Exception as e:
            print(f"❌ 搜索失败: {e}")


if __name__ == "__main__":
    debug_baidu_search()