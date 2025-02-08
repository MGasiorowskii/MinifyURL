from links.models import ClickLog, ShortURL


def log(request_meta_data: dict, short_link: ShortURL):
    ip_address = get_client_ip(request_meta_data)
    user_agent = request_meta_data.get("HTTP_USER_AGENT", "")
    ClickLog.objects.create(
        short_url=short_link, ip_address=ip_address, user_agent=user_agent
    )


def get_client_ip(request_meta_data):
    if x_forwarded_for := request_meta_data.get("HTTP_X_FORWARDED_FOR"):
        return x_forwarded_for.split(",")[0]
    return request_meta_data.get("REMOTE_ADDR")
