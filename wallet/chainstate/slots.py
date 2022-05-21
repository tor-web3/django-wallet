
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


from wallet.models import Address
from wallet.chainstate.models import State,RPC


@receiver(post_save, sender=Address)
def handle_post_save_address(sender, instance:Address, created:bool, **kwargs):
    """主动发现处于活跃的地址

    Args:
        sender (_type_): 发送本次消息的对象
        instance (Address): 对象实例
        created (bool): 是否为新增对象

    Raises:
        State.DoesNotExist: 该对象未在库中存档
    """
    rpc_obj = RPC.objects.filter(chain=instance.chain).first()
    # 地址有效刷新24小时
    now = timezone.now()
    end_time = now + timezone.timedelta(hours=24,minutes=0,seconds=0)
    
    # 更新地址状态机
    try:
        if created:
            raise State.DoesNotExist("not found")
        obj = State.objects.get(
            address=instance
        )
        obj.is_active = True
        obj.next_time = end_time
        obj.rpc = rpc_obj
        obj.save(update_fields=['is_active','end_time'])
    except State.DoesNotExist as e:
        obj = State.objects.create(
            address=instance,
            balance='',
            rpc=rpc_obj,
            stop_at=end_time,
        )