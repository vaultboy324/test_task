window.onload = async function () {
    await updateTable();
}

async function getComments() {
    const response = await fetch('http://localhost:5000/data/comment');
    return await response.json();
}

function fillCommentsTable(comments) {
    let commentsTable = document.getElementById('commentsTable');

    comments.forEach((current_comment) => {
        let row = commentsTable.insertRow(-1);
        row.id = current_comment.id;

        let surnameCell = row.insertCell(-1);
        surnameCell.innerHTML = current_comment.surname;

        let nameCell = row.insertCell(-1);
        nameCell.innerHTML = current_comment.name;

        let fatherNameCell = row.insertCell(-1);
        fatherNameCell.innerHTML = current_comment.father_name

        let regionCell = row.insertCell(-1);
        regionCell.innerHTML = current_comment.region;

        let cityCell = row.insertCell(-1);
        cityCell.innerHTML = current_comment.city;

        let phoneCell = row.insertCell(-1);
        phoneCell.innerHTML = current_comment.phone;

        let emailCell = row.insertCell(-1);
        emailCell.innerHTML = current_comment.email;

        let commentCell = row.insertCell(-1);
        commentCell.innerHTML = current_comment.comment_text;

        let buttonCell = row.insertCell(-1);
        let deleteButton = document.createElement('button');
        deleteButton.innerText = 'Удалить';
        deleteButton.onclick = async function (e) {
            const commentId = e.target.closest('tr').id;
            await deleteComment(commentId);
            await updateTable();

        };
        buttonCell.appendChild(deleteButton);
    });
}

function clearTable() {
    let commentsTable = document.getElementById('commentsTable');
    while (commentsTable.rows.length > 1) {
        commentsTable.deleteRow(commentsTable.rows.length - 1);
    }
}

async function deleteComment(commentId) {
    await fetch(`http://localhost:5000/comment/${commentId}`, {
        method: 'DELETE'
    });
}

async function updateTable() {
    clearTable();
    const comments = await getComments();
    fillCommentsTable(comments);
}