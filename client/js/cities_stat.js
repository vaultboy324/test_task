window.onload = async function () {
    const citiesStat = await getCitiesStat();
    fillCitiesStatTable(citiesStat)
}

async function getCitiesStat() {
    const id = getRegionIdFromUrl();
    const response = await fetch(`http://localhost:5000/data/cities_stat/${id}`);
    return await response.json();
}

function fillCitiesStatTable(citiesStat){
    let citiesStatTable = document.getElementById('statTable');

    citiesStat.forEach((current_info)=>{
       let row = citiesStatTable.insertRow(-1);

       let regionCell = row.insertCell(-1);
       regionCell.innerHTML = current_info.region;

       let cityCell = row.insertCell(-1);
       cityCell.innerHTML = current_info.city;

       let countCell = row.insertCell(-1);
       countCell.innerHTML = current_info.count;

    });
}

function getRegionIdFromUrl(){
    let link = document.location.href;
    const url = new URL(link);
    const pathname = url.pathname;

    let params = pathname.split('/');
    params.splice(0, 1);

    if(params.length < 2){
        window.location.replace(`${link}/1`)
        return 1;
    }

    if(!validateId(params[1])){
        link = link.replace(pathname, '/stat');
        window.location.replace(link)
        return 1;
    }

    return params[1];
}

function validateId(id) {
    const re = /^\d+$/;
    return re.test(String(id).toLowerCase());
}
