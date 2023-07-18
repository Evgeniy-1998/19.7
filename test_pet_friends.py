import string
import random

from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Fred', animal_type='cat',
                                     age='3', pet_photo='img/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Fred", "cat", "3", "img/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Fred', animal_type='cat', age=3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_with_valid_date_without_photo(name='Dora', animal_type='cat', age="1212"):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters_and_digits) for i in range(length))


#Тест 1. Проверка получения ключа API при усолвии, что введён не валидный пароль
def test_get_api_wrong_password(email = valid_email, password = generate_random_string(10)):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
        print("Введите правильный пароль.")


#Тест 2. Проверка получения ключа API при условии, что не введён пароль
def test_get_api_key_without_password(email = valid_email, password = ""):
    status, _ = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
        print("Введите пароль!")


#Тест 3. Проверка получения ключа API при условии, что введён не валидный адрес электронной почты
def test_get_api_key_wrong_email(email = generate_random_string(10), password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
        print("Введите правильный адрес электронной почты!")


#Тест 4. Проверка получения API при условии, что адрес электронной почты не введён.
def test_get_api_key_without_email(email = '', password = valid_password):
    status, _ = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
        print("Введите адрес электронной почты!")


#Тест 5. Проверка добавления питомца без фото.
def test_add_pet_without_photo_with_walid_data(name = fed, animal_type = cat, age = 5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert result['name'] == name
    print(name, animal_type, age)


#Тест 6. Проверка невозможности получения списка питомцев.
def test_get_all_pets_with_wrong_key(filter = 'my_pets'):
    auth_key = {'key' : 'wrong_api'}
    status, _ = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


#Тест 7. Проверка невозможности удаления питомца с помощью невалидного API ключа
def test_delete_pet_with_wrong_api_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_pet_without_photo(auth_key, "aaa", "bbb", "4")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    auth_key = {'key': 'wrong_api'}
    status = pf.delete_pet(auth_key, pet_id)
    assert status == 403


#Тест 8. Проверка невозможности обновления информации с помощью невалидного API ключа
def test_update_pet_info_with_wrong_api_key(name = generate_random_string(7), animal_type = 'dog', age = 3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    auth_key = {'key': 'wrong_api'}
    status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 403


#Тест 9. Проверка невозможности получения списка питомцев с неправильным фильтром
def test_get_all_pets_with_wrong_filter(filter = str(generate_random_string(7))):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


#Тест 10. Проверка возможности добавить нового питомца без имени
def test_add_new_pet_without_name(name = None, animal_type = 'crocodile', age = '15', pet_photo='img/croco.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
