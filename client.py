# -*- coding: utf-8 -*-

import json
import urllib.error
import urllib.request


def normalize_chat_url(base_url):
    base_url = str(base_url or "").strip().rstrip("/")
    if not base_url:
        raise RuntimeError("缺少接口 URL")
    if base_url.endswith("/chat/completions"):
        return base_url
    return base_url + "/chat/completions"


def _content_to_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                value = item.get("text") or item.get("content") or ""
                if isinstance(value, dict):
                    value = value.get("value") or ""
                if value:
                    parts.append(str(value))
        return "".join(parts)
    return "" if content is None else str(content)


def extract_reply_text(data):
    if isinstance(data, dict):
        output_text = data.get("output_text")
        if output_text:
            return str(output_text).strip()
        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            choice = choices[0] or {}
            message = choice.get("message") or choice.get("delta") or {}
            if isinstance(message, dict):
                text = _content_to_text(message.get("content")).strip()
                if text:
                    return text
            text = _content_to_text(choice.get("text")).strip()
            if text:
                return text
    raise RuntimeError("无法从接口响应中读取回复文本")


def request_json(url, payload, headers, timeout):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "ignore")
        raise RuntimeError("HTTP %s: %s" % (exc.code, raw[:800]))
    except urllib.error.URLError as exc:
        raise RuntimeError("网络连接失败：%s" % exc)

    try:
        return json.loads(raw)
    except Exception:
        raise RuntimeError("接口返回的不是 JSON：%s" % raw[:800])


def request_openai_compatible(api, messages):
    url = normalize_chat_url(api.get("base_url"))
    payload = {
        "model": api.get("model"),
        "messages": messages,
        "temperature": api.get("temperature", 0.7),
        "max_tokens": api.get("max_tokens", 3000),
    }
    extra_body = api.get("extra_body") or {}
    if isinstance(extra_body, dict):
        payload.update(extra_body)

    headers = {"Content-Type": "application/json"}
    api_key = str(api.get("api_key") or "").strip()
    if api_key:
        headers["Authorization"] = "Bearer %s" % api_key
    organization = str(api.get("organization") or "").strip()
    if organization:
        headers["OpenAI-Organization"] = organization
    extra_headers = api.get("extra_headers") or {}
    if isinstance(extra_headers, dict):
        for key, value in extra_headers.items():
            key = str(key or "").strip()
            if key:
                headers[key] = str(value)

    data = request_json(url, payload, headers, int(api.get("timeout_seconds", 60)))
    return extract_reply_text(data)


def request_openai_compatible_vision(api, prompt, image_urls):
    url = normalize_chat_url(api.get("base_url"))
    content = [{"type": "text", "text": str(prompt or "")}]
    for image_url in image_urls or []:
        image_url = str(image_url or "").strip()
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})

    payload = {
        "model": api.get("model"),
        "messages": [{"role": "user", "content": content}],
        "temperature": api.get("temperature", 0.2),
        "max_tokens": api.get("max_tokens", 700),
    }
    extra_body = api.get("extra_body") or {}
    if isinstance(extra_body, dict):
        payload.update(extra_body)

    headers = {"Content-Type": "application/json"}
    api_key = str(api.get("api_key") or "").strip()
    if api_key:
        headers["Authorization"] = "Bearer %s" % api_key
    organization = str(api.get("organization") or "").strip()
    if organization:
        headers["OpenAI-Organization"] = organization
    extra_headers = api.get("extra_headers") or {}
    if isinstance(extra_headers, dict):
        for key, value in extra_headers.items():
            key = str(key or "").strip()
            if key:
                headers[key] = str(value)

    data = request_json(url, payload, headers, int(api.get("timeout_seconds", 45)))
    return extract_reply_text(data)
