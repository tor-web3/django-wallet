from django.utils.translation import gettext_lazy as _


SUBMITTED="SUBMITTED"
AUDITED="AUDITED"
REJECT="REJECT"
WITHDRAWING="WITHDRAWING"
WITHDRAWN="WITHDRAWN"
ERROR="ERROR"
TRANSACTION_STATUS = (
    (SUBMITTED,_("submitted")), # 已提交
    (AUDITED,_("audited")), # 已审核
    (REJECT,_("reject")), # 已拒绝
    (WITHDRAWING,_("withdrawing")), # 提币中
    (WITHDRAWN,_("withdrawn")), # 已提币
    (ERROR,_("error")), # 错误
)

SELF="SELF"
BLOCKCHAIN_ORGAN = (
    (SELF, _("Tor")),
    ("HUOBI", _("Huobi Global Limited"))
)


MANUAL = "MANUAL"
ROBOT = "ROBOT"
AUDIT_MODE = (
    (MANUAL ,_("Manual")),
    (ROBOT ,_("Robot")),
)