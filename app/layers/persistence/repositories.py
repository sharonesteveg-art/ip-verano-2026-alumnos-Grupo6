# capa DAO de acceso/persistencia de datos.
from app.models import Favourite

def saveFavourite(fav):
    # Crear y guardar un registro en la tabla Favourite usando los campos de la Card.
    # 'fav' es un objeto Card con atributos (name, gender, ...). Aquí lo persistimos en la BD.
    fav = Favourite.objects.create(
        name=fav.name,
        gender=fav.gender,
        status=fav.status,
        occupation=fav.occupation,
        phrases=fav.phrases,
        age=fav.age,
        image=fav.image,
        user=fav.user
    )
    return fav

def getAllFavourites(user):
    """
    Obtiene todos los favoritos de un usuario desde la base de datos.
    """
    # Consultar la tabla Favourite y devolver una lista de diccionarios con los campos necesarios.
    # Usamos .values() para obtener diccionarios que luego el translator puede mapear a Card.
    favs_qs = Favourite.objects.filter(user=user).values(
        'id', 'name', 'gender', 'status', 'occupation', 'phrases', 'age', 'image'
    )
    return list(favs_qs)

def deleteFavourite(favId):
    # Borrar el favorito cuya PK es 'favId'.
    favourite = Favourite.objects.get(id=favId)
    favourite.delete()
    return True