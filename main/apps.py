from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    # Execute on start-up, add all predefined categories to database
    def ready(self):
        try:
            from .models import Area
            # Add the following pre-defined categories:
            area_names = ["Video & Animation", "Graphics & Design", "Writing", "Translation", "Technology", "Music & Audio"]
            for name in area_names:
                if not Area.objects.filter(name=name).exists():
                    area = Area(name=name)
                    area.save()
        except:
            print("Failed to add categories")
