import os

project_root = 'laborator5'  # Numele folderului modificat

structure = {
    'run.py': '''from flask import Flask, render_template
from app.routes.items import items_bp
import os

app = Flask(__name__, static_folder='static', template_folder=os.path.join('app', 'templates'))

app.register_blueprint(items_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
''',

    os.path.join('app', 'routes', 'items.py'): '''import json
from flask import Blueprint, request, jsonify, abort
import os

items_bp = Blueprint('items_bp', __name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'items.json')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

@items_bp.route('/items', methods=['GET'])
def get_items():
    data = load_data()
    return jsonify(data), 200

@items_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    data = load_data()
    item = next((i for i in data if i['id'] == item_id), None)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@items_bp.route('/items', methods=['POST'])
def create_item():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    new_item = request.get_json()

    if not all(k in new_item for k in ('name', 'quantity', 'price')):
        return jsonify({'error': 'Missing fields'}), 400

    data = load_data()
    new_id = max((item['id'] for item in data), default=0) + 1
    new_item['id'] = new_id

    if not isinstance(new_item['name'], str) or \\
       not isinstance(new_item['quantity'], int) or \\
       not isinstance(new_item['price'], (int, float)):
        return jsonify({'error': 'Invalid field types'}), 400

    data.append(new_item)
    save_data(data)
    return jsonify(new_item), 201

@items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    update_data = request.get_json()

    data = load_data()
    item = next((i for i in data if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    for field in ('name', 'quantity', 'price'):
        if field in update_data:
            item[field] = update_data[field]

    save_data(data)
    return jsonify(item), 200

@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()
    item = next((i for i in data if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    data.remove(item)
    save_data(data)
    return jsonify({'message': f'Item {item_id} deleted'}), 200
''',

    os.path.join('app', 'data', 'items.json'): '''[
  {"id": 1, "name": "Mouse", "quantity": 10, "price": 15.5},
  {"id": 2, "name": "Keyboard", "quantity": 5, "price": 25.0},
  {"id": 3, "name": "Monitor", "quantity": 3, "price": 120.0}
]
''',

    os.path.join('app', 'templates', 'index.html'): '''<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8" />
    <title>Inventar Produse</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body class="container mt-4">
    <h1>Inventar Produse</h1>

    <button id="addBtn" class="btn btn-primary mb-3">Adaugă produs</button>

    <table class="table table-bordered" id="itemsTable">
        <thead>
            <tr>
                <th>ID</th><th>Nume</th><th>Cantitate</th><th>Preț</th><th>Acțiuni</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <div class="modal" tabindex="-1" id="itemModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="modalTitle">Adaugă produs</h5>
            <button type="button" class="btn-close" id="closeModal"></button>
          </div>
          <div class="modal-body">
            <form id="itemForm">
              <input type="hidden" id="itemId" />
              <div class="mb-3">
                <label for="itemName" class="form-label">Nume</label>
                <input type="text" class="form-control" id="itemName" required />
              </div>
              <div class="mb-3">
                <label for="itemQuantity" class="form-label">Cantitate</label>
                <input type="number" class="form-control" id="itemQuantity" min="0" required />
              </div>
              <div class="mb-3">
                <label for="itemPrice" class="form-label">Preț</label>
                <input type="number" step="0.01" class="form-control" id="itemPrice" min="0" required />
              </div>
              <button type="submit" class="btn btn-success" id="saveBtn">Salvează</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div id="message" class="mt-3"></div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/script.js"></script>
</body>
</html>
''',

    os.path.join('static', 'script.js'): '''document.addEventListener('DOMContentLoaded', () => {
  const itemsTableBody = document.querySelector('#itemsTable tbody');
  const messageDiv = document.getElementById('message');

  const modal = new bootstrap.Modal(document.getElementById('itemModal'));
  const modalTitle = document.getElementById('modalTitle');
  const itemForm = document.getElementById('itemForm');
  const itemIdInput = document.getElementById('itemId');
  const itemNameInput = document.getElementById('itemName');
  const itemQuantityInput = document.getElementById('itemQuantity');
  const itemPriceInput = document.getElementById('itemPrice');
  const addBtn = document.getElementById('addBtn');
  const closeModalBtn = document.getElementById('closeModal');

  function showMessage(text, isError = false) {
    messageDiv.textContent = text;
    messageDiv.className = isError ? 'alert alert-danger' : 'alert alert-success';
    setTimeout(() => messageDiv.textContent = '', 3000);
  }

  function loadItems() {
    fetch('/items')
      .then(res => res.json())
      .then(data => {
        itemsTableBody.innerHTML = '';
        data.forEach(item => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.quantity}</td>
            <td>${item.price.toFixed(2)}</td>
            <td>
              <button class="btn btn-sm btn-warning editBtn" data-id="${item.id}">Edit</button>
              <button class="btn btn-sm btn-danger deleteBtn" data-id="${item.id}">Delete</button>
            </td>
          `;
          itemsTableBody.appendChild(tr);
        });
      })
      .catch(() => showMessage('Eroare la încărcarea datelor', true));
  }

  addBtn.addEventListener('click', () => {
    modalTitle.textContent = 'Adaugă produs';
    itemIdInput.value = '';
    itemNameInput.value = '';
    itemQuantityInput.value = '';
    itemPriceInput.value = '';
    modal.show();
  });

  closeModalBtn.addEventListener('click', () => modal.hide());

  itemForm.addEventListener('submit', e => {
    e.preventDefault();

    const id = itemIdInput.value;
    const payload = {
      name: itemNameInput.value.trim(),
      quantity: parseInt(itemQuantityInput.value),
      price: parseFloat(itemPriceInput.value)
    };

    if (!payload.name || isNaN(payload.quantity) || isNaN(payload.price)) {
      showMessage('Date invalide', true);
      return;
    }

    if (id) {
      fetch(`/items/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      })
      .then(res => {
        if (res.ok) return res.json();
        else return res.json().then(err => Promise.reject(err));
      })
      .then(() => {
        showMessage('Produs actualizat cu succes');
        modal.hide();
        loadItems();
      })
      .catch(err => showMessage(err.error || 'Eroare la actualizare', true));
    } else {
      fetch('/items', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      })
      .then(res => {
        if (res.status === 201) return res.json();
        else return res.json().then(err => Promise.reject(err));
      })
      .then(() => {
        showMessage('Produs adăugat cu succes');
        modal.hide();
        loadItems();
      })
      .catch(err => showMessage(err.error || 'Eroare la adăugare', true));
    }
  });

  itemsTableBody.addEventListener('click', e => {
    if (e.target.classList.contains('editBtn')) {
      const id = e.target.dataset.id;
      fetch(`/items/${id}`)
        .then(res => {
          if (res.ok) return res.json();
          else return res.json().then(err => Promise.reject(err));
        })
        .then(item => {
          modalTitle.textContent = 'Editează produs';
          itemIdInput.value = item.id;
          itemNameInput.value = item.name;
          itemQuantityInput.value = item.quantity;
          itemPriceInput.value = item.price;
          modal.show();
        })
        .catch(err => showMessage(err.error || 'Eroare la încărcare produs', true));
    } else if (e.target.classList.contains('deleteBtn')) {
      const id = e.target.dataset.id;
      if (confirm('Sigur ștergeți produsul?')) {
        fetch(`/items/${id}`, { method: 'DELETE' })
          .then(res => {
            if (res.ok) return res.json();
            else return res.json().then(err => Promise.reject(err));
          })
          .then(data => {
            showMessage(data.message);
            loadItems();
          })
          .catch(err => showMessage(err.error || 'Eroare la ștergere', true));
      }
    }
  });

  loadItems();
});
'''
}

def create_structure(base_path, structure_dict):
    for path, content in structure_dict.items():
        full_path = os.path.join(base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    print(f"Proiectul a fost creat în folderul '{base_path}'.")

if __name__ == '__main__':
    create_structure(project_root, structure)
