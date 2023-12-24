from rest_framework import serializers

from links.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link

        fields = ("url",)


class LinkDetailSerializer(serializers.ModelSerializer):
    shortened_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ("url", "shortened_url")

    def get_shortened_url(self, obj):
        request = self.context.get('request')
        domain = self._get_request_domain(request)
        return f"{domain}/{obj.id}"

    def _get_request_domain(self, request):
        scheme = request.scheme
        host = request.get_host()
        return f"{scheme}://{host}"
