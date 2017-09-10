class WatersaverDatabaseRouter(object):
    """
    Determine how to route database calls for an app's models (in this case, for an app named Example).
    All other models will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on WaterSaver app models to `raspi`."""
        if model._meta.app_label == 'WaterSaver':
            return 'raspi'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on WaterSaver app models to `raspi`."""
        if model._meta.app_label == 'WaterSaver':
            return 'raspi'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the WaterSaver app.
        if obj1._meta.app_label == 'WaterSaver' and obj2._meta.app_label == 'WaterSaver':
            return True
        # No opinion if neither object is in the WaterSaver app (defer to default or other routers).
        elif 'WaterSaver' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the WaterSaver app and the other isn't.
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Example app's models get created on the right database."""
        if app_label == 'WaterSaver':
            # The WaterSaver app should be migrated only on the raspi database.
            return db == 'raspi'
        elif db == 'raspi':
            # Ensure that all other apps don't get migrated on the raspi database.
            return False

        # No opinion for all other scenarios
        return None