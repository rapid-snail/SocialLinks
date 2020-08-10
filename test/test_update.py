import pytest
from model.profile import Profile
from data.profile import test_data


@pytest.mark.parametrize("data", test_data)
def test_update_name(app, data):
    new_data = Profile()
    if data.name is not None:
        new_data.name = data.name
    if data.country is not None:
        new_data.country = data.country
    if data.business is not None:
        new_data.business = data.business
    if data.phone is not None:
        new_data.phone = data.phone
    if data.phone_code is not None:
        new_data.phone_code = data.phone_code

    old_profile = app.profile.get_profile_info()
    app.profile.update(new_data)
    # проверки сохранились ли данные в профиле после logout'а из профиля
    # new_profile = app.profile.get_profile_info()
    # if new_data.name is not None:
    #     assert new_profile.name == new_data.name
    # else:
    #     assert new_profile.name == old_profile.name
    #
    # assert old_profile.email == new_profile.email
    #
    # if new_data.country is not None:
    #     assert new_profile.country == new_data.country
    # else:
    #     assert new_profile.country == old_profile.country
    #
    # if new_data.phone_code is not None:
    #     assert new_profile.phone_code == new_data.phone_code
    # else:
    #     assert new_profile.phone_code == old_profile.phone_code
    #
    # if new_data.phone is not None:
    #     assert new_profile.phone == new_data.phone
    # else:
    #     assert new_profile.phone == old_profile.phone
    #
    # if new_data.business is not None:
    #     assert new_profile.business == new_data.business
    # else:
    #     assert new_profile.business == old_profile.business
