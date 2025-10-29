from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # ✅ Load signals for profile creation and department mapping
        import accounts.signals
        logger.info("✅ accounts.signals loaded in AppConfig")




