from openai import OpenAI

def _get_client(api_key: str):
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

# 单选, 多选题
def deepseek_choice(api_key: str, question: str, options: list):
    """
    使用 DeepSeek 解单选/多选题，要求 AI 严格返回 A/B/C/D 或 A,C
    options: [("A", "内容1"), ("B", "内容2"), ...]
    """

    client = _get_client(api_key)

    options_text = "\n".join([f"{label}. {text}" for label, text in options])

    prompt = f"""
你是一名专业的考试答题机器人。

规则：
1. 单选题只能输出 A/B/C/D 之一。
2. 多选题可以输出多个字母，例如：A,C。
3. 不允许输出解释。
4. 不允许输出选项内容。
5. 不允许出现“答案是”“正确答案”“理由”等字样。

题目：
{question}

选项：
{options_text}

请只返回选项序号，不要返回其它内容。
"""

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    answer = resp.choices[0].message.content.strip().upper()

    # 规范化：强制提取 ABCD 字母
    valid = [ch for ch in answer if ch in "ABCD"]

    if not valid:
        return "A"  # fallback

    return ",".join(valid) if len(valid) > 1 else valid[0]


# 简答题（3–6 句的文字）
def deepseek_answer_text(api_key: str, question: str):
    client = _get_client(api_key)

    prompt = f"""
请根据下面的简答题，生成一个清晰、简洁、准确的回答。

要求：
- 不要重复题目
- 不要输出“好的，我来回答”等废话
- 长度控制为 3~6 句话
- 回答要有逻辑性，直击重点

题目：
{question}
"""

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    return resp.choices[0].message.content.strip()


# 填空题
def deepseek_answer_blank(api_key: str, question: str):
    """
    填空题：要求返回非常短的答案（一般是名词、符号、术语）。
    """
    client = _get_client(api_key)

    prompt = f"""
请根据下面的填空题，返回最简短、最精确的答案。

严格要求：
- 只能输出答案本身（1~6 个字）
- 不允许输出任何解释
- 不允许包含句号、空格
- 不要重复题目内容

题目：
{question}
"""

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    answer = resp.choices[0].message.content.strip()

    # 去掉空格和标点
    return "".join(ch for ch in answer if ch.isalnum() or ch in "→-<>△▲")


# 对外暴露统一接口
__all__ = [
    "deepseek_choice",
    "deepseek_answer_text",
    "deepseek_answer_blank"
]