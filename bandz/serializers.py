import ast
from datetime import datetime
from rest_framework.serializers import ModelSerializer, CharField, RelatedField, ValidationError
from api_.models import Model, Place, MusicGenre, User, Fa, Band, Host, Event, Proposition, EventPublic
from api_.services import get_place_from_google_places


def _generic_to_internal_value(data, to_internal_type: type(Model)):
    if isinstance(data, str) and '"' in data:
        # It must be a JSON
        try:
            json_dict = ast.literal_eval(data)
            data = json_dict.get('id', None)
        except ValueError:
            raise ValidationError('Malformed {} instance'.format(str(to_internal_type)))
    try:
        return to_internal_type.objects.get(pk=data)
    except to_internal_type.DoesNotExist:
        raise ValidationError(
            'No instance of {} was found matching the provided data'.format(str(to_internal_type)))


class PlaceRelatedField(RelatedField):
    def get_queryset(self):
        return Place.objects.all()

    def to_representation(self, value):
        return str({
            'id': value.id,
            'formatted_address': value.formatted_address,
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=Place)


class MusicGenreRelatedField(RelatedField):
    def get_queryset(self):
        return MusicGenre.objects.all()

    def to_representation(self, value):
        return str({
            'id': value.id,
            'name': value.name
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=MusicGenre)


class FaRelatedField(RelatedField):
    def get_queryset(self):
        return Fa.objects.all()
    
    def to_representation(self, value):
        return str({
            'id': value.id,
            'full_name': value.user.get_full_name(),
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=Fa)


class BandRelatedField(RelatedField):
    def get_queryset(self):
        return Band.objects.all()

    def to_representation(self, value):
        return str({
            'id': value.id,
            'name': value.name,
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=Band)


class HostRelatedField(RelatedField):
    def get_queryset(self):
        return Host.objects.all()

    def to_representation(self, value):
        return str({
            'id': value.id,
            'name': value.name,
            'place': str({
                'id': value.place.id,
                'formatted_address': value.place.formatted_address,
            })
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=Host)


class EventRelatedField(RelatedField):
    def get_queryset(self):
        return Event.objects.all()

    def to_representation(self, value):
        return str({
            'id': value.id,
            'name': value.name,
            'starts_at': str(value.starts_at),
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=Event)


class PropositionRelatedField(RelatedField):
    def get_queryset(self):
        return Proposition.objects.all()

    def to_representation(self, value):
        return str({
            'id': value.id,
            'band': {
                'id': value.band.id,
                'name': value.band.name,
            },
            'host': {
                'id': value.host.id,
                'name': value.host.name,
            },
            'event': {
                'id': value.event.id,
                'name': value.event.name,
                'starts_at': str(value.event.starts_at),
            },
            'message': value.message,
            'price': value.price,
            'confirmed': value.confirmed,
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=Proposition)


class EventPublicRelatedField(RelatedField):
    def get_queryset(self):
        return EventPublic.objects.all()

    def to_representation(self, value):
        return str({
            'id': value.id,
            'fa': {
                'id': value.fa.id,
                'full_name': value.fa.user.get_full_name(),
            },
            'event': {
                'id': value.event.id,
                'name': value.event.name,
                'starts_at': str(value.event.starts_at),
            },
            'feeling': value.feeling,
            'rating': value.rating,
            'comment': value.comment,
        })

    def to_internal_value(self, data):
        return _generic_to_internal_value(data, to_internal_type=EventPublic)


# ----------------- Model Serializers ----------------- #
class PlaceSerializer(ModelSerializer):
    formatted_address = CharField(read_only=True)

    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ('formatted_address', )

    def create(self, validated_data):
        place = get_place_from_google_places(place_id=validated_data['id'])
        if place:
            return place
        else:
            raise ValidationError('There is no place with this place_id')


class MusicGenreSerializer(ModelSerializer):
    class Meta:
        model = MusicGenre
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'groups', )


class FaSerializer(ModelSerializer):
    music_genres = MusicGenreRelatedField(many=True)
    events = EventPublicRelatedField(many=True, source='eventpublic_set', read_only=True)

    class Meta:
        model = Fa
        fields = '__all__'
        read_only_fields = ('user',)


class BandSerializer(ModelSerializer):
    events = EventRelatedField(many=True)
    propositions = PropositionRelatedField(many=True)
    music_genres = MusicGenreRelatedField(many=True)
    place = PlaceRelatedField()

    class Meta:
        model = Band
        fields = '__all__'
        read_only_fields = ('user',)


class HostSerializer(ModelSerializer):
    events = EventRelatedField(many=True)
    propositions = PropositionRelatedField(many=True)
    music_genres = MusicGenreRelatedField(many=True)
    place = PlaceRelatedField()

    class Meta:
        model = Host
        fields = '__all__'
        read_only_fields = ('user',)


class EventSerializer(ModelSerializer):
    band = BandRelatedField(read_only=True)
    host = HostRelatedField()
    music_genres = MusicGenreRelatedField(many=True)
    public = EventPublicRelatedField(many=True, source='eventpublic_set', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('confirmed', 'band',)
        depth = 1

    @staticmethod
    def _validate_time_lapse(starts_at: datetime, ends_at: datetime):
        if starts_at >= ends_at:
            raise ValidationError('starts_at must be earlier than ends_at')

    def create(self, validated_data):
        self._validate_time_lapse(
            validated_data.get('starts_at', None),
            validated_data.get('ends_at', None),
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        starts_at = validated_data.get('starts_at', instance.starts_at)
        ends_at = validated_data.get('ends_at', instance.ends_at)
        self._validate_time_lapse(starts_at, ends_at)
        return super().update(instance, validated_data)


class NewPropositionSerializer(ModelSerializer):
    band = BandRelatedField()
    host = HostRelatedField()
    event = EventRelatedField()

    class Meta:
        model = Proposition
        fields = '__all__'


class ExistingPropositionSerializer(ModelSerializer):
    band = BandRelatedField(read_only=True)
    host = HostRelatedField(read_only=True)
    event = EventRelatedField(read_only=True)

    class Meta:
        model = Proposition
        fields = '__all__'


class EventPublicSerializer(ModelSerializer):
    fa = FaRelatedField()
    event = EventRelatedField()

    class Meta:
        model = EventPublic
        fields = '__all__'

    def update(self, instance, validated_data):
        if instance.event_id != validated_data.get('event_id', None) \
                or instance.fa_id != validated_data.get('fa_id', None):
            raise ValidationError('event_id and fa_id are read-only after creation')
        else:
            return super().update(instance, validated_data)
