window.onload = async function () {
    document.querySelector('#send_data').onclick = async (e) => {
        e.preventDefault();
        await send_data(e);
    }

    document.querySelector('#region_selector').onchange = async (e) => {
        const regionSelector = e.target;

        const regionId = regionSelector[regionSelector.selectedIndex].id;

        await updateCitySelector(regionId)
        changePhoneCode()

        changePhoneFieldColor();
    }

    document.querySelector('#city_selector').onchange = (e) => {
        changePhoneCode()

        changePhoneFieldColor();
    }

    document.querySelector('#free_part').oninput = (e) => {
        e.preventDefault();

        changePhoneFieldColor();
    }

    document.querySelector('#email_field').oninput = (e) => {
        changeEmailFieldColor();
    }

    const regions = await get_regions();
    fillRegionSelector(regions);

    await updateCitySelector(regions[0].id);
    changePhoneCode()

    addMandatoryFieldListener('surname_field');
    addMandatoryFieldListener('name_field');
    addMandatoryFieldListener('comment_text');

    changeMandatoryInputColor(document.getElementById('surname_field'));
    changeMandatoryInputColor(document.getElementById('name_field'));
    changeMandatoryInputColor(document.getElementById('comment_text'));
}

async function send_data() {
    let errMessage = '';

    const surname = document.getElementById('surname_field').value;
    if (surname.length === 0) {
        errMessage += 'Не заполнена фамилия\n';
    }

    const name = document.getElementById('name_field').value;
    if (name.length === 0) {
        errMessage += 'Не заполнено имя\n';
    }

    const father_name = document.getElementById('father_name').value;

    let phone = '';
    if (!freePartIsEmpty()) {
        if (validatePhone()) {
            phone = getPhone();
        } else {
            errMessage += 'Некорректно заполнен телефон\n';
        }
    }

    const email = document.getElementById('email_field').value;
    if (!validateEmail()) {
        errMessage += 'Некорректно заполнен почтовый адрес\n';
    }

    const comment_text = document.getElementById('comment_text').value;
    if (comment_text.length === 0) {
        errMessage += 'Поле комментария пустое\n';
    }

    if (errMessage.length !== 0) {
        alert(errMessage)
    } else {
        const citySelector = document.getElementById('city_selector');
        const city_id = citySelector[citySelector.selectedIndex].id;

        const result = {
            surname,
            name,
            father_name,
            phone,
            email,
            comment_text,
            city_id
        }

        const response = await fetch('http://localhost:5000/comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(result)
        });

        if(response.ok){
            alert('Комментарий добавлен');
        } else {
            alert('Что-то пошло не так');
        }
    }
}

async function get_regions() {
    const regionsResponse = await fetch('http://localhost:5000/data/regions');
    const regions = await regionsResponse.json();

    return regions
}

async function get_cities_by_region(regionId) {
    const citiesResponse = await fetch(`http://localhost:5000/data/cities/${regionId}`);
    const cities = await citiesResponse.json();

    return cities;
}

function fillRegionSelector(regions) {
    let regionSelector = document.getElementById('region_selector');

    regions.forEach((current_region) => {
        let option = document.createElement('option');
        option.id = current_region.id;
        option.text = current_region.name;
        regionSelector.add(option);
    });
}

function fillCitySelector(cities) {
    let citySelector = document.getElementById('city_selector');

    cities.forEach((current_city) => {
        let option = document.createElement('option');
        option.id = current_city.id;
        option.text = current_city.name;
        option.value = current_city.code;
        citySelector.add(option);
    });
}

function clearSelector(selector) {
    let options = selector.options;
    for (let i = options.length - 1; i >= 0; i--) {
        options[i] = null;
    }
}

async function updateCitySelector(regionId) {
    const cities = await get_cities_by_region(regionId);

    clearSelector(document.getElementById('city_selector'));
    fillCitySelector(cities);
}

function changePhoneCode() {
    const citySelector = document.getElementById('city_selector');
    const phoneCode = citySelector[citySelector.selectedIndex].value;

    let codeField = document.getElementById('code_field');
    codeField.value = phoneCode;

}

function validatePhone() {
    const phone = getPhone();
    if (phone.length !== 12) {
        return freePartIsEmpty();
    }

    return true;
}

function changePhoneFieldColor() {
    let freePart = document.getElementById('free_part');
    if (validatePhone()) {
        toOk(freePart)
    } else {
        toError(freePart)
    }
}

function validateEmail() {
    const email = document.getElementById('email_field').value;

    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase()) || email.length === 0;
}

function changeEmailFieldColor() {
    let emailInput = document.getElementById('email_field');
    if (validateEmail()) {
        toOk(emailInput);
    } else {
        toError(emailInput);
    }
}

function changeMandatoryInputColor(input) {
    if (input.value.length === 0) {
        toError(input);
    } else {
        toOk(input);
    }
}

function toError(input) {
    input.style.borderColor = "#ff0000"
}

function toOk(input) {
    input.style.borderColor = ''
}

function getPhone() {
    return document.getElementById('phone_field').value +
        document.getElementById('code_field').value +
        document.getElementById('free_part').value;
}

function freePartIsEmpty() {
    const freePart = document.getElementById('free_part').value;
    return freePart.length === 0
}

function addMandatoryFieldListener(id) {
    document.querySelector(`#${id}`).oninput = (e) => {
        changeMandatoryInputColor(e.target);
    }
}