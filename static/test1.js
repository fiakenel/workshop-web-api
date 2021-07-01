const uri = '/clients';
let clients = [];

function getClients() {
     fetch(uri)
        .then(response => response.json())
        .then(data => _displayClients(data))
        .catch(error => console.error('Unable to get clients.', error));
}

function addClient() {
    const addNameTextbox = document.getElementById('add-name');
    const addPhoneTextBox = document.getElementById('add-phone');

    const client = {
        name: addNameTextbox.value.trim(),
        phone: addPhoneTextBox.value.trim(),
    };

    fetch(uri, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(client)
    })
        .then(response => response.json())
        .then(() => {
            getClients();
            addNameTextbox.value = '';
            addPhoneTextBox.value = '';
        })
        .catch(error => console.error('Unable to add client.', error));
}

function deleteClient(id) {
    fetch(`${uri}/${id}`, {
        method: 'DELETE'
    })
        .then(() => getClients())
        .catch(error => console.error('Unable to delete client.', error));
}

function displayEditForm(id) {
    const client = clients.find(client => client.id === id);

    document.getElementById('edit-id').value = client.id;
    document.getElementById('edit-name').value = client.name;
    document.getElementById('edit-phone').value = client.phone;
    document.getElementById('editForm').style.display = 'block';
}

function updateClient() {
    const clientId = document.getElementById('edit-id').value;
    const client = {
        id: parseInt(clientId, 10),
        name: document.getElementById('edit-name').value.trim(),
        phone: document.getElementById('edit-phone').value.trim()
    };

    fetch(`${uri}/${clientId}`, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(client)
    })
        .then(() => getClients())
        .catch(error => console.error('Unable to update client.', error));

    closeInput();

    return false;
}

function closeInput() {
    document.getElementById('editForm').style.display = 'none';
}


function _displayClients(data) {
    const tBody = document.getElementById('clients');
    tBody.innerHTML = '';

 
    const button = document.createElement('button');

    data.forEach(client => {
        let editButton = button.cloneNode(false);
        editButton.innerText = 'Edit';
        editButton.setAttribute('onclick', `displayEditForm(${client.id})`);

        let deleteButton = button.cloneNode(false);
        deleteButton.innerText = 'Delete';
        deleteButton.setAttribute('onclick', `deleteClient(${ client.id })`);

        let tr = tBody.insertRow();

 
        let td1 = tr.insertCell(0);
        let textNode = document.createTextNode(client.name);
        td1.appendChild(textNode);

        let td2 = tr.insertCell(1);
        let textNodeInfo = document.createTextNode(client.phone);
        td2.appendChild(textNodeInfo);

        let td3 = tr.insertCell(2);
        td3.appendChild(editButton);

        let td4 = tr.insertCell(3);
        td4.appendChild(deleteButton);
    });

    clients = data;
}
