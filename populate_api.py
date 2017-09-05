import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bandz.settings')

import django
django.setup()

from datetime import datetime
from api_ import models


def populate():
    def populate_place():
        places = [
            models.Place(id='EjJSLiBBdWd1c3RhIC0gQ29uc29sYcOnw6NvLCBTw6NvIFBhdWxvIC0gU1AsIEJyYXNpbA',
                         formatted_address= 'R. Augusta - Consolação - São Paulo, SP - Brasil'),
            models.Place(id='ChIJoYLR3L5ZzpQRhxQbVHJCpMY',
                         formatted_address='Av. Paulista - Paraíso, São Paulo - SP, Brasil'),
            models.Place(id='ChIJvSCkAnhXzpQRmQa9TVrTo3A',
                         formatted_address='Av.Rebouças - Pinheiros - São Paulo, SP - Brasil'),
            models.Place(id='ChIJR1Y3PqlZzpQRlZA82jzXaxw',
                         formatted_address='Praça da Liberdade - Liberdade, São Paulo - SP, Brasil'),
            models.Place(id='ChIJ3dGqMMBXzpQRZ55QWNI9dsk',
                         formatted_address='R.Heitor Penteado - Sumarezinho, São Paulo - SP, Brasil'),
            models.Place(id='ChIJwXjrfaJXzpQR7V9bT95eTbc',
                         formatted_address='R. Inácio Pereira da Rocha, 362 - Pinheiros, São Paulo - SP, 05432-011, Brazil'),
            models.Place(id='ChIJ46dhgp3IyJQR05HldSMaRfs',
                         formatted_address='R.Erasmo Braga, 6 - Jardim Chapadão, Campinas - SP, 13070-147, Brazil')
        ]

        for place in places:
            try:
                models.Place.objects.get(id=place.id)
            except models.Place.DoesNotExist:
                place.save()

    def populate_music_genre():
        music_genres = [
            models.MusicGenre(name='Alternativo'),
            models.MusicGenre(name='Blues'),
            models.MusicGenre(name='Clássica'),
            models.MusicGenre(name='Country'),
            models.MusicGenre(name='Dance'),
            models.MusicGenre(name='Drum and bass'),
            models.MusicGenre(name='Eletrônica'),
            models.MusicGenre(name='Hip-Hop/Rap'),
            models.MusicGenre(name='Gospel'),
            models.MusicGenre(name='J-Pop'),
            models.MusicGenre(name='Jazz'),
            models.MusicGenre(name='Latina'),
            models.MusicGenre(name='New Age'),
            models.MusicGenre(name='Pop'),
            models.MusicGenre(name='Reggae'),
            models.MusicGenre(name='Rock'),
            models.MusicGenre(name='Sertanejo'),
            models.MusicGenre(name='MPB'),
            models.MusicGenre(name='Vocal'),
            models.MusicGenre(name='World'),
        ]

        for music_genre in music_genres:
            models.MusicGenre.objects.get_or_create(name=music_genre.name)

    def populate_auth_user():
        users = [
            models.User(
                username='nilton-ramires',
                password='nilton',
                email='nilton.ramires@gmail.com',
            ),
            models.User(
                username='maria-aparecida',
                password='maria',
                email='maria_aparecida90@hotmail.com',
            ),
            models.User(
                username='aco-pesado',
                password='acopesado',
                email='contato@acopesado.com.br',
            ),
            models.User(
                username='sangue-suga',
                password='sanguesuga',
                email='contato@asanguesuga.com.br',
            ),
            models.User(
                username='roberto-carlos',
                password='roberto',
                email='imprensa@robertocarlos.com.br',
            ),
            models.User(
                username='lavanderia-pop',
                password='lavanderia',
                email='contato@lavanderiapop.com.br',
            ),
            models.User(
                username='morrison-rockbar',
                password='morrison',
                email='contato@morrisonrockbar.com.br',
            ),
        ]

        for user in users:
            try:
                models.User.objects.get(username=user.username)
            except models.User.DoesNotExist:
                models.User.objects.create_user(username=user.username,
                                                email=user.email,
                                                password=user.password)

    def populate_fa():
        fas = [
            models.Fa(
                user=models.User.objects.get(username='nilton-ramires'),
                birth_date=datetime(year=1974, month=4, day=6),
                place=models.Place.objects.get(
                    id='EjJSLiBBdWd1c3RhIC0gQ29uc29sYcOnw6NvLCBTw6NvIFBhdWxvIC0gU1AsIEJyYXNpbA')
            ),
            models.Fa(
                user=models.User.objects.get(username='maria-aparecida'),
                birth_date=datetime(year=1990, month=7, day=25),
                place=models.Place.objects.get(id='ChIJoYLR3L5ZzpQRhxQbVHJCpMY')
            ),
        ]

        for fa in fas:
            models.Fa.objects.get_or_create(user=fa.user, birth_date=fa.birth_date, place=fa.place)

    def populate_band():
        bands = [
            models.Band(
                user=models.User.objects.get(username='aco-pesado'),
                name='Aço Pesado',
                description='Metal pesado e forte',
                url='http://www.facebook.com/?page=aco-pesado',
                place=models.Place.objects.get(id='ChIJvSCkAnhXzpQRmQa9TVrTo3A')
            ),
            models.Band(
                user=models.User.objects.get(username='sangue-suga'),
                name='Sangue-Suga',
                description='Parasitas sonoros com o melhor do flash back',
                url='http://www.facebook.com/?page=sangue-suga',
                place=models.Place.objects.get(id='ChIJ46dhgp3IyJQR05HldSMaRfs')
            ),
            models.Band(
                user=models.User.objects.get(username='roberto-carlos'),
                name='Roberto Carlos',
                description='As mais belas canções que a tua mãe já ouviu',
                url='http://www.globo.com.br/programacao/reveillon/roberto-carlos.hmtl',
                place=models.Place.objects.get(id='ChIJR1Y3PqlZzpQRlZA82jzXaxw')
            ),
        ]

        for band in bands:
            try:
                models.Band.objects.get(user=band.user)
            except models.Band.DoesNotExist:
                band.save()

    def populate_host():
        hosts = [
            models.Host(
                user=models.User.objects.get(username='lavanderia-pop'),
                name='Lavanderia do Pop',
                description='Venha lavar tua alma e teu ouvido com um ótimo som',
                url='http://www.lavanderia-do-pop.com.br/index.php',
                max_capacity=100,
                place=models.Place.objects.get(id='ChIJ3dGqMMBXzpQRZ55QWNI9dsk')
            ),
            models.Host(
                user=models.User.objects.get(username='morrison-rockbar'),
                name='Morrison Rock Bar',
                description='Sempre em busca das melhores bandas, o Morrison Rock Bar não tem medo de ousar',
                url='http://www.morrison.com.br',
                max_capacity=120,
                place=models.Place.objects.get(id='ChIJwXjrfaJXzpQR7V9bT95eTbc')
            ),
        ]

        for host in hosts:
            try:
                models.Host.objects.get(user=host.user)
            except models.Host.DoesNotExist:
                host.save()

    def populate_event():
        events = [
            models.Event(
                name='Lavando o Aço',
                description='A lavanderia recebe sua roupa mais pesada: o couro!',
                starts_at=datetime(year=2017, month=1, day=16, hour=20),
                ends_at=datetime(year=2017, month=1, day=16, hour=23),
                min_age=18,
                price=20.00,
                url='https://www.facebook.com/event/lavando-o-aco',
                host=models.Host.objects.get(name='Lavanderia do Pop'),
                band=models.Band.objects.get(name='Aço Pesado'),
                confirmed=True
            ),
        ]

        for event in events:
            try:
                models.Event.objects.get(name=event.name, starts_at=event.starts_at)
            except models.Event.DoesNotExist:
                event.save()

    def populate_proposition():
        propositions = [
            models.Proposition(
                band=models.Band.objects.get(name='Aço Pesado'),
                host=models.Host.objects.get(name='Lavanderia do Pop'),
                message='Olá Lavanderia, gostaria de levar nosso som às máquinas. Vamos fazer acontecer?',
                price=200.00,
                host_confirmed=True,
                event=models.Event.objects.get(name='Lavando o Aço')
            ),
            models.Proposition(
                band=models.Band.objects.get(name='Sangue-Suga'),
                host=models.Host.objects.get(name='Lavanderia do Pop'),
                message='Olá! Podemos fechar nesse preço mais consumação?',
                price=180.00,
                host_confirmed=None,
                event=models.Event.objects.get(name='Lavando o Aço')
            )
        ]

        for proposition in propositions:
            try:
                models.Proposition.objects.get(band=proposition.band, event=proposition.event)
            except models.Proposition.DoesNotExist:
                proposition.save()

    populate_place()
    populate_music_genre()
    populate_auth_user()
    populate_fa()
    populate_band()
    populate_host()
    populate_event()
    populate_proposition()


if __name__ == '__main__':
    print('Running bandz populate api script')
    populate()
