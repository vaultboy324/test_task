window.onload = async function () {
    const regionStat = await getRegionStat();
    fillRegionStatTable(regionStat);
}

async function getRegionStat() {
    const response = await fetch('http://localhost:5000/data/stat');
    return await response.json();
}

function fillRegionStatTable(regionStat) {
    let regionStatTable = document.getElementById('statTable');

    regionStat.forEach((current_info) => {
        let row = regionStatTable.insertRow(-1);
        row.id = current_info.id;

        let regionCell = row.insertCell(-1);
        regionCell.innerHTML = current_info.region;

        let countCell = row.insertCell(-1);
        countCell.innerHTML = current_info.count;

        row.onclick = (e) => {
            e.preventDefault();

            let rowId = e.target.closest('tr').id;
            window.location.replace(getLinkToRedirect(rowId))
        }

    });
}

function getLinkToRedirect(regionId){
    let link = document.location.href;
    link = link.replace('stat', 'cities_stat');
    return `${link}/${regionId}`
}