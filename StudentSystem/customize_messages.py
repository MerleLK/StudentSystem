from django.contrib import messages

# 自定义一个消息


def flash(request, title, text, level='info'):

    """
    使用django的message系统发送一个消息
    :param request: 当前请求的对象
    :param title: 标题
    :param text: 内容
    :param level: 等级
    :return: 返回值
    """

    level_map = {
        'info': messages.INFO,
        'debug': messages.DEBUG,
        'success': messages.SUCCESS,
        'warning': messages.WARNING,
        'error': messages.ERROR
    }

    try:
        level = level_map[level]

        messages.add_message(request, level, text, extra_tags=title)

        return True
    except KeyError:
        return False
