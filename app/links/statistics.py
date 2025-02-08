def get_user_agent(request_meta_data):
    return request_meta_data.get("HTTP_USER_AGENT", "")


def get_client_ip(request_meta_data):
    if x_forwarded_for := request_meta_data.get("HTTP_X_FORWARDED_FOR"):
        return x_forwarded_for.split(",")[0]
    return request_meta_data.get("REMOTE_ADDR", "")
