from enum import Enum

class URLNames(str, Enum):
    # Custom
    MAIN_PAGE = "main_page"
    CART_PAGE = "cart_page"
    CATALOG_PAGE = "catalog_page"
    ORDER_PAGE = "order_page"
    PRODUCT_DETAIL_PAGE = "product_detail_page"
    ACTION_ADD_TO_CART = "action_add_to_cart"
    ACTION_UPDATE_CART_ITEM = "update_cart_item"
    ACTION_REMOVE_CART_ITEM = "remove_cart_item"

    # allauth: account
    ACCOUNT_LOGIN = "account_login"
    ACCOUNT_LOGOUT = "account_logout"
    ACCOUNT_SIGNUP = "account_signup"

    ACCOUNT_EMAIL = "account_email"
    ACCOUNT_CONFIRM_EMAIL = "account_confirm_email"

    ACCOUNT_CHANGE_PASSWORD = "account_change_password"
    ACCOUNT_SET_PASSWORD = "account_set_password"
    ACCOUNT_RESET_PASSWORD = "account_reset_password"
    ACCOUNT_RESET_PASSWORD_DONE = "account_reset_password_done"
    ACCOUNT_RESET_PASSWORD_FROM_KEY = "account_reset_password_from_key"
    ACCOUNT_RESET_PASSWORD_FROM_KEY_DONE = "account_reset_password_from_key_done"

    ACCOUNT_INACTIVE = "account_inactive"
    ACCOUNT_SIGNUP_CLOSED = "account_signup_closed"
    ACCOUNT_EMAIL_VERIFICATION_SENT = "account_email_verification_sent"

    # allauth: socialaccount
    SOCIALACCOUNT_CONNECTIONS = "socialaccount_connections"
    SOCIALACCOUNT_SIGNUP = "socialaccount_signup"
